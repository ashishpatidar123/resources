# Microservices Data Consistency: Dual-Write, 2PC and the Transactional Outbox Pattern

## 1. Introduction

When we break a monolith into microservices, each service usually has its own database. So we lose the safety of a single, centralized database transaction which covers everything.

Now suppose a service has to update its own database **and** tell other services about it by publishing an event to a message broker. Keeping data consistent across these independent systems, without crushing system latency, is one of the defining challenges of distributed architecture.

!!! note "The Basic Idea"
    Don't write to two different systems (database and Kafka) in one go. Write only to the local database in a single transaction, and let a separate process deliver the event to Kafka.

In this article we will go through three approaches:

`Dual-Write (naive)` → `Two-Phase Commit (legacy)` → `Transactional Outbox (modern standard)`

---

## 2. The Problem: The Dual-Write Problem

### The Naive Approach

Let's take an example. An Order Service needs to save an order to its PostgreSQL database and immediately publish an `OrderCreated` event to an Apache Kafka topic, so the Inventory Service can reserve stock.

The naive code looks like this:

```java
db.save(order);                        // 1. write to the database
kafka.publish("OrderCreated", order);  // 2. write to Kafka
```

### The Flaw (Partial Failure)

Network calls are fundamentally unreliable. These are two separate systems, so there is no single transaction that covers both writes.

Suppose the database saves successfully, but the Kafka network call times out or the broker crashes:

```text
Order Service   → saves order in DB      ✔
Order Service   → publishes to Kafka    ✘ (failed)
Inventory Service → never hears about the order
```

The Order Service thinks the order exists, but the Inventory Service never hears about it. The two services are now inconsistent, and nothing in the system will fix it automatically (someone needs to find and repair it manually).

### The Reversed Flaw

What if we publish to Kafka *first*, and then the database write fails (for example, due to a constraint violation)?

The Inventory Service reserves stock for a ghost order that does not exist.

!!! note
    Wrapping the code in a database transaction doesn't help. Even if we publish to Kafka inside the transaction, the commit can still fail *after* the message is already sent, and we cannot take the message back.

---

## 3. The Legacy Fix: Two-Phase Commit (2PC)

Historically, enterprise systems solved dual-writes using Distributed Transactions (XA / 2PC), which are governed by a central **Transaction Coordinator**.

### How it Works

* **Phase 1 (Prepare):** The coordinator asks both the Database and the Message Broker to lock their resources and confirm they are ready to commit.
* **Phase 2 (Commit):** If both say "yes", the coordinator sends a global commit. If anyone says "no", it sends a global rollback.

`Coordinator` → `Prepare?` → `DB: yes` + `Broker: yes` → `Commit`

### The Flaws

2PC is the enemy of low-latency systems:

