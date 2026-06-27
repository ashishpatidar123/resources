# System Design Concepts: A Comprehensive Guide

> A deep-dive into core system design concepts with real-world examples and scenarios.

## Table of Contents

1. [Scalability: Introduction](#1-scalability-introduction)
2. [Horizontal vs. Vertical Scaling](#2-horizontal-vs-vertical-scaling)
3. [Failover Strategies](#3-failover-strategies)
4. [Sharding Databases / NoSQL](#4-sharding-databases-nosql)
5. [Data Lakes](#5-data-lakes)
6. [ACID Compliance and the CAP Theorem](#6-acid-compliance-and-the-cap-theorem)
7. [Using CAP to Choose a Database](#7-using-cap-to-choose-a-database)
8. [Caching: Introduction](#8-caching-introduction)
9. [Caching Technologies](#9-caching-technologies)
10. [Eviction Strategies for Caching](#10-eviction-strategies-for-caching)
11. [Content Distribution Networks (CDNs)](#11-content-distribution-networks-cdns)
12. [Resiliency: Introduction](#12-resiliency-introduction)
13. [Designing for Resiliency](#13-designing-for-resiliency)
14. [Scaling Your Data: Introduction](#14-scaling-your-data-introduction)
15. [Distributed Storage Solutions](#15-distributed-storage-solutions)
16. [HDFS Architecture](#16-hdfs-architecture)
17. [RPO and RTO](#17-rpo-and-rto)
18. [Split-Brain and Distributed Consensus](#18-split-brain-and-distributed-consensus)
19. [OLTP vs. OLAP](#19-oltp-vs-olap)
20. [Consistent Hashing](#20-consistent-hashing)
21. [Fan-out Patterns](#21-fan-out-patterns)
22. [ID Generation Strategies](#22-id-generation-strategies)
23. [Thundering Herd and Cache Stampede](#23-thundering-herd-and-cache-stampede)
24. [Write-Ahead Log (WAL)](#24-write-ahead-log-wal)
25. [Load Balancers](#25-load-balancers)
26. [Message Queues and Event-Driven Architecture](#26-message-queues-and-event-driven-architecture)
27. [API Gateway and Rate Limiting](#27-api-gateway-and-rate-limiting)
28. [SQL vs NoSQL — Comprehensive Comparison](#28-sql-vs-nosql-comprehensive-comparison)
29. [Database Indexes](#29-database-indexes)
30. [Proxy and Reverse Proxy](#30-proxy-and-reverse-proxy)
31. [Microservices vs Monolith](#31-microservices-vs-monolith)
32. [Real-time Communication](#32-real-time-communication)
33. [Distributed Transactions — SAGA and 2PC](#33-distributed-transactions-saga-and-2pc)
34. [Bloom Filters](#34-bloom-filters)
35. [Service Discovery](#35-service-discovery)

---

### Part II — Low Level Design (LLD)

36. [OOP Concepts](#36-oop-concepts)
37. [SOLID Principles](#37-solid-principles)
38. [Design Patterns — Creational](#38-design-patterns-creational)
39. [Design Patterns — Structural and Behavioral](#39-design-patterns-structural-and-behavioral)
40. [LLD Interview Approach and Case Studies](#40-lld-interview-approach-and-case-studies)

---

## 1. Scalability: Introduction

### What is Scalability?
Scalability is the ability of a system to handle increased load (users, data, traffic) without degrading performance.

### Key Metrics to Measure
*   **Throughput** — requests per second
*   **Latency** — time per request
*   **Availability** — uptime percentage (e.g., 99.9%)

### Real-Life Scenario
> 🐦 **Twitter**: Handles ~500 million tweets per day. On a regular Tuesday, traffic is predictable. But during a World Cup final or a breaking news event, traffic spikes 10–20x. A scalable system handles this gracefully instead of crashing.

### Types of Load
| Load Type | Example |
| :--- | :--- |
| **User growth** | App going viral overnight |
| **Data growth** | 10 years of transaction logs |
| **Computation growth** | ML model training on bigger datasets |

---

## 2. Horizontal vs. Vertical Scaling

### Vertical Scaling (Scale Up)
Add more power (CPU, RAM, disk) to an existing machine.

*   **Before:** `[Server: 4 CPU, 16GB RAM]`
*   **After:** `[Server: 32 CPU, 128GB RAM]`
*   **Pros:** Simple, no code changes needed
*   **Cons:** Hardware limits, single point of failure, expensive

### Horizontal Scaling (Scale Out)
Add more machines running the same service.

*   **Before:** `[Server 1]`
*   **After:** `[Server 1] [Server 2] [Server 3]` (← Load Balancer distributes traffic)
*   **Pros:** Nearly unlimited scale, fault-tolerant
*   **Cons:** Requires stateless design, more complex infrastructure

### Real-Life Scenario
> 🎬 **Netflix** uses horizontal scaling. When a new season of a popular show drops, they spin up hundreds of additional servers in minutes using AWS Auto Scaling. They don't just make one server bigger — they add many servers and distribute traffic via load balancers.
> 
> 🚀 **A small startup's database** might start with vertical scaling (upgrading to a bigger RDS instance) before eventually migrating to a distributed database.

### Decision Guide
*   **Is your app stateless?** → Horizontal scaling preferred
*   **Single giant computation?** → Vertical scaling may be simpler
*   **Need 99.99% uptime?** → Horizontal (no single point of failure)

### How to Think About This in an Interview
Don't just pick one — reason through trade-offs step by step:

1.  **Step 1: Calculate the numbers**
    *   Current: 1,000 req/sec. Expected: 50,000 req/sec.
    *   Can one machine handle 50x? *(Often yes, but with a hard ceiling)*
2.  **Step 2: Ask about fault tolerance**
    *   Payment service down = \$1M/minute lost → single machine is unacceptable
    *   Internal metrics dashboard → one machine is fine
3.  **Step 3: Ask about statelessness**
    *   Sessions stored in-process (RAM)? → Horizontal scaling requires redesign
    *   Sessions stored in Redis? → Horizontal scaling = just add machines
4.  **Step 4: Give the pragmatic answer (what interviewers love)**
    *   "Scale vertically first — fast, cheap, zero code change. But design stateless from day one (sessions in Redis, no local disk state) so horizontal scaling is just adding machines when you hit the ceiling."

> ⚠️ **Interview trap:** A candidate who always says "horizontal scaling" without justification sounds rehearsed. The one who says "vertical first, but here's how I'd architect for horizontal" sounds experienced.

---

Interview trap: A candidate who always says "horizontal scaling" without justification sounds rehearsed. The one who says "vertical first, but here's how I'd architect for horizontal" sounds experienced.

## 3. Failover Strategies

### What is Failover?
Failover is the automatic switch to a backup system when the primary system fails.

### Types of Failover

#### Active-Passive (Cold Standby)
*   One server handles traffic; the backup is on standby.
*   On failure, traffic switches to the passive node.
*   **Downtime:** A few seconds to minutes.

```text
[Primary DB] ———(Replication)———> [Standby DB]
  (Traffic)                         (Promoted on failure)

```
#### Active-Active (Hot Standby)
* Both servers handle traffic simultaneously.
* On failure, the remaining node absorbs all traffic.
* **Downtime:** Near-zero.

```text
[Load Balancer]
           /           \
          v             v
     [DB Node A] <---> [DB Node B]
               (Sync)
```
#### Warm Standby
• Backup is running and synced but not serving traffic.
• Faster recovery than cold standby.

### Real-Life Scenario
> **Amazon RDS Multi-AZ** uses Active-Passive failover. Your primary DB is in us-east-1a. If that availability zone goes down, AWS automatically promotes the standby in us-east-1b within ~60 seconds, and your application reconnects via the same DNS endpoint.
> **Google Search** uses Active-Active. Multiple data centers serve requests simultaneously. If one goes down, others absorb the traffic instantly.

### Failover vs. Fallback
- Failover = switching to the backup automatically
- Fallback = switching back to the primary once recovered

### Replication Modes — What Determines Your Data Loss Window

#### Asynchronous Replication (Default in most systems)
```
Primary writes -> immediately confirms to app -> replicates to standby later.
```
-  ✅ Fast writes, standby latency doesn't affect you.
-  ❌ Data loss window exists — standby may lag by seconds.

#### Synchronous Replication
```
Primary writes -> waits for standby ACK -> confirms to app.
```
-  ✅ Zero data loss (every write confirmed on both nodes).
-  ❌ Every write is as slow as the network round-trip to the standby.
-  ❌ If standby is unreachable, primary blocks all writes entirely.

#### Semi-Synchronous (MySQL default)
At least one replica must ACK before the primary confirms. Best balance of safety vs. speed.

### How to Think About Failover Design
```
Question 1: How much data loss is acceptable? -> defines RPO (see Section 17)
Question 2: How long can the system be down? -> defines RTO (see Section 17)
Question 3: Is a brief outage worse than stale data? -> CP vs AP decision

If RPO = 0 (zero data loss acceptable):
       -> Use synchronous replication, accept slower writes.
If RPO = seconds (small loss acceptable):
       -> Use async replication + Kafka as safety net.
       -> Kafka retains events even if DB loses them -> replay on recovery.
If RTO = seconds (must recover instantly):
       -> Active-Active (both nodes always serving traffic).
If RTO = minutes (brief downtime acceptable):
       -> Active-Passive with automated promotion.
```
> 🛠️ **Real-Life:** During a 2 AM PagerDuty incident on a fintech system: primary DB dies at 02:00:00, standby last synced at 01:59:54 — 6 seconds of transactions are lost forever unless Kafka retained those payment events for replay. This is why production financial systems pair async replication with a message queue.

### The Split-Brain Problem (Preview)
When the old primary restarts after failover, two nodes both believe they are primary — causing conflicting writes and data corruption. See [Section 18](#18-split-brain-and-distributed-consensus) for the full breakdown and how STONITH prevents it.

---

## 4. Sharding Databases / NoSQL

### What is Sharding?
Sharding is the process of splitting a large database into smaller pieces (shards) distributed across multiple servers.

```text
                  [ Full User Table (100M rows) ]
                                 |
              +------------------+------------------+
              |                  |                  |
         [ Shard 1 ]        [ Shard 2 ]        [ Shard 3 ]
           (A-H)              (I-P)              (Q-Z)
                      (Sharding by last name)
```
### Sharding Strategies

| Strategy    |    How It Works         |           Example |
|--------------|-------------------------|--------------------|
| **Range-based**  |   Shard by value range     |       User IDs 1-1M -> Shard 1 |
| **Hash-based**    |  shard = hash(key) % N     |      Distributes evenly |
| **Directory-based** |  Lookup table maps key -> shard | Flexible but adds complexity |
| **Geo-based**    |   Shard by geography      |        US users -> US shard |

### NoSQL and Sharding
NoSQL databases like MongoDB, Cassandra, and DynamoDB have sharding (partitioning) built in.
```
# MongoDB sharding example
sh.enableSharding("ecommerce")
sh.shardCollection("ecommerce.orders", { "userId": "hashed" })
```
### Real-Life Scenario
> **Instagram** shards its user data. With 2 billion users, no single PostgreSQL instance can hold all user data. Instagram shards by `user_id`, so user 1-10M lives on Shard 1, 10M-20M on Shard 2, etc. When you load someone's profile, the system knows exactly which shard to query.

> **WhatsApp** messages are sharded by `chat_id` - all messages in a conversation land on the same shard, making reads fast.

### Challenges
- **Cross-shard** joins are expensive
- **Rebalancing** when adding new shards
- **Hot shards** when one key gets all the traffic (e.g., a celebrity's account)

### How to Think About Choosing a Shard Key
The shard key is the most critical architectural decision in a sharded system. Getting it wrong means redesigning storage later.
```
Good shard key:
 ✅ High cardinality (many unique values -> even distribution)
 ✅ Queries mostly hit one shard (avoids cross-shard joins)
 ✅ No celebrity/viral key problem (no single value gets disproportionate traffic)

Bad shard key examples:
  ❌ Shard by country     -> 80% of users in US -> one hot shard
  ❌ Shard by created_date -> all new writes go to "today's" shard
  ❌ Shard by status      -> active/inactive -> massive imbalance
```

### Fixing Hot Shards

> **Scenario:** WhatsApp group with 500K members - millions of reads/writes all hitting one shard (`chat_id = group123`).
```
Fix 1: Sub-sharding the hot key
Split: group123:sub_0, group123:sub_1 ... group123:sub_N
Writes are distributed across sub-shards; reads fan-out + merge results.

Fix 2: Separate storage tier for large groups
Small chats (<1,000 members) -> sharded PostgreSQL
Large groups (>1,000 members) -> Cassandra (built for high write throughput)

Fix 3: Aggressive caching
Last 50 messages of any chat cached in Redis
90% of reads served from cache -> shard barely touched
```

### Consistent Hashing - Solving the Rebalancing Problem
See [Section 20](#20-consistent-hashing) for the full deep-dive.

Simple hash sharding breaks when nodes are added/removed:
```
hash(key) % 3 -> routes to shards 0, 1, 2
Add a 4th shard:
hash(key) % 4 -> COMPLETELY different distribution
              -> almost every key now maps to the wrong shard!
              -> massive data migration required
```
Consistent hashing solves this by ensuring only `1/N` of keys move when a node is added or removed.

## 5. Data Lakes

### What is a Data Lake?
A **centralized repository** that stores all your raw data - structured, semi-structured, and unstructured - at any scale, in its native format.
```
Data Sources                Data Lake (Raw)          Consumers
------------                ---------------          ---------
App logs       ------------> /raw/logs/     --------> BI Dashboards
DB snapshots   ------------> /raw/db-exports/ ------> ML Models
IoT sensors    ------------> /raw/iot/      --------> Data Scientists
Social media   ------------> /raw/social/   --------> Analysts
```
### Data Lake vs. Data Warehouse

| Feature | Data Lake | Data Warehouse |
| :--- | :--- | :--- |
| **Data format** | Raw (any format) | Processed, structured |
| **Schema** | Schema-on-read | Schema-on-write |
| **Storage cost** | Low (object storage) | Higher |
| **Speed to query** | Slower | Faster |
| **Users** | Data scientists | Business analysts |
| **Example** | AWS S3 + Athena | Amazon Redshift, Snowflake |

### Real-Life Scenario
> **Uber** collects GPS pings every few seconds from millions of drivers and riders. This raw data flows into a data lake (on HDFS/S3). Data Scientists use it to train a surge pricing models, route optimization algorithms, and safety anomaly detection - all from the same raw source without tranforming it first.
> **Netflix** stores every click, play, pause, and skip event in a data lake. Engineers can re-process historical data with new algorithms to improve the recommendation engine.

### The "Data Swamp" Problem
A data lake without governance becomes a data swamp - data nobody can find or trust. Solutions:
- Data catalog (Apache Atlas, AWS Glue Catalog)
- Data lineage tracking
- Access controls

### OLTP vs. OLAP - Why You Must Never Run Analytics on Your Production DB
See [Section 19](#19-oltp-vs-olap) for the full deep-dive.

| | OLTP | OLAP |
| :--- | :--- | :--- |
| **Full name** | Online Transaction Processing | Online Analytical Processing |
| **Query pattern** | Small, fast, single-row reads/writes | Massive scans over millions of rows |
| **Use case** | Your app (user actions, payments) | Reporting, dashboards, ML |
| **Database** | PostgreSQL, MySQL, DynamoDB | Redshift, Snowflake, BigQuery |
| **Optimized for** | Low latency, high write throughput | High read throughput, aggregations |

**What happens when an analyst runs a 300M row scan on your production PostgreSQL:**
```
Full table scan -> consumes ALL disk I/O bandwidth
Shared locks held -> write operations queue up behind the scan
Connection pool fills -> app servers time out waiting for a connection
Users see 500 errors / infinite loading spinners

This is called: "OLAP killing OLTP"
```

**The fix:** Data flows OLTP -> Data Lake -> Data Warehouse. Analysts query the warehouse, never the production DB.

### The ETL/ELT Pipeline - Connecting Raw Data to Analytics
```
Production DB (OLTP)
     |
     v  CDC (Change Data Capture) or Nightly Export
     |
Data Lake (S3 / HDFS)                 <- Raw, unprocessed, cheap storage
     |
     v  ETL / ELT (Spark, dbt, Airflow)
     |   - Clean (nulls, format fixes, deduplication)
     |   - Join (enrich with reference data)
     |   - Aggregate (daily totals, user cohorts, funnels)
     |
Data Warehouse (Snowflake / Redshift) <- Structured, fast SQL queries
     |
     v
BI Tools (Tableau, Metabase, Looker)  -> Business dashboards
```

**ETL vs. ELT:**
- **ETL** (Extract -> Transform -> Load): Transform before loading. Old approach, transformation happens outside the warehouse.
- **ELT** (Extract -> Load -> Transform): Load raw first, transform inside the warehouse using SQL. Modern approach - cloud warehouses are powerful enough to handle it, and raw data is preserved for re-processing.

> **Real-Life:** Uber's pipeline - raw GPS pings every 3 seconds -> Data Lake (HDFS/S3) -> Spark transforms -> Hive/Presto Data Warehouse -> analyst dashboards for surge pricing analysis and driver incentive reports.

## 6. ACID Compliance and the CAP Theorem

---

### ACID Properties
ACID guarantees **reliable database transactions**.

#### A - Atomicity
A transaction is **all or nothing**. If one step fails, the entire transaction is rolled back.
```sql
-- Bank Transfer: atomicity ensures both happen or neither does
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE id = 1; -- Debit Alice
  UPDATE accounts SET balance = balance + 500 WHERE id = 2; -- Credit Bob
COMMIT;
-- If step 2 fails, step 1 is also rolled back
```
#### C — Consistency
A transaction brings the database from one valid state to another. No rules (constraints, triggers) are violated.
> **Example:** A `NOT NULL` constraint on an `email` column ensures no transaction can leave a user profile without an email.

#### I — Isolation
Concurrent transactions don't interfere with each other. Each transaction sees a consistent snapshot.
*   **Transaction A:** reads balance (\$1000)
*   **Transaction B:** deducts \$200 concurrently
*   **Transaction A:** should NOT see B's in-progress change until it commits.

> **Isolation levels:** `READ UNCOMMITTED` $\rightarrow$ `READ COMMITTED` $\rightarrow$ `REPEATABLE READ` $\rightarrow$ `SERIALIZABLE`

#### D — Durability
Once committed, data persists even if the system crashes (written to disk, WAL logs, etc.).

---

### CAP Theorem
In a distributed system, you can only guarantee **2 of these 3** properties:

```text
         C (Consistency)
        / \
       /   \
      / PICK\
     /   2   \
    /_________\
A (Availability)  P (Partition Tolerance)
```
| Property | Meaning |
| :--- | :--- |
| **Consistency** | Every read gets the most recent write |
| **Availability** | Every request receives a (non-error) response |
| **Partition Tolerance** | System works even if network splits occur |

> **P is non-negotiable** in distributed systems - network partitions will happen. So the real choice is CP vs. AP.
> 
#### **CP Systems (Consistency + Partition Tolerance)**
- Sacrifice availability during a partition
- Returns an error rather than stale data
- Examples: HBase, Zookeeper, etcd, MongoDB (default config)

#### **AP Systems (Availability + Partition Tolerance)**
- Returns potentially stale data but never an error
- Eventually consistent
- Examples: Cassandra, DynamoDB, CouchDB, DNS

### Real-Life Scenario
> **ATM withdrawals** need CP behavior. You'd rather the ATM refuse a transaction ("system unavailable") than let you overdraw your account due to stale balance data.
> **Facebook's "Like" counter** uses AP behavior. If you like a post, some users might see the old count for a few seconds. That's fine - availability and speed matter more than perfect consistency.

### How to Think About CAP in an Interview
The most common mistake is applying CAP to the **entire system** instead of **per operation**.
```
Wrong: "We use Cassandra, so our system is AP."
Right: "Our payment writes need CP - we use PostgreSQL for those.
       Our activity feed is fine with AP - we use Cassandra for that."
```
**The one question to ask for each feature:**
> *"What is WORSE for the user - seeing stale data, or getting an error?"*
```
Stale data is worse -> CP
Examples: bank balance, inventory stock count, seat booking, distributed lock

Error is worse -> AP
Examples: social feed, recommendations, like counts, search results, GPS location
```
**The per-operation approach in a single system (e.g., ride-sharing app):**
```
Driver location updates (every 3 sec) -> AP (Cassandra)
Slightly stale location is fine; service must always be available

Payment processing -> CP (PostgreSQL)
Must never double-charge; errors are better than wrong charges

Surge pricing calculation -> AP (Cassandra)
A 5-second-stale price is acceptable; pricing must always respond
```
## 7. Using CAP to Choose a Database

### Decision Framework
```
Does your app require strong consistency?
├── YES -> Is high availability critical?
│          ├── YES -> Reconsider design (try saga patterns, 2PC)
│          └── NO  -> Use CP database (PostgreSQL, HBase)
└── NO  -> Can you tolerate eventual consistency?
           ├── YES -> Use AP database (Cassandra, DynamoDB)
           └── NO  -> Rethink requirements
```
### Real-World Mapping

| Use Case | Requirement | Database Choice | Reason |
| :--- | :--- | :--- | :--- |
| **Banking transactions** | Strong consistency | PostgreSQL, CockroachDB | CP - no stale reads |
| **Shopping cart** | High availability | DynamoDB, Cassandra | AP - cart can sync eventually |
| **Distributed locks** | Consistency | etcd, ZooKeeper | CP - must be authoritative |
| **Social media feed** | High availability | Cassandra, DynamoDB | AP - slight staleness OK |
| **Leaderboard/gaming** | Both? | Redis + DB combo | Redis for speed, DB for truth |
| **Ride-sharing location** | Availability + speed | Cassandra | AP - GPS updates every second |

### Real-Life Scenario
> **Amazon Shopping Cart** uses AP (DynamoDB). If two devices add items simultaneously during a network glitch, both items are kept (merge conflict resolved by keeping all). This is better than failing the add.
> **Google Spanner** attempts to provide ACID + global distribution using atomic clocks (TrueTime API) - a rare CP+global system.

## 8. Caching: Introduction

### What is Caching?
Storing frequently accessed data **closer to the consumer** (in faster storage like RAM) to reduce latency and backend load.
```
Without Cache:                With Cache:
User -> DB (50ms)            User -> Cache (0.5ms) -> Cache Hit
                              User -> DB (50ms)     -> Cache Miss (then populate cache)
```
### Cache Hit vs. Cache Miss
- **Cache Hit** - data found in cache -> fast response
- **Cache Miss** - data not in cache -> fetch from source, then store in cache
- **Hit Rate** = hits / (hits + misses) - aim for > 90%

### Where to Cache

| Layer | Example | Latency |
| :--- | :--- | :--- |
| **CPU L1/L2/L3** | Hardware cache | < 1 ns |
| **In-memory (app)** | Java HashMap | ~ 1 µs |
| **Distributed cache** | Redis, Memcached | ~ 0.5 ms |
| **CDN** | CloudFront, Cloudflare | ~ 10-50 ms |
| **Database query cache** | MySQL query cache | ~ 1-5 ms |

### Caching Patterns

#### Cache-Aside (Lazy Loading)
```
1. App checks cache
2. Cache miss -> app fetches from DB
3. App writes result to cache
4. Future requests hit cache
```

#### Write-Through
```
1. App writes to cache AND DB simultaneously
2. Cache is always in sync
3. Slightly slower writes, but no stale data
```

#### Write-Back (Write-Behind)
```
1. App writes to cache only
2. Cache asynchronously writes to DB later
3. Fast writes, risk of data loss if cache crashes
```

#### Cache Invalidation on Write (Most Common Fix for Stale Data)
```
Admin updates product price -> write to DB -> DELETE product:123 from Redis
Next read -> cache miss -> fetches fresh data from DB -> re-caches it
```
- ✅ Simple, always correct after one miss
- ✅ No risk of data loss (DB is always the source of truth)
- ❌ One cache miss per update (acceptable when writes are rare)
- **Best for**: Product prices, user profiles, config values

### How to Think About Which Pattern to Use
```
Data changes rarely + correctness critical?
└──> Cache Invalidation on Write (delete key on every update)

Data changes frequently + write speed matters?
└──> Write-Through (always write to cache + DB together)

Ultra-high write throughput, some loss acceptable?
└──> Write-Back (counters, IoT sensor data)

Data has a natural expiry window?
└──> TTL (stock prices, exchange rates, weather)

Don't know access patterns upfront?
└──> Cache-Aside / Lazy Loading (default safe choice)
```

> **Interview pattern:** When asked "the website showed a stale price after an update", the answer is always **Cache Invalidation on Write** - not Write-Back (which is riskier) and not just TTL (which leaves stale data for minutes).

### Real-Life Scenario
> **Twitter's home timeline** is pre-computed and cached per user in Redis. When you open Twitter, it reads from the cache (microseconds), not from a complex SQL join across billions of tweets (seconds). The cache is updated when people follow tweets.

## 9. Caching Technologies

### Redis
An in-memory data structure store supporting strings, hashes, lists, sets, sorted sets, streams.
```bash
# Redis basics
SET user:1001:name "Alice"         # Store
GET user:1001:name                 # Retrieve -> "Alice"
SETEX session:abc123 3600 "user_1" # Store with TTL (1 hour)
INCR page:views:home               # Atomic counter
ZADD leaderboard 9500 "Alice"      # Sorted set (leaderboards)
```

**Use cases:** Sessions, leaderboards, pub/sub, rate limiting, queues

### Memcached
Simple, high-performance, distributed memory caching. Only supports key-value strings.
```java
XMemcachedClient client = new XMemcachedClientBuilder("localhost:11211").build();
client.set("user_1001", 3600, serializedUserData);
Object result = client.get("user_1001");
```
**Use cases:** Simple object caching, when you don't need Redis's advanced features

### Redis vs. Memcached

| Feature | Redis | Memcached |
| :--- | :--- | :--- |
| **Data structures** | Rich (lists, sets, etc.) | Key-value only |
| **Persistence** | Yes (RDB, AOF) | No |
| **Replication** | Yes | No |
| **Clustering** | Yes (Redis Cluster) | Limited |
| **Pub/Sub** | Yes | No |
| **Lua scripting** | Yes | No |

### Varnish (HTTP Cache)
Sits in front of your web server, caches full HTTP responses.
```
Browser -> Varnish -> Web Server
           ↑ Returns cached HTML/JSON
```

**Use cases:** Caching entire API responses or web pages

### Real-Life Scenario
> **Instagram** uses both Redis and Memcached at massive scale. Redis handles the social graph (who follows whom) and Memcached caches serialized Python objects (user profiles, media metadata) as a last resort.

## 10. Eviction Strategies for Caching

When a cache is **full**, old entries must be removed to make room for new ones. The strategy determines which entries are evicted.

### LRU — Least Recently Used
Evicts the entry that hasn't been accessed for the longest time.
```
Cache (capacity: 3):
[A, B, C] -> Access D -> evict A (oldest) -> [B, C, D]
```

**Best for:** General-purpose caching, web sessions
**Used by:** Redis (default policy), many CPU caches

### LFU — Least Frequently Used
Evicts the entry with the fewest total accesses.
```
Cache: A(accessed 10x), B(accessed 2x), C(accessed 1x)
Add D -> evict C (least frequent) -> [A, B, D]
```

**Best for:** When popular items should stay forever
**Pitfall:** New items are always at risk of eviction before they get popular

### FIFO — First In, First Out
Evicts the oldest inserted entry, regardless of usage.

```
Queue: [A, B, C] -> Add D -> evict A -> [B, C, D]
```

**Simple but rarely optimal** — a heavily used old item gets evicted unfairly.

### TTL — Time To Live
Each entry expires after a set duration.

```java
jedis.setex("product:123", 300, productJson); // expires in 5 minutes
```

**Best for:** Data that becomes stale (stock prices, weather, exchange rates)

### Random Replacement
Evicts a random entry. Surprisingly effective and CPU-cheap.

### MRU — Most Recently Used
Evicts the most recently used entry. Counterintuitive but useful when old data is more likely to be accessed again (e.g., rotating through a dataset once).

### Summary Table

| Strategy | Evicts | Best For |
| :--- | :--- | :--- |
| **LRU** | Least recently accessed | General purpose |
| **LFU** | Least frequently accessed | Popularity-based caching |
| **FIFO** | Oldest inserted | Simple queues |
| **TTL** | Expired entries | Time-sensitive data |
| **Random** | Random entry | Low overhead needs |
| **MRU** | Most recently accessed | Cyclical access patterns |

### Real-Life Scenario
> **Redis** with maxmemory-policy allkeys-lru will automatically evict the least recently used keys when it hits its memory limit. A news website using Redis to cache articles would naturally keep today's top stories in cache (frequently accessed) while yesterday's stories are evicted.

> **Browser cache** uses TTL: Cache-Control: max-age=86400 tells the browser to keep a CSS file for 24 hours before re-fetching.

## 11. Content Distribution Networks (CDNs)

### What is a CDN?
A CDN is a geographically distributed network of servers (Points of Presence / PoPs) that delivers content to users from the nearest location.

```
Without CDN:
User in Tokyo ------------------------------> Origin Server (New York) [200ms]

With CDN:
User in Tokyo -> CDN PoP (Tokyo) -> Origin (only on cache miss) [10ms]
```

### How CDNs Work
1. User requests https://cdn.example.com/logo.png
2. DNS resolves to nearest CDN PoP (based on Anycast routing)
3. CDN checks its cache -> Cache Hit -> returns immediately
4. Cache Miss -> CDN fetches from origin, caches it, returns to user
5. Next user in same region -> instant cache hit

### What CDNs Cache
- **Static assets:** Images, CSS, JS, fonts, videos
- **Dynamic content:** Some CDNs (Cloudflare Workers, Lambda@Edge) run code at the edge
- **API responses:** With appropriate cache headers

### Popular CDNs

| CDN | Known For |
| :--- | :--- |
| **Cloudflare** | Security + performance, free tier |
| **AWS CloudFront** | Deep AWS integration |
| **Akamai** | Enterprise, oldest CDN |
| **Fastly** | Real-time purging, Varnish-based |
| **Google Cloud CDN** | GCP integration |

### Real-Life Scenario
> **Netflix** uses their own CDN called Open Connect. They place servers inside ISP data centers (Comcast, AT&T, etc.). When you stream a popular show, the data never leaves the ISP's network — it comes from a server physically near you. This is why Netflix can stream 4K to 200M+ subscribers simultaneously.

> **Spotify** uses CDNs to distribute song files. The MP3 file for "Blinding Lights" is cached at hundreds of PoPs globally. The first person to stream it in Lagos triggers a fetch from origin; everyone after gets it from the Lagos PoP.

### CDN Cache Invalidation
```bash
# AWS CloudFront invalidation
aws cloudfront create-invalidation \
  --distribution-id E1234 \
  --paths "/images/*" "/css/main.css"
```

## 12. Resiliency: Introduction

### What is Resiliency?
The ability of a system to absorb failures and recover to normal operation, minimizing impact on users.

```
Fragile System: Failure -> System Down -> Users affected
Resilient System: Failure -> Degraded Mode -> Auto-recover -> Users barely notice
```

### Key Resiliency Concepts

| Concept | Definition |
| :--- | :--- |
| **Fault Tolerance** | System continues working despite component failures |
| **Graceful Degradation** | System offers reduced functionality instead of failing entirely |
| **Self-Healing** | System detects and corrects faults automatically |
| **Redundancy** | Duplicate components so failure of one doesn't cause outage |

### Resiliency vs. Reliability vs. Availability
- **Reliability** - probability that system works correctly over time
- **Availability** - percentage of time system is operational
- **Resiliency** - how well system handles and recovers from failure

```
Availability = Uptime / (Uptime + Downtime)

99%    = ~3.65 days downtime/year
99.9%  = ~8.7 hours downtime/year
99.99% = ~52 minutes downtime/year (four nines)
99.999% = ~5 minutes downtime/year  (five nines)
```

### Real-Life Scenario
> During the **2021 Facebook outage**, a configuration change caused all Facebook's data centers to withdraw their BGP routes. The entire system went down for ~6 hours. This was a resiliency failure — a single misconfiguration cascaded globally.

## 13. Designing for Resiliency

### Key Patterns

#### Circuit Breaker
Stops calling a failing service to give it time to recover - like an electrical circuit breaker.
```
States:
CLOSED    -> requests flow normally
OPEN      -> requests fail fast (no calls to broken service)
HALF-OPEN -> test if service recovered, then close or reopen

Failure threshold hit
CLOSED ------------------------> OPEN
  ^                               |
  |                               v
  |                        Timeout expires
  |                               |
  |                               v
  +--- success? ------ HALF-OPEN <-+
  |                      |
  +--- failure? ---------+
```

**Libraries:** Netflix Hystrix, Resilience4j, Polly (.NET)

### Retry with Exponential Backoff
```java
public <T> T callWithRetry(Callable<T> fn, int maxRetries) throws Exception {
    for (int attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return fn.call();
        } catch (TransientException e) {
            double wait = Math.pow(2, attempt) + Math.random(); // // jitter
            Thread.sleep((long)(wait * 1000));
        }
    }
    throw new MaxRetriesExceededException();
}
```
**Jitter** prevents the **thundering herd** problem where all retries hit the server simultaneously.