* It requires synchronous, blocking network calls.
* It holds row-level database locks open while waiting for network acknowledgments from external systems.
* If the coordinator crashes after the prepare phase, the participants stay blocked with their locks held, until the coordinator comes back. This is a serious availability risk.
* Modern, high-throughput message brokers like Kafka do not support XA distributed transactions. (Kafka has its own transactions, but they only cover writes inside Kafka, so they can't include your database.)

Because of its poor throughput and availability risks, 2PC is generally avoided in modern microservices.

---

## 4. The Modern Standard: The Transactional Outbox Pattern

To avoid distributed locking, we rely on the guarantees of a single, local ACID database transaction.

### The Mechanics

We create an `Outbox` table in the exact same database as the `Order` table.

### The Atomic Write

When a user places an order, the application writes the `Order` record **and** the `Outbox` event (the message which was intended for Kafka) in a single, local database transaction.

```text
BEGIN TRANSACTION
   INSERT INTO orders  ...   (the business data)
   INSERT INTO outbox  ...   (the event to be sent to Kafka)
COMMIT
```

### The Guarantee

Because relational databases (like PostgreSQL or MySQL) guarantee Atomicity, the order cannot be saved without the outbox event also being saved. If the database crashes mid-write, the entire transaction rolls back.

!!! info
    This only works because both tables are in the **same database**. That is what allows one local transaction to cover both writes.

But writing to the Outbox table is only half of the solution. Now we need to get those events from the table to Kafka.

---

## 5. Change Data Capture (CDC) and the WAL

We still need to get the outbox messages to Kafka, without writing dual-write application code again. For this we use Change Data Capture.

### The Write-Ahead Log (WAL)

When a database commits a transaction, it doesn't immediately write the data to the scattered data files (this requires slow, random I/O). Instead, it appends the transaction sequentially to an append-only file on disk called the **Write-Ahead Log** (WAL in Postgres) or **binlog** (in MySQL). Sequential disk writes are very fast.

This is the same WAL idea we saw before: the log is written first, and the data files are updated later.

### Debezium (The CDC Engine)

Instead of the Java/C++ application pushing to Kafka, we deploy a Change Data Capture (CDC) tool like **Debezium**. Debezium acts as a silent observer. It continuously reads the database's log.

!!! note
    In PostgreSQL, Debezium doesn't read the raw WAL files directly. It uses *logical decoding* through a replication slot, which turns the WAL into a stream of row changes. This needs `wal_level = logical` in the Postgres configuration. Debezium usually runs on top of Kafka Connect.

### The Flow

As soon as Debezium sees a new committed change for the `Outbox` table, it extracts the payload and asynchronously publishes it to Kafka.

`Application` → `Order + Outbox (one DB transaction)` → `WAL` → `Debezium` → `Kafka` → `Inventory Service`

Debezium also has a ready-made **Outbox Event Router** transformation, which reads the outbox rows and routes them to the correct Kafka topics for you.

### The Architecture Advantage

The application thread never waits for Kafka. It simply commits to the local DB and returns a `200 OK` to the user. Latency is minimized, and the dual-write problem is removed from the application code.

!!! tip
    Debezium picks up the `INSERT` from the log, so the outbox rows can be deleted from the table soon after they are inserted. This keeps the outbox table small.

    Another (simpler, but slower) option is a *polling publisher*: a background job which reads new rows from the outbox table every few seconds and publishes them.

---

## 6. Practical Implementation (Java + Spring Data)

First, the Outbox table in the same database:

```sql
CREATE TABLE outbox (
    id             UUID PRIMARY KEY,           -- unique event id (used later for idempotency)
    aggregate_type VARCHAR(100) NOT NULL,      -- e.g. 'ORDER'
    aggregate_id   VARCHAR(100) NOT NULL,      -- e.g. the order id
    event_type     VARCHAR(100) NOT NULL,      -- e.g. 'ORDER_CREATED'
    payload        JSONB        NOT NULL,      -- the message for Kafka
    created_at     TIMESTAMP    NOT NULL DEFAULT now()
);
```

Here is how we implement the Outbox write using standard Spring Boot `@Transactional` semantics.

```java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final OutboxRepository outboxRepository;
    private final ObjectMapper jsonMapper;

    public OrderService(OrderRepository orderRepository,
                        OutboxRepository outboxRepository,
                        ObjectMapper jsonMapper) {
        this.orderRepository = orderRepository;
        this.outboxRepository = outboxRepository;
        this.jsonMapper = jsonMapper;
    }

    // This annotation guarantees both writes succeed, or both fail.
    // There is ZERO network call to Kafka in this thread.
    @Transactional
    public Order createOrder(OrderRequest request) {
        // 1. Save the business entity
        Order newOrder = new Order(request.getCustomerId(), request.getAmount());
        orderRepository.save(newOrder);

        // 2. Create the event payload
        String eventPayload;
        try {
            eventPayload = jsonMapper.writeValueAsString(newOrder);
        } catch (JsonProcessingException e) {
            // Unchecked exception, so Spring rolls back the whole transaction
            throw new IllegalStateException("Could not serialize order event", e);
        }

        // 3. Save to the Outbox table in the SAME database
        OutboxEvent event = new OutboxEvent(
            "ORDER_CREATED",
            newOrder.getId(),
            eventPayload
        );
        outboxRepository.save(event);

        return newOrder;
    }
}
```

!!! warning
    By default, Spring rolls back a transaction only for unchecked exceptions (`RuntimeException` and `Error`). `writeValueAsString` throws a *checked* `JsonProcessingException`, so if we just let it escape from the method, the order would be committed **without** its outbox event, which is exactly the inconsistency we wanted to avoid. That's why we wrap it in an unchecked exception (or use `@Transactional(rollbackFor = Exception.class)`).

!!! tip
    In real projects, it is better to serialize a separate event object (a small DTO) instead of the database entity itself. Then the event format is stable even if the entity changes.

---

## 7. The Trade-off: At-Least-Once Delivery and Idempotency

There are no perfect systems, only trade-offs. The Outbox pattern avoids the blocking of 2PC, but in return we get **Eventual Consistency**: the Inventory Service will see the order a little later, not at the same instant.

### The Consumer Flaw

CDC tools like Debezium guarantee **At-Least-Once** delivery. Suppose Debezium publishes an event to Kafka, but crashes before it can record its offset (how far it has read). When it restarts, it will publish the exact same event again.

### The Requirement (Idempotency)

Because the Outbox pattern can produce duplicate messages (during retries or restarts), the downstream consumer (the Inventory Service) **must be idempotent**. It should track the processed event IDs in its own database, so it doesn't reserve stock twice for the same `OrderCreated` event.

```text
Event arrives (id = 42)
   ├─ id 42 already processed?  → yes → ignore it
   └─ no → reserve stock + save id 42 (in one local transaction)
```

The event ID is the `id` column we created in the outbox table.

### Comparison

| Approach              | Consistency          | Latency                | Main Problem                                      |
| :-------------------- | :------------------- | :--------------------- | :------------------------------------------------ |
| Dual-Write            | Can become wrong     | Low                    | Partial failure loses events or creates ghost events |
| Two-Phase Commit      | Strong               | High (blocking locks)  | Kafka has no XA support; coordinator failure blocks everything |
| Outbox + CDC          | Eventual             | Low                    | Duplicate events, so consumers must be idempotent |

---

## 8. Summary

When microservices must update a local database and publish an event to a message broker, naive dual-writes can lead to inconsistent data because of partial network failures. Traditional Two-Phase Commit (2PC) solves this, but it hurts throughput through blocking locks and is not supported by Kafka.

The Transactional Outbox pattern is the industry standard here: it writes both the business entity and the event to the local database in a single ACID transaction. A separate Change Data Capture (CDC) process (like Debezium) then reads the database log (WAL) and publishes the event to Kafka asynchronously. This guarantees that an event is never lost and keeps application latency low, with the trade-off that the system is eventually consistent and downstream consumers must be designed to handle duplicate messages idempotently.
