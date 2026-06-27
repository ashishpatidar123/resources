# System Design Concepts: A Comprehensive Guide

> A deep-dive into core system design concepts with real-world examples and scenarios.

## Table of Contents

1. [Scalability: Introduction](#1-scalability-introduction)
2. [Horizontal vs. Vertical Scaling](#2-horizontal-vs-vertical-scaling)
3. [Failover Strategies](#3-failover-strategies)
4. [Sharding Databases / NoSQL](#4-sharding-databases--nosql)
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
28. [SQL vs NoSQL — Comprehensive Comparison](#28-sql-vs-nosql--comprehensive-comparison)
29. [Database Indexes](#29-database-indexes)
30. [Proxy and Reverse Proxy](#30-proxy-and-reverse-proxy)
31. [Microservices vs Monolith](#31-microservices-vs-monolith)
32. [Real-time Communication](#32-real-time-communication)
33. [Distributed Transactions — SAGA and 2PC](#33-distributed-transactions--saga-and-2pc)
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
```javascript
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

#### Bulkhead Pattern
Isolate components so failure in one doesn't drain resources from others.

```
Thread Pool A (Payment Service)    -> max 20 threads
Thread Pool B (Recommendation)     -> max 10 threads
Thread Pool C (Search)             -> max 30 threads

If Recommendations floods -> only its pool is exhausted, others work fine
```

### How Cascading Failures Actually Happen - Thread Pool Exhaustion

This is the root mechanism behind most "one service took down the whole app" incidents. Interviewers want you to explain *why* it cascades, not just that it does.

```
Recommendation Service slows: 50ms -> 8 seconds response time
↓
Each in-flight request holds one app server thread open for 8 seconds
↓
100 concurrent users * 8 seconds = 800 thread-seconds consumed simultaneously
↓
App server thread pool (200 threads total) is completely exhausted
↓
New requests for Payment, Notifications, Search also need threads
↓
They queue up -> time out -> users get 500 errors
↓
Entire app appears down, even though Payment Service is perfectly healthy
```
**The Recommendation Service didn't crash — It held threads hostage.**

**The three-layer defence (must be used together):**
```
Layer 1 - Timeout
requests.get(url, timeout=0.5) # fail fast, don't wait 8 seconds
-> Prevents threads from being held hostage

Layer 2 - Bulkhead
Separate thread pool per downstream service
-> Even if Recommendations pool fills up, Payment pool is untouched

Layer 3 - Circuit Breaker
After N failures: OPEN circuit -> return default immediately, don't even call
After timeout: HALF-OPEN -> test if service recovered
-> Stops calling a broken service, giving it time to recover
```

> **Real-Life:** Amazon reported that every 100ms of extra latency costs ~1% in sales. A single slow dependency holding threads doesn't crash the system — it just slows everything down, which silently bleeds revenue. Circuit breakers + bulkheads prevent this.

### How to Think About Resiliency Design
```
For every external call your service makes, ask:
1. What happens if this call takes 10 seconds?     -> Add timeout
2. What if it fails 100 times in a row?             -> Add circuit breaker
3. What if it's slow for 1000 concurrent users?    -> Add bulkhead
4. What should users see when this service is down? -> Design fallback
   (show product page WITHOUT recommendations rather than failing entirely)
```

#### Timeout
Always set timeouts on external calls. Never wait forever.

```java
HttpClient client = HttpClient.newBuilder()
   .connectTimeout(Duration.ofSeconds(5))
   .build();

HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```
#### Health Checks & Liveness Probes
```yaml
# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3 # restart container after 3 failures
```

### Real-Life Scenario
> **Amazon's microservices** use circuit breakers extensively. If the "Recommendations" service is slow, circuit breakers trip and product pages render without recommendations rather than timing out for users. This is graceful degradation in action.
> **AWS Auto Scaling** + health checks is self-healing: if an EC2 instance fails its health check, it's terminated and replaced automatically.

## 14. Scaling Your Data: Introduction

### The Data Scaling Challenge
As applications grow, data management becomes the bottleneck:
```
10K users     -> Single PostgreSQL instance (fine)
1M users      -> Add read replicas, vertical scaling
10M users     -> Sharding, caching layers needed
1B users      -> Distributed databases, specialized stores per use case
```

### Read vs. Write Scaling

#### Read Replicas
```
         ┌─> Read Replica 1 (read queries)
App ──> Primary DB ──> binlog replication
         ├─> Read Replica 2 (read queries)
         └─> Read Replica 3 (analytics)
```

- Write goes to primary only
- Reads distributed across replicas
- **Replication lag** is a consideration (eventual consistency)

#### Write Scaling
- **Sharding** (split by key)
- **CQRS** (Command Query Responsibility Segregation) - separate read/write models
- **Event sourcing** - store events, not state

### Polyglot Persistence
Use different databases for different needs:

```
User Profiles    -> PostgreSQL (relational, ACID)
Session Data     -> Redis (fast, ephemeral)
Product Catalog  -> Elasticsearch (full-text search)
User Activity    -> Cassandra (time-series, high write)
Images/Videos    -> S3 (object storage)
Recommendations  -> Neo4j (graph relationships)
```

### Real-Life Scenario
> **LinkedIn** uses polyglot persistence: MySQL for member profiles, Espresso (their NoSQL) for messaging, Kafka for activity streams, Voldemort for key-value serving, and Samza for stream processing.

## 15. Distributed Storage Solutions

### Object Storage
Stores data as objects (file + metadata + unique ID). Infinitely scalable, cheap.

```
Use cases: Images, videos, backups, data lake files
Examples: AWS S3, Google Cloud Storage, Azure Blob Storage

aws s3 cp large-dataset.csv s3://my-data-lake/raw/2024/
```

### Distributed File Systems
Designed for large files, high throughput (not random access).

```
Examples: HDFS (Hadoop), Google File System (GFS), Ceph
Use cases: Big data processing, ML training datasets
```

### Distributed Block Storage
Replicated block devices for databases and VMs.

```
Examples: AWS EBS, Google Persistent Disk, Ceph RBD
Use cases: Database storage that needs low-latency random I/O
```

### Distributed Databases
See sharding section. Examples:
- **Cassandra** - wide-column, AP, peer-to-peer
- **CockroachDB** - distributed PostgreSQL, CP
- **Google Bigtable** - wide-column, petabyte scale
- **DynamoDB** - managed key-value + document, AP

### Comparison Table

| Solution | Best For | Latency | Scalability |
| :--- | :--- | :--- | :--- |
| **S3/Object Storage** | Large files, archives | ~50–200ms | Infinite |
| **HDFS** | Batch processing | High throughput | Petabytes |
| **Cassandra** | High-write time-series | ~1ms | Petabytes |
| **Redis** | Cache, sessions | <1ms | Tens of TB |
| **Elasticsearch** | Search, analytics | ~5ms | Petabytes |

### Real-Life Scenario
> **Dropbox** migrated away from S3 to their own distributed block storage called Magic Pocket. They store exabytes (1 EB = 1 million TB) of user files across custom hardware in their own data centers - saving ~75% in storage costs compared to S3.

> **Spotify** stores ~82 million songs. Each song exists in multiple formats/bitrates. They use Google Cloud Storage (object storage) for the audio files and their own distributed metadata store for song information.

---

## 16. HDFS Architecture

What is HDFS?
**Hadoop Distributed File System** - a distributed file system designed to store **very large files** (GBs to TBs) across commodity hardware.

Design principles:
- Files are split into large blocks (default: 128 MB)
- Each block is replicated across multiple nodes (default: 3 replicas)
- Optimized for streaming reads, not random access
- Write-once, read-many model

### Architecture

```
                  NameNode
    - Manages filesystem namespace
    - Tracks which blocks are on which DN
    - Stores metadata (no actual data)
                 |
                 v metadata ops
    +────────────┼────────────+
    |            |            |
    v            v            v
DataNode 1   DataNode 2   DataNode 3
Block A1     Block A2     Block A3
Block B2     Block B3     Block B1
Block C3     Block C1     Block C2
Data Nodes (store actual data blocks + replicas)
```

### Key Components

#### NameNode
- The **master** that manages the filesystem tree and metadata
- Knows which files exist, which blocks make up each file, where each block is stored
- **Single point of failure** -> mitigated by Secondary NameNode or HA NameNode

#### DataNodes
- Worker nodes that store actual data blocks
- Periodically send heartbeats to NameNode (every 3 seconds)
- If heartbeat stops -> NameNode marks the node as dead and re-replicates its blocks

#### Secondary NameNode
- NOT a hot standby - it periodically merges the NameNode's edit log to reduce restart time
- In modern Hadoop, replaced by NameNode HA with ZooKeeper

#### Block Replication
```
Default replication factor = 3
Placement strategy:
  Replica 1 -> Same rack as writer
  Replica 2 -> Different rack
  Replica 3 -> Same rack as Replica 2 (different node)

This balances:
  - Write performance (local write fast)
  - Rack failure tolerance (data survives rack failure)
```

### Read Path

```
1. Client asks NameNode: "Where are the blocks for /data/file.csv?"
2. NameNode returns block locations sorted by proximity
3. Client reads blocks directly from the nearest DataNode
4. Client assembles the file from blocks
```

### Write Path
```
1. Client asks NameNode to create /data/new_file.csv
2. NameNode assigns blocks and chooses DataNodes
3. Client writes to DN1 -> DN1 pipelines to DN2 -> DN2 to DN3
4. Acknowledgment flows back: DN3 -> DN2 -> DN1 -> Client
5. Client notifies NameNode of completion
```

### Real-Life Scenario
> **Yahoo** was one of the earliest large-scale HDFS users, running clusters with tens of thousands of machines storing hundreds of petabytes of web crawl data for their search engine.
> **Facebook** ran one of the largest HDFS clusters ever - over 100 petabytes storing user data, logs, and analytics. A 1 TB log file is split into ~8,000 blocks of 128 MB, spread across thousands of DataNodes.

### HDFS vs. S3

| Feature | HDFS | S3 |
| :--- | :--- | :--- |
| **Data locality** | Yes (compute near data) | No |
| **Latency** | Lower for local reads | Higher |
| **Cost** | Hardware + ops | Pay-per-use |
| **Scalability** | Cluster-limited | Infinite |
| **Management** | Complex | Managed |
| **Modern trend** | Being replaced by S3+Spark | Preferred for cloud |

---

## 17. RPO and RTO

### The Two Numbers That Define Every Failover SLA
Every business decision about database redundancy, backup strategy, and failover design comes down to two metrics.

| Metric | Full Name | Question It Answers |
| :--- | :--- | :--- |
| **RPO** | Recovery Point Objective | How much data loss is acceptable? |
| **RTO** | Recovery Time Objective | How long can the system be down? |

```
Timeline of a DB failure:
─────────────────────────────────────────────────────────────────────────────────────> time
   [Last backup]         [DB crashes]    [Failover complete]      [System restored]
       │                      │                      │                        │
       <───────── RPO ────────>                      <────────── RTO ─────────>
          (data loss window)                             (downtime window)
```

### Real-Life Mapping

| Business | RPO | RTO | Why |
| :--- | :--- | :--- | :--- |
| **Stock trading platform** | 0 seconds | < 5 seconds | Every second = millions in trades |
| **E-commerce checkout** | < 1 minute | < 1 minute | Lost orders, revenue impact |
| **Internal HR system** | 1 hour | 4 hours | Low urgency, people can wait |
| **Personal blog** | 24 hours | 24 hours | Some data loss is tolerable |

### How RPO Drives Replication Strategy

```
RPO = 0         -> Synchronous replication (write only confirmed when standby ACKed)
                   + Active-Active setup
RPO = seconds   -> Async replication + Kafka safety net
                   (Kafka retains events even if DB loses them -> replay on recovery)
RPO = minutes   -> Periodic snapshots (RDB for Redis, pg_dump for PostgreSQL)
RPO = hours     -> Nightly backups to S3
```

### How RTO Drives Architecture

```
RTO < 30 seconds -> Active-Active (traffic already on both nodes)
RTO < 5 minutes  -> Active-Passive with automated failover (AWS RDS Multi-AZ)
RTO < 1 hour     -> Manual failover with runbook
RTO = hours      -> Restore from backup (acceptable for non-critical systems)
```

### Real-Life Scenario
> **Netflix** targets RPO of near-zero and RTO of seconds using their Chaos Engineering practice (Netflix Chaos Monkey). They deliberately kill random instances in production to prove their system recovers automatically. If it doesn't, they fix it before a real outage.

> **A fintech startup's on-call incident:** Primary PostgreSQL dies at 02:00:00. Last standby sync was 01:59:54. RPO = 6 seconds. Those 6 seconds contained 3 payment confirmations that must be replayed from Kafka or manually reconciled with the payment gateway.

---

## 18. Split-Brain and Distributed Consensus

### What is Split-Brain?
When a primary DB fails and the standby is promoted, if the old primary later comes back online, you end up with two nodes both believing they are the primary - each accepting writes independently.

```
02:00 -> Primary (Node A) dies
02:01 -> Node B promoted to primary, new writes start flowing in
02:15 -> Node A restarts, still thinks IT is primary

Result — Two conflicting write histories:
Node A: payment #9001 = $500 deducted from Alice  <- stale branch
Node B: payment #9001 = $200 deducted from Bob    <- correct branch
Same ID, different data -> data corruption
```

### Why It Happens
In a partitioned network, both nodes may believe the other is dead (each can't reach the other), and both promote themselves. This is the classic network partition scenario in CAP.

### STONITH — "Shoot The Other Node In The Head"
The solution is to forcibly fence the old primary before promoting the standby:

```
1. Standby detects primary is unresponsive
2. Before promoting itself, standby sends a STONITH command:
   - Power off old primary via IPMI/BMC (bare metal)
   - Revoke old primary's network access via firewall rule
   - Force-stop the DB process via cloud API (AWS EC2 terminate)
3. Only after confirmed fencing -> standby promotes itself
```

This guarantees only ONE node can be primary at any time.

### Distributed Consensus (The Right Way)
Modern HA systems use distributed consensus algorithms (Raft, Paxos) so a leader is only elected when a majority of nodes agree. Tools like etcd and ZooKeeper provide this:

```
PostgreSQL HA with Patroni + etcd
=================================

       +--------------------+              +--------------------+
       |   Patroni Node A   |              |   Patroni Node B   |
       |  (Current Leader)  |              |  (Current Standby) |
       +---------+----------+              +---------+----------+
                 |                                   |
                 | Updates Lease                     | Watches Lease
                 v                                   v
       +--------------------------------------------------------+
       |                      etcd Cluster                      |
       |                   (Consensus Store)                    |
       +--------------------------------------------------------+

If Node A dies:
  -> etcd lease expires
  -> Node B acquires the lock (only after majority of etcd nodes agree)
  -> Node B promotes itself
  -> Node A, even if it comes back, cannot acquire the lock -> joins as replica
```

### Real-Life Scenario
> **PostgreSQL + Patroni (used by Zalando, GitLab, Notion):** Patroni uses etcd or Consul as the consensus store. When a failover happens, the old primary's Patroni agent detects it lost the etcd lock and immediately demotes itself to a replica — no STONITH needed because the old primary cooperates.
> **Redis Sentinel** uses a similar majority voting system — a new primary is only elected when the majority of sentinel processes agree the old primary is unreachable.

--- 

## 19. OLTP vs. OLAP

### The Full Picture

| Feature | OLTP | OLAP |
| :--- | :--- | :--- |
| **Full name** | Online Transaction Processing | Online Analytical Processing |
| **Query pattern** | Point queries (single row by ID) | Full scans, aggregations, GROUP BY |
| **Query size** | KB of data touched | GB to TB of data scanned |
| **Latency target** | Milliseconds | Seconds to minutes (acceptable) |
| **Concurrency** | Thousands of users simultaneously | Dozens of analysts |
| **Write pattern** | Frequent, small inserts/updates | Bulk loads (nightly/hourly) |
| **Index type** | B-tree (for row lookups) | Columnar (for aggregations) |
| **Examples** | PostgreSQL, MySQL, DynamoDB | Snowflake, Redshift, BigQuery |

### Why They Can't Share Infrastructure

```
OLTP query (your app):
SELECT * FROM orders WHERE id = 12345;  -> touches 1 row, uses index, done in 1ms

OLAP query (analyst):
SELECT country, SUM(revenue) FROM orders WHERE created_at > '2024-01-01' GROUP BY country; -> scans 300M rows, no useful index, 20 minutes
```

The OLAP query:
- Holds shared read locks -> blocks concurrent writes
- Saturates disk I/O -> all other queries slow down
- Fills connection pool -> app servers time out
- Causes: **user-facing 500 errors despite the DB being "up"**

### Columnar Storage — Why OLAP Warehouses Are Fast

Traditional row storage (OLTP):
```
Row 1: [id=1, name="Alice", country="US", revenue=500]
Row 2: [id=2, name="Bob", country="UK", revenue=200]
```

Columnar storage (OLAP):
```
id column:      [1, 2, 3, 4, ...]
country column: ["US", "UK", "US", ...]  <- only this column read for GROUP BY country
revenue column: [500, 200, 300, ...]     <- only this column read for SUM(revenue)
```

For `SUM(revenue) GROUP BY country`, columnar storage reads only 2 columns instead of all columns. For a 100-column table, this is a 50x I/O reduction.

### Real-Life Scenario
> **Airbnb** had a critical incident early on where a data analyst ran a complex reporting query directly on their production MySQL database. It triggered a full table scan that caused a cascading slowdown — booking requests started timing out at peak travel season. They resolved it by standing up a read replica dedicated to analytics, then eventually migrated to Apache Hive + Presto for true OLAP workloads.

---

## 20. Consistent Hashing

### The Problem with Simple Hash Sharding

```
6 keys distributed across 3 nodes: hash(key) % 3
   key_A -> hash % 3 = 0 -> Node 0
   key_B -> hash % 3 = 1 -> Node 1
   key_C -> hash % 3 = 2 -> Node 2

Now add Node 3 (4 nodes total): hash(key) % 4
   key_A -> hash % 4 = 3 -> Node 3 -> MOVED!
   key_B -> hash % 4 = 0 -> Node 0 -> MOVED!
   key_C -> hash % 4 = 2 -> Node 2 -> stayed

Result: ~75% of all keys need to move to a different node. On a system with 1TB of data, this triggers a massive migration while still serving traffic.
```

### How Consistent Hashing Works

Place both nodes and keys on a circular ring (hash space 0 -> 2^32):

```
       0
     /   \
Node C    Node A
(hash=90) (hash=10)
     \   /
    Node B
   (hash=50)

Key placement: walk clockwise from key's hash -> first node you hit owns it
key_X (hash=30) -> walks clockwise -> hits Node B (hash=50) -> stored on Node B
key_Y (hash=70) -> walks clockwise -> hits Node C (hash=90) -> stored on Node C
```

### Adding/Removing Nodes — Minimal Movement

```
Add Node D (hash=40) between Node B (50) and Node A (10):
Before: keys with hash 10-50 -> Node B
After:  keys with hash 10-40 -> Node D (MOVED)
        keys with hash 40-50 -> Node B (unchanged)

Only 1/N fraction of keys move. For 4 nodes -> only ~25% move instead of ~75%.
```

### Virtual Nodes (VNodes)
Real systems assign each physical node multiple positions on the ring to improve distribution:

```
Node A -> positions at hash: 10, 110, 210, 310  (4 virtual nodes)
Node B -> positions at hash: 50, 150, 250, 350
Node C -> positions at hash: 90, 190, 290, 390
```

This prevents one physical node from owning a disproportionately large slice.

### Real-Life Usage
- **Amazon DynamoDB** — consistent hashing for partition routing
- **Apache Cassandra** — each node owns a token range on the ring
- **Memcached client libraries** — distribute keys across cache nodes

### Real-Life Scenario
> **Discord** scaled their message storage to Cassandra using consistent hashing. When they added new Cassandra nodes to handle growth, the data automatically rebalanced — only the affected token ranges moved, not the entire dataset. Rebalancing happened live without downtime.

---

## 21. Fan-out Patterns

### What is Fan-out?
Fan-out describes how an event (e.g., a new post) is distributed to all interested parties (e.g., all followers). The strategy you choose has massive performance implications at scale.

#### Fan-out on Write (Push Model)
When a user posts, immediately write to the feed cache of every follower:

```
User A posts a photo
↓
Fan-out Service reads A's follower list (500 followers)
↓
For each follower: LPUSH feed:{follower_id} {post_id} -> Redis
↓
500 Redis writes happen asynchronously
When follower opens app -> reads pre-built feed instantly (O(1))
```

- ✅ Feed reads are instant — just fetch from Redis
- ✅ No computation at read time
- ❌ 1 post * 500 followers = 500 writes per post
- ❌ **Celebrity problem:** 1 post * 60M followers = 60M writes (hours of lag)

#### Fan-out on Read (Pull Model)
Don't pre-build feeds. When a user opens the app, query all followed accounts:

```
User opens feed
↓
Query: "Get latest 20 posts from each of my 500 followed accounts"
↓
500 queries -> merge -> sort by time -> return top 20
```

- ✅ No write amplification — 1 post = 1 write regardless of follower count
- ✅ Always fresh data
- ❌ Feed load is expensive — 500 queries merged at read time
- ❌ Cannot meet <200ms SLA at scale

### Hybrid Model (What Instagram/Twitter Actually Use)

```
Normal users (<1M followers)     -> Fan-out on WRITE
                                    Push post_id to each follower's Redis feed cache
Celebrities (>1M followers)    -> Fan-out on READ
                                    Don't push to anyone's cache
                                    Fetch celebrity posts at read time and merge

When user opens feed:
1. Fetch pre-built feed from Redis (fast, covers ~95% of posts)
2. Fetch latest N posts from celebrities they follow (small targeted queries)
3. Merge + rank -> return in <200ms
```

### What Gets Stored in the Feed Cache

```
Redis list per user: feed:{user_id}
-> Stores only post_ids (NOT full post content)
-> Max 1000 post_ids kept (LTRIM after every push)

LPUSH feed:user_456 post_id_789  # add new post
LTRIM feed:user_456 0 999        # keep only latest 1000

At read time:
1. Fetch post_ids from Redis feed list
2. Batch-fetch post details from Cassandra (parallel)
3. Batch-fetch images from CDN
```

### The Inactive User Problem
No point fan-out-writing to someone who hasn't opened the app in 6 months:

```
Before fan-out: check last_active_at for each follower
If inactive > 30 days -> skip the Redis write
On their next login -> rebuild feed on-demand (fan-out on read for that session)
```

### Real-Life Scenario
> **Twitter** historically used fan-out on write for most users. When Lady Gaga (90M+ followers) tweeted, her tweet was pushed to millions of Redis lists — causing notable spikes in their write infrastructure. They eventually moved to a hybrid model, treating accounts above a follower threshold differently.
> **Instagram** built a hybrid from early on. Kylie Jenner (400M followers) posting a photo does not trigger 400M Redis writes. Her followers see her posts because Instagram fetches her timeline at read time and merges it with their pre-built cache.

---

## 22. ID Generation Strategies

### Why Auto-Increment Fails at Scale

```
Single database auto-increment:
INSERT -> DB assigns ID -> works fine on one node

Sharded database:
Shard 1 auto-increment: 1, 2, 3, 4...
Shard 2 auto-increment: 1, 2, 3, 4...  <- ID collision!
You cannot use DB auto-increment across multiple shards.
```

### Strategy 1: UUID (Universally Unique Identifier)
```java
String id = UUID.randomUUID().toString(); // e.g., "550e8400-e29b-41d4-a716-446655440000"
```
- ✅ No coordination needed, generate anywhere
- ❌ 128-bit - large storage, bad for indexed DB columns
- ❌ Random — causes index fragmentation, poor cache locality
- ❌ Not sortable by time — can't tell creation order

### Strategy 2: Base62 Encoding of Auto-Increment

Used by URL shorteners (bit.ly, TinyURL):
```
Database auto-increment ID: 1,000,000
Base62 encode: 1000000 -> "4c92"
Characters: [0-9, a-z, A-Z] = 62 characters
Short, URL-safe, unique, no collisions
```
- ✅ Short (6-8 chars for billions of IDs)
- ✅ No collisions (single ID source)
- ❌ Single DB for ID generation = bottleneck at extreme scale

### Strategy 3: Twitter Snowflake ID (Most Production-Ready)
A 64-bit integer composed of:

```
1 bit   41 bits: Timestamp (ms)          10 bits: Machine ID   12 bits: Sequence
+-----+----------------------------------+---------------------+-------------------+
|  0  | 00000000000000000000000000000000 |     0000000000      |   000000000000    |
+-----+----------------------------------+---------------------+-------------------+
       (Years of custom epoch coverage)     (Up to 1024 nodes)   (4096 IDs per ms)

|___________________________________ 64-bit Integer _______________________________|
```
```java
long snowflakeId = (timestampMs << 22) | (machineId << 12) | sequence;
// Result: 7504288475836416L (64-bit long)
```

- ✅ Roughly time-sortable (chronological ordering for free)
- ✅ No coordination between machines needed
- ✅ 4096 IDs per millisecond per machine
- ✅ Compact — fits in a 64-bit integer (BIGINT in PostgreSQL)
- ❌ Requires clock synchronization (NTP drift can cause issues)

**Used by:** Twitter, Discord, Instagram, Mastodon

### Real-Life Scenario
> **Discord** uses Snowflake IDs for every message, channel, and server. The ID itself encodes the creation time — Discord's "jump to message" feature works by decoding the timestamp from the message ID to seek directly to that point in their Cassandra time-series storage.
> **URL shortener design:** Use a single auto-increment counter (PostgreSQL sequence) + Base62 encoding. At 10M URLs/day, a single Postgres sequence can handle the write rate fine. Only beyond ~1M inserts/second would you need Snowflake-style distributed ID generation.

---

## 23. Thundering Herd and Cache Stampede

### What is Thundering Herd?
When many processes/clients simultaneously attempt the same action after a trigger event, overwhelming a backend resource.

### Cache Stampede (the most common form)

```
Scenario: A popular product's cache entry expires at 12:00:00
12:00:01 -> 10,000 users request the product page simultaneously
        -> All 10,000 get a cache MISS at the same time
        -> All 10,000 queries hit the database simultaneously
        -> DB overwhelmed, latency spikes, potential outage
```

### Fix 1: Mutex / Probabilistic Early Expiration
Only allow one request to rebuild the cache; all others wait:

```java
public String getProduct(String productId) throws InterruptedException {
    String data = jedis.get("product:" + productId);
    if (data != null) return data;

    // Cache miss - acquire a lock so only ONE request rebuilds
    String acquired = jedis.set("lock:product:" + productId, "1", 
        SetParams.setParams().nx().ex(5));
    if ("OK".equals(acquired)) {
        data = db.query("SELECT * FROM products WHERE id=" + productId);
        jedis.setex("product:" + productId, 300, data);
        return data;
    } else {
        // Another request is rebuilding - wait briefly and retry
        Thread.sleep(100);
        return getProduct(productId);
    }
}
```

### Fix 2: Staggered TTLs (Jitter)
Don't set the same TTL for all keys — add random jitter so they don't all expire simultaneously:

```java
int baseTtl = 300; // 5 minutes
int jitter = new Random().nextInt(61); // 0-60 extra seconds
jedis.setex("product:" + productId, baseTtl + jitter, data);
// Keys now expire at: 300s, 312s, 348s, 301s... not all at 300s
```

### Fix 3: Background Refresh (Proactive Cache Warming)
Refresh the cache before it expires using a background job:

```java
// When TTL drops below 30 seconds, trigger async refresh
long ttl = jedis.ttl("product:" + productId);
if (ttl < 30) {
    executorService.submit(() -> refreshProductCache(productId));
}
return jedis.get("product:" + productId); // serve stale data while refreshing
```

### Thundering Herd in Retry Storms
Also happens when a service goes down and recovers — all clients retry simultaneously:

```
Service goes down -> all clients get errors -> all clients retry after 1 second
Service recovers -> 10,000 simultaneous requests hit it at once -> goes down again

Fix: Exponential backoff + jitter
retry_after = (2 ** attempt) + random.uniform(0, 1)
# attempt 1: ~2s, attempt 2: ~4s, attempt 3: ~8s (with random spread)
# Clients spread out their retries instead of thundering back in unison
```

### Real-Life Scenario
> **Reddit's front page** is a classic thundering herd target. The front page cache expires every few minutes. Without stampede protection, thousands of simultaneous requests would rebuild the same expensive query. Reddit uses a background job to proactively refresh the front page cache before it expires.

> **Any flash sale (Amazon Prime Day, Black Friday at midnight):** Product price/stock caches all need invalidation simultaneously when the sale starts. Without jitter in the new TTLs, a second stampede happens when all newly-cached "sale prices" expire at the same time.

---

## 24. Write-Ahead Log (WAL)

### What is a WAL?
A Write-Ahead Log is a durability mechanism where every change is written to an append-only log file on disk before it is applied to the actual data files.

```
Without WAL:
Write data to disk -> crash halfway -> data file is corrupt/incomplete

With WAL:
Write to WAL log (fast, sequential append) -> apply to data file -> crash?
On restart: replay WAL log -> data file is restored to consistent state
```

### Why "Write-Ahead"?
The log is written before (ahead of) the actual data modification. This guarantees:
- If crash during data file write -> WAL has the full intent -> can redo
- If crash during WAL write -> WAL is incomplete -> that transaction never happened -> safe

### How PostgreSQL Uses WAL

```
Client: BEGIN; UPDATE accounts SET balance=900 WHERE id=1; COMMIT;

Step 1: Write WAL record: "SET balance=900 for id=1 at LSN 0/1A2B3C" (fast sequential write to wal file)
Step 2: Update in-memory buffer (very fast)
Step 3: Acknowledge COMMIT to client -> client gets success here
Step 4: Eventually flush buffer to data file (background checkpoint)

Crash between Step 3 and 4?
-> On restart, replay WAL -> buffer is reconstructed -> data is safe
```

### WAL and Replication
PostgreSQL streaming replication works by shipping WAL to replicas:

```
Primary: writes WAL -> ships WAL stream to standby
Standby: receives WAL -> replays it -> stays in sync with primary

Replication lag = how far behind the standby's WAL position is vs primary's
```

### WAL in Other Systems

| System | WAL/Log Name | Purpose |
| :--- | :--- | :--- |
| **PostgreSQL** | WAL (Write-Ahead Log) | Durability + replication |
| **MySQL** | Redo Log + Binlog | Durability + replication |
| **Kafka** | Commit Log | The entire storage model is a log |
| **HDFS** | Edit Log | NameNode metadata changes |
| **Redis AOF** | Append-Only File | Durability (same concept) |
| **Cassandra** | Commit Log | Durability before memtable flush |

### Real-Life Scenario
> **Kafka** is essentially a WAL exposed as a messaging system. Every message is appended to a segment file on disk. Consumers read by offset (position in the log). This is why Kafka can replay messages — it never deletes them immediately, just like a WAL replays transactions on recovery.

> **PostgreSQL logical replication** (used by tools like Debezium for CDC) reads the WAL to capture every INSERT/UPDATE/DELETE and stream them to other systems (data lakes, Elasticsearch, Redis) in real time — turning the WAL into a change stream.

---

## 25. Load Balancers

### What is a Load Balancer?
A load balancer sits between clients and servers, distributing incoming requests across multiple backend instances to prevent any single server from becoming a bottleneck.

```
Clients -> [Load Balancer] -> Server 1
                           -> Server 2
                           -> Server 3
```

### L4 vs L7 Load Balancers

| Feature | L4 (Transport Layer) | L7 (Application Layer) |
| :--- | :--- | :--- |
| **Operates on** | TCP/UDP packets | HTTP/HTTPS content |
| **Routing based on** | IP + port | URL path, headers, cookies |
| **Can inspect content?** | No | Yes |
| **Speed** | Faster | Slightly slower |
| **Use case** | Any TCP traffic (DB, gRPC) | HTTP microservices |
| **Example** | AWS NLB, HAProxy TCP | AWS ALB, NGINX, Traefik |

### Load Balancing Algorithms

#### Round Robin
```
Request 1 -> Server A
Request 2 -> Server B
Request 3 -> Server C
Request 4 -> Server A (cycle repeats)
```
Simple, ignores server capacity/load. Best when servers are identical.

#### Weighted Round Robin
```
Server A (weight=3): gets 3 of every 5 requests
Server B (weight=2): gets 2 of every 5 requests
```
Use when servers have different capacities (e.g., 8-core vs 4-core).

#### Least Connections
Routes to the server with the fewest active connections.
```
Server A: 50 active connections
Server B: 12 active connections  <- next request goes here
Server C: 33 active connections
```
Best for long-lived connections (WebSockets, file uploads, video streaming).

#### IP Hash
```
hash(client_ip) % N -> always routes same client to same server
```
Provides **sticky sessions** without needing shared session storage.

### Sticky Sessions Problem and Fix
```
Problem: User logs in -> Server A stores session in its RAM
         Next request -> Load Balancer sends them to Server B -> "not logged in!"

Fix 1 (recommended): Store sessions externally in Redis
         -> Any server reads session from Redis -> no stickiness needed -> true stateless

Fix 2: IP Hash or cookie-based routing
         -> Always same user to same server -> breaks when server dies
```

> **Interview insight:** Always design for stateless app servers. Sticky sessions are a workaround that trades simplicity for fragility.

### How to Think About Load Balancers in an Interview
```
Interviewer asks: "How do you scale your API?"
Wrong: "I'll add more servers"
Right: "I'll add a load balancer (L7, least-connections) in front of 
       stateless app servers. Sessions go to Redis. Health checks
       remove unhealthy instances automatically."
```

### Real-Life Scenario
> **AWS ALB** routes /api/* to the API service containers, /static/* serves from S3 directly, and WebSocket upgrade requests route to a dedicated WebSocket server cluster - all configured on one load balancer with path-based routing rules.

> **NGINX upstream with least_conn:**
```nginx
upstream api_servers {
    least_conn;
    server api1.internal:8080;
    server api2.internal:8080;
    server api3.internal:8080;
}
```
---

## 26. Message Queues and Event-Driven Architecture

### What is a Message Queue?
A **durable buffer** that decouples producers (create work) from consumers (process work). Producer fires-and-forgets; consumer processes at its own rate.

```
Without queue (coupled):               With queue (decoupled):
  Producer -> Consumer                        Producer -> [Queue] -> Consumer
  (producer blocks waiting)                   (producer returns instantly)
  (consumer crash = data loss)                (consumer crash = message stays in queue)
```

### Why Use Message Queues?

| Problem | Queue Solution |
| :--- | :--- |
| **Consumer is slow** | Messages buffer; no data loss, no back-pressure on producer |
| **Consumer crashes** | Messages retained, reprocessed on restart |
| **Traffic spike** | Queue absorbs burst; consumer processes at steady rate |
| **Multiple consumers** | Same message consumed by many independent services |

### Kafka Architecture
The de-facto standard for high-throughput event streaming.

```
+------------+
       |  Producer  |
       +-----+------+
             |
             v
+--------------------------------------------------------+
| Topic: "orders"                                        |
|                                                        |
|  Partition 0:  [msg1] -> [msg4] -> [msg7] ...          |
|  Partition 1:  [msg2] -> [msg5] -> [msg8] ...          |
|  Partition 2:  [msg3] -> [msg6] -> [msg9] ...          |
+-------+--------------------------------+---------------+
        |                                |
        | Fan-out                        | Fan-out
        v                                v
+--------------------------+     +--------------------------+
| Consumer Group A         |     | Consumer Group B         |
| (Order Svc)              |     | (Analytics Svc)          |
|                          |     |                          |
|  [C0] reads Partition 0  |     |  [C0] reads Partition 0  |
|  [C1] reads Partition 1  |     |  [C1] reads Partition 1  |
|  [C2] reads Partition 2  |     |  [C2] reads Partition 2  |
+--------------------------+     +--------------------------+
```

### Key concepts:
- **Topic** - named stream of messages (like a DB table)
- **Partition** - unit of parallelism; one consumer per partition per group
- **Offset** - position of a message in a partition; consumers track their own
- **Consumer Group** - multiple services independently consume the same topic
- **Retention** - messages kept for configurable period (default 7 days) -> replay possible

### Kafka vs RabbitMQ

| Feature | Kafka | RabbitMQ |
| :--- | :--- | :--- |
| **Model** | Log-based (consumers read by offset) | Queue-based (deleted on ACK) |
| **Throughput** | Millions/sec | Thousands/sec |
| **Message replay** | Yes (retain by time/size) | No |
| **Consumer model** | Pull | Push |
| **Ordering guarantee** | Per partition | Per queue |
| **Best for** | Event streaming, CDC, analytics pipeline | Task queues, RPC, complex routing |

### Event-Driven Architecture
Services emit events; other services react - no direct coupling.

```
1. Synchronous (Coupled Architecture)
=====================================
[Place Order] ───(200ms)───> [Inventory Svc]
              ───(100ms)───> [Email Svc]
              ───(50ms)────> [Analytics Svc]
              
* Total Latency: ~350ms (Blocking)
* Blast Radius: High (If any service fails, the entire order fails)


2. Event-Driven (Decoupled Architecture)
========================================
[Place Order] ───( Emit "order.placed" )───> [ Message Broker / Kafka ]
                                                      │
                       ┌──────────────────────────────┼──────────────────────────────┐
                       ▼                              ▼                              ▼
              [Inventory Service]               [Email Service]             [Analytics Service]
             (Updates stock async)           (Sends receipt async)         (Records metrics async)

* Total Latency: <10ms (Non-blocking)
* Blast Radius: Low (If Email fails, the order is still safely processed)
```

### How to Think About Queues in an Interview
```
Should this be synchronous or async?
Needs immediate response to user? -> Synchronous (REST/gRPC)
Example: "Is this seat available?" -> must answer now

Result can be processed later? -> Async (message queue)
Example: "Send order confirmation email" -> user doesn't wait for this

Multiple services need the same event? -> Kafka topic (fan-out)
Example: "order.placed" -> inventory + email + analytics all consume it
```

### Real-Life Scenario
> **LinkedIn** processes over 7 trillion messages per day through Kafka. Every profile view, connection request, and job application generates events flowing to the analytics pipeline, notification service, and recommendation engine - all independently.
> **Uber** emits driver location updates to a Kafka topic every 3 seconds. The surge pricing service, the dispatch service, and the ETA calculator are all separate consumer groups reading the same topic at their own pace.

---

## 27. API Gateway and Rate Limiting

### What is an API Gateway?
A single entry point that sits in front of all microservices, handling **cross-cutting** concerns so individual services don't have to:

```
Client -> [API Gateway] -> User Service
                        -> Order Service
                        -> Payment Service
                        -> Product Service

Gateway handles:
✅ Authentication (JWT validation, OAuth)
✅ Rate Limiting (100 req/min per user)
✅ SSL Termination (HTTPS -> HTTP internally)
✅ Request Routing (path-based, header-based)
✅ Request/Response transformation
✅ Logging, tracing, metrics
```

### Rate Limiting Algorithms

#### Token Bucket (most common, recommended)
```
Bucket capacity: 10 tokens
Refill rate: 1 token/second

Each request consumes 1 token.
Bucket empty -> reject with 429 Too Many Requests.
Allows bursts (empty all 10 tokens at once) but limits sustained rate (max 1 req/sec long-term).
```

#### Leaky Bucket
```
Requests enter the bucket at any rate.
Bucket processes (leaks) data at a fixed rate (1 req/sec).
Overflow -> request dropped.
Smooths bursts -> output is always at a constant rate.
Best for: protecting downstream services from traffic spikes.
```

#### Fixed Window Counter
```
Window: 1 minute | Limit: 100 requests
Counter resets every minute.

Problem (boundary exploit):
100 requests at 00:59 + 100 requests at 01:00 = 200 in 2 seconds!
```

#### Sliding Window Log
```
Keep timestamps of all requests in the last N seconds.
On each request: remove old timestamps, count remaining.
Allow if count < Limit.
No boundary problem, but memory-heavy at scale.
```

### Implementing Rate Limiting with Redis
```java
public boolean isRateLimited(String userId, int Limit, int windowSeconds) {
    String key = "rate:" + userId;
    Long count = jedis.incr(key);          // atomic increment
    if (count == 1) {
        jedis.expire(key, windowSeconds);  // set TTL only on first request
    }
    return count > Limit;
}

if (isRateLimited(request.getUserId(), 100, 60)) {
    response.setStatus(429);
    response.setHeader("Retry-After", "60");
}
```

### How to Think About Rate Limiting in an Interview
```
Per user?       -> key = f"rate:{user_id}"
Per IP?         -> key = f"rate:{client_ip}"
Per API key?    -> key = f"rate:{api_key}"
Global?         -> key = "rate:global"

Which algorithm?
Need to allow bursts?       -> Token Bucket
Need smooth output rate?    -> Leaky Bucket
Simple implementation?      -> Fixed Window (accept boundary issue)
Strict accuracy?            -> Sliding Window Log
```

### Real-Life Scenario
> **GitHub API:** 5,000 requests/hour for authenticated users. Every response includes X-RateLimit-Remaining: 4999 and X-RateLimit-Reset: 1372700873. Implemented with token bucket per API token stored in Redis.
> **Stripe API:** Uses rate limiting at the API Gateway level. Exceeding limits returns 429 Too Many Requests with a Retry-After header. Behind the gateway, Stripe's microservices never see the rejected requests - gateway absorbs them.

---

## 28. SQL vs NoSQL — Comprehensive Comparison

### SQL (Relational Databases)
Data in tables with rows and columns. **Strict schema** enforced at write time (schema-on-write).

```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20),
    created_at TIMESTAMP 
);
```

**Strengths:** ACID transactions, powerful JOINs, strong consistency, mature tooling
**Weaknesses:** Schema migrations required, hard to shard horizontally, not ideal for nested/variable-shape data

### NoSQL Types

#### Key-Value (Redis, DynamoDB)
```
key: "user:1001:session"
value: '{"token": "abc123", "expires": 1719000000}'
Operations: GET, SET, DEL, EXPIRE
```
**Use for:** Sessions, caching, shopping cart, feature flags, leaderboards

#### Document (MongoDB, Firestore)
```json
{
  "_id": "order_123",
  "user": "alice",
  "items": [
    {"product": "laptop", "qty": 1, "price": 999},
    {"product": "mouse", "qty": 2, "price": 25}
  ],
  "address": { "city": "New York", "zip": "10001" }
}
```
**Use for:** Product catalogs, user profiles, CMS content - data with nested/variable structure

#### Column-Family (Cassandra, HBase)
```
Row key: "user_123"
Columns: "2024-01-15" -> {steps: 8000, calories: 400}
         "2024-01-16" -> {steps: 10000, calories: 500}
```
**Use for:** Time-series data, IoT sensors, activity logs - high write throughput + time-based queries

#### Graph (Neo4j, Amazon Neptune)
```
(Alice)-[FOLLOWS]->(Bob)
(Bob)-[LIKES]->(Post:123)

Query: "Friends of Alice who liked Post 123?"
-> Natural graph traversal, terrible in SQL (multiple self-joins)
```
**Use for:** Social networks, fraud detection, recommendation engines, knowledge graphs

### Decision Guide

```
Complex transactions + JOINs across tables?       -> PostgreSQL / MySQL
Scale writes horizontally across many nodes?       -> Cassandra / DynamoDB
Data structure varies per record?                  -> MongoDB
Time-series / high-write append workload?          -> Cassandra / InfluxDB
Relationship traversal (6 degrees of separation)? -> Neo4j
Fast key lookups + caching layer?                  -> Redis / DynamoDB
Full-text search?                                  -> Elasticsearch
Need ACID + horizontal scale globally?             -> CockroachDB / Google Spanner
```

### How to Think About SQL vs NoSQL in an Interview
```
Don't choose NoSQL just because it "scales better."
Ask:

1. Do I need transactions across multiple entities?
   YES -> SQL (or CockroachDB for distributed)
2. Is my data schema fixed and relational?
   YES -> SQL
3. Will I have very high write throughput (>100K writes/sec)?
   YES -> Consider Cassandra/DynamoDB
4. Is my data hierarchical/nested and schema varies per record?
   YES -> MongoDB
5. Do I have complex relationship traversals?
   YES -> Graph DB
```

### Real-Life Scenario
> **Airbnb polyglot setup:** MySQL for bookings and payments (ACID critical), Elasticsearch for property search (full-text + geo), Redis for session data and availability cache, Presto+S3 for analytics - each database chosen for what it does best.
> **Discord** migrated from MongoDB to Cassandra for messages because MongoDB couldn't handle their write throughput and data size (billions of messages). Cassandra's time-series model (channel_id + timestamp as partition key) was a natural fit.

---

## 29. Database Indexes

### What is an Index?
A data structure that speeds up data retrieval at the cost of extra storage and slightly slower writes.

```
Without index on email:
SELECT * FROM users WHERE email = 'alice@gmail.com'
-> Scans all 100M rows (45 seconds!)

With index on email:
B-tree lookup -> O(log n)
vs full scan -> O(n)
-> 8 milliseconds
```

### B-Tree Index (Default)
A balanced tree where each node contains sorted keys with pointers to data.
```
         [M]
        /   \
    [D,H]   [R,V]
   /  |  \  /  |  \
 [B] [F][J][P][T] [X]

Query: WHERE email = 'F@example.com'
Root [M] -> F < M -> left [D,H] -> D < F < H -> left [F] -> found in 3 steps
vs. full scan of millions of rows
```

**B-tree indexes work for:**
- Equality: WHERE email = 'x'
- Range: WHERE age BETWEEN 25 AND 35
- Sorting: ORDER BY created_at DESC
- Prefix: WHERE name LIKE 'Ali%'

### Composite Index
An index on multiple columns — column order matters critically.

```sql
CREATE INDEX idx_user_status ON orders(user_id, status);

-- Uses the index:
SELECT * FROM orders WHERE user_id=1 AND status='shipped';
SELECT * FROM orders WHERE user_id=1;       -- leftmost prefix works

-- Does NOT use the index:
SELECT * FROM orders WHERE status='shipped'; -- missing leftmost column!
```

**Rule:** Order composite index columns as: most selective first, then match your most common query pattern.

### Covering Index
An index that contains all columns a query needs - the DB never touches the actual table rows:

```sql
-- Query: SELECT user_id, status, created_at FROM orders WHERE user_id=1
CREATE INDEX idx_covering ON orders(user_id, status, created_at);
-- All data lives in the index -> zero table lookups -> extremely fast
```

### When NOT to Index

```
❌ Low cardinality columns (boolean, status with 2-3 values)
   Index on "is_active" (true/false): half the table is true -> index useless
❌ Tables with heavy writes, rare reads
   Every INSERT/UPDATE also writes to all indexes -> write overhead
❌ Small tables (< ~10,000 rows)
   Full scan is faster than index lookup + random I/O to fetch rows
❌ Columns never used in WHERE, JOIN, or ORDER BY
```

### The N+1 Query Problem (Index-Adjacent)
A common interview bug caused by missing a join + index:

```java
// BAD - N+1 queries (1 query for posts + 1 per post for user)
List<Post> posts = db.query("SELECT * FROM posts LIMIT 100");
for (Post post : posts) {
    User user = db.query("SELECT * FROM users WHERE id=" + post.getUserId());
}
// -> 101 database queries!

// GOOD - 1 query with join, leverages primary key index on users.id
List<PostWithUser> results = db.query(
    "SELECT posts.*, users.name " +
    "FROM posts " +
    "JOIN users ON posts.user_id = users.id " +
    "LIMIT 100"
);
// -> 1 query
```

### Real-Life Scenario
> **Slow query on 100M row users table:** SELECT * FROM users WHERE last_login < '2023-01-01' takes 45 seconds. Adding CREATE INDEX ON users(last_login) drops it to 8ms. One line of SQL, 5,625x faster.
> **Index bloat:** A high-write table with 12 indexes on it can be 3-4x slower on writes than without indexes. Rule: index the minimum set needed, remove unused indexes with pg_stat_user_indexes.

---

## 30. Proxy and Reverse Proxy

### Forward Proxy
Sits in front of clients — forwards requests to the internet on their behalf.

```
[Client A]┐
[Client B]┼─> [Forward Proxy] ──> Internet (destination sees proxy IP)
[Client C]┘
```

- Hides the client's IP from the destination server
- **Use cases:** Corporate firewalls, VPNs, geo-restriction bypass, content filtering

### Reverse Proxy
Sits in front of servers — receives client requests and forwards them to backend servers.

```
Internet ──> [Reverse Proxy] ┌──> Server 1
                             ├──> Server 2
                             └──> Server 3
            (destination sees proxy; client doesn't know about servers)
```

- Hides server infrastructure from the internet
- **Use cases:** Load balancing, SSL termination, caching, DDoS protection, WAF

### What a Reverse Proxy Handles

```
Client (HTTPS) -> Reverse Proxy -> Backend (HTTP, internal network)
                  ├── SSL termination        (decrypt once, not on every server)
                  ├── Static file serving    (serve CSS/JS/images directly)
                  ├── Gzip compression       (compress responses before sending)
                  ├── Request buffering      (protect slow app servers)
                  ├── Rate limiting          (per-IP or per-user)
                  ├── IP allow/blocklist
                  └── WebSocket upgrade handling
```

### Forward vs Reverse Proxy — One-Line Distinction
```
Forward proxy: "I'll make requests for you (client)" -> hides CLIENT
Reverse proxy: "I'll receive requests for you (server)" -> hides SERVERS
```

### Real-Life Scenario
> **Cloudflare** is a global reverse proxy — every HTTP request to example.com hits Cloudflare's nearest PoP first. Cloudflare handles DDoS protection, SSL, caching, and bot filtering before forwarding clean traffic to the origin server. The actual IP is never exposed.

> **NGINX** as reverse proxy + static file server:
```nginx
server {
    listen 443 ssl;
    
    location /static/ {
        root /var/www;
        expires 30d;           # serve directly, no app server involved
    }
    
    location /api/ {
        proxy_pass http://api_upstream;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 31. Microservices vs Monolith

### Monolith
All components deployed as a single unit. One codebase, one deployment, one database.

```
+--------------------------------------------+
|                MONOLITH                    |
|                                            |
|  [ Users ]       [ Orders ]                |
|                                            |
|  [ Payment ]     [ Notifications ]         |
+---------------------+----------------------+
                      |
                      | Single Deployment
                      v
            +-------------------+
            |   One Shared DB   |
            +-------------------+
```

**Pros:** Simple to build, test, debug, and deploy in early stages
**Cons:** Deploy everything for any change; can't scale one part independently; one bug can crash the whole app

### Microservices
Each component is a separate, independently deployable service with its own database.

```
Client -> API Gateway ├──> Order Service   ──> Orders DB (PostgreSQL)
                       ├──> Payment Service ──> Payments DB (PostgreSQL)
                       └──> Search Service  ──> Search DB (Elasticsearch)
```

**Pros:** Independent deployments; scale each service independently; teams own their service; polyglot tech stacks
**Cons:** Distributed systems complexity; network latency; data consistency across services harder; observability is harder

### When to Use Each

```
Start with a monolith when:
✔ Early-stage startup (ship fast, iterate faster)
✔ Small team (< 10 engineers)
✔ Domain not yet well understood
✔ Simple and uniform traffic patterns

Migrate to microservices when:
✔ Components have very different scaling needs
   (recommendations: 100K req/sec vs billing: 1K req/sec)
✔ Teams are large enough to own services independently
✔ Deployment cycle is becoming a bottleneck
✔ Different components need different languages or databases
```

### Service Communication

| Type | Protocol | When to Use |
| :--- | :--- | :--- |
| **Sync** | REST (HTTP/JSON) | External-facing APIs, simple internal calls |
| **Sync** | gRPC (binary) | High-performance internal service-to-service calls |
| **Async** | Kafka / RabbitMQ | Fire-and-forget, event-driven, high throughput |
| **Async** | Redis Pub/Sub | Real-time broadcast to multiple consumers |

### How to Think About This in an Interview
```
"Should we use microservices?"
Red flag answer: "Yes, microservices always scale better."
Good answer: "It depends on team size and traffic patterns. Start with a well-structured monolith. Extract services when a specific component's scaling requirements or deployment cadence diverge significantly."
```

### Real-Life Scenario
> **Amazon** decomposed its monolith in the early 2000s with Bezos's API mandate: every team must expose functionality only via APIs. Today thousands of microservices power Amazon.com. The shopping cart, pricing, recommendations, and inventory are all independent services.
> **Stack Overflow** runs a **monolith** serving millions of developers daily with a tiny ops team. Their argument: microservices add distributed systems complexity that is not worth it unless team size or scale genuinely demands it.

---

## 32. Real-time Communication

### The Four Options (in order of complexity)

#### HTTP Short Polling
```
Client: "Any new messages?" -> Server: "No" (repeats every N seconds)
Client: "Any new messages?" -> Server: "Yes" -> client gets data
```
- ✔ Trivially simple, works everywhere
- ❌ High server load even when nothing changed; data is always slightly stale

#### HTTP Long Polling
```
Client sends request -> Server holds connection open until data arrives ... 30 seconds pass... New message arrives -> Server responds -> connection closes
Client immediately opens a new request
```
- ✔ Near real-time, no wasted empty responses
- ❌ Each open connection holds a server thread; hard to scale beyond thousands

#### Server-Sent Events (SSE)
```
Client: GET /stream HTTP/1.1
Server: Content-Type: text/event-stream
        (keeps connection open, pushes as data becomes available)
Server: data: {"event": "new_message", "body": "Hello!"}
Server: data: {"event": "price_update", "symbol": "AAPL", "price": 213.5}
```

- ✔ Simple, native browser support, auto-reconnect built-in
- ✔ One persistent connection per client -> efficient
- ❌ One-directional only (server -> client)
- ✔ **Use for:** Live feeds, notifications, dashboards, activity streams

#### WebSockets
```
Client ─── HTTP Upgrade ───> Server
Client <─── full-duplex ───> Server (both sides can send at any time)
```

- ✔ True bidirectional, low latency (~50ms)
- ✔ Efficient - no HTTP headers per message after handshake
- ❌ Stateful (each connection is tied to one server instance)
- ❌ More complex to scale (needs sticky sessions or pub/sub for cross-server)
- ✔ **Use for:** Chat, multiplayer games, live trading, collaborative editing

### Quick Decision Guide
```
Server pushes updates, user only reads? -> SSE (simpler)
User sends and receives in real time?  -> WebSocket
Simplest possible, some latency ok?    -> Long polling
Legacy system, no real-time budget?   -> Short polling
```

### Scaling WebSockets (The Hard Part)
```
Problem: 1M concurrent WebSocket connections -> can't fit on one server. WebSocket state (connection) is on Server 1. User B's message to User A must reach Server 1.
Solution: Redis Pub/Sub as message bus between servers.
User A connected to Server 1
User B connected to Server 2
User B sends message: -> Server 2 PUBLISH to Redis channel "user:A:inbox" -> Server 1 is SUBSCRIBED -> receives message -> pushes to User A's WebSocket
```

### Real-Life Scenario
> **Slack** uses WebSockets for the real-time messaging experience. The "Alice is typing..." indicator is a WebSocket push event with debounce. Slack's WebSocket servers are stateful; Redis pub/sub routes messages between them so that users on different server instances still receive each other's messages.
> **Robinhood** (stock trading) pushes real-time price ticks over WebSockets. SSE wouldn't work here because the client also sends buy/sell orders over the same low-latency connection — true bidirectional communication is required.

---

## 33. Distributed Transactions — SAGA and 2PC

### The Problem
In microservices, one business operation spans multiple services with separate databases. Traditional ACID transactions only work within one database.

```
Place Order requires:
1. Deduct inventory   (Inventory Service DB)
2. Charge payment     (Payment Service DB)
3. Create shipment    (Shipping Service DB)
What if step 2 fails after step 1 succeeds? -> Inventory deducted, payment not charged -> inconsistent state!
```

### Two-Phase Commit (2PC)
A coordinator asks all participants to prepare, then signals all to commit atomically.

```
Phase 1 — Prepare:
Coordinator -> "Can you commit?" -> Inventory: "Yes (locks row)"
                                 -> Payment:   "Yes (locks row)"
                                 -> Shipping:  "Yes (locks row)"
Phase 2 — Commit (all said yes):
Coordinator -> "Commit!" -> all release locks and commit
Phase 2 — Rollback (any said no):
Coordinator -> "Rollback!" -> all undo their changes
```

**Problems with 2PC:**
- **Blocking:** If coordinator crashes after Phase 1, participants hold locks indefinitely
- **Latency:** Two synchronous round-trips across all services
- **Availability:** One participant down blocks the entire transaction (CP behavior)
- **Not practical at scale** beyond 3-4 services

### SAGA Pattern (Preferred for Microservices)
Break the transaction into a sequence of local transactions, each paired with a compensating transaction to undo it if a later step fails.

```
Order Saga:
Step 1: Deduct inventory   -> compensation: Restore inventory
Step 2: Charge payment     -> compensation: Issue refund
Step 3: Create shipment    -> compensation: Cancel shipment

Failure at Step 2 triggers compensations in reverse:
-> Run Step 1 compensation (restore inventory)
-> User sees: "Payment failed, order cancelled"
```

#### Choreography (Event-based, decentralized)
```
Order Service emits "order.created"
-> Inventory Service listens -> deducts -> emits "inventory.reserved"
-> Payment Service listens -> charges -> emits "payment.completed"
-> Shipping Service listens -> creates label
If Payment fails -> emits "payment.failed"
-> Inventory Service listens -> restores stock
```
✔ Simple, no central coordinator ❌ Hard to track overall saga state

#### Orchestration (Central coordinator)
```
  Order Orchestrator:
  1. Call Inventory Service -> success
  2. Call Payment Service   -> FAIL
  3. Call Inventory Service compensation (restore stock)
  4. Return failure to user
```
✔ Easier to track, audit, debug ❌ Orchestrator is a potential bottleneck

### How to Think About This in an Interview
```
"How do you handle a transaction across 3 microservices?"

Wrong: "I'd use a distributed database" (bypasses the architecture)
Wrong: "I'd use 2PC" (doesn't scale, blocking)
Right: "SAGA pattern with compensating transactions.
       For simple linear flows -> choreography via Kafka events.
       For complex conditional flows -> orchestration with a state machine.
       Key: design every operation to be idempotent so retries are safe."
```

### Real-Life Scenario
> **Uber trip creation is a SAGA:** reserve driver -> charge card -> create trip record. If payment fails after driver is reserved, a compensation saga releases the driver and the user sees "payment failed."
> **Amazon order placement:** Reserve inventory -> process payment -> notify warehouse -> ship. Each step has compensations. If payment fails, inventory is released. If warehouse can't fulfill, payment is refunded. AWS Step Functions is used to orchestrate these sagas.

---

## 34. Bloom Filters

### What is a Bloom Filter?
A **probabilistic data structure** that answers "Is this element in the set?" using very little memory.

```
Result: "Probably YES" or "Definitely NO"
False positive: Filter says "yes" but element isn't in set -> possible (tunable)
False negative: Filter says "no" but element IS in set -> NEVER happens

How It Works
A bit array + multiple hash functions:

Bit array: [0,0,0,0,0,0,0,0,0,0] (all zeros initially)

Add "alice@gmail.com":
  hash1("alice") % 10 = 3 -> set bit[3] = 1
  hash2("alice") % 10 = 7 -> set bit[7] = 1
  hash3("alice") % 10 = 1 -> set bit[1] = 1
  Array: [0,1,0,1,0,0,0,1,0,0]

Check "bob@gmail.com":
  hash1("bob") % 10 = 5 -> bit[5] = 0 -> DEFINITELY NOT in set (true negative)

Check "charlie@gmail.com":
  hash1 = 3 -> 1, hash2 = 7 -> 1, hash3 = 1 -> 1 -> all set -> "Probably YES"
  (but "charlie" was never added -> false positive!)
```

### Why It's Useful
```
Bloom filter: ~10 bits per element -> 1M entries = 1.25MB (near-zero memory)
HashSet:      64 bytes per element -> 1M entries = 64MB   (50x more memory)
```
With a 1% false positive rate, a Bloom filter uses ~9.6 bits per element regardless of how large the elements are.

### When to Use
- **Before an expensive DB lookup:** "Does this username exist?" -> check Bloom filter -> only query DB if probably yes
- **Web crawlers:** "Have I visited this URL?" -> filter saves re-crawling billions of URLs
- **Duplicate detection:** Check if event was already processed
- **Spell checkers:** Check if word is in dictionary

### Real-Life Usage
- **Cassandra** - bloom filters per SSTable to skip disk reads for non-existent keys
- **Google Chrome** - malicious URL list checked via bloom filter locally before full API call
- **PostgreSQL** - pg_partman uses bloom filters for partition pruning
- **Redis** - built-in BF.ADD / BF.EXISTS commands

### Real-Life Scenario
> **Cassandra read path:** When reading a key, Cassandra may need to check multiple SSTables on disk. A bloom filter sits in memory per SSTable. If the bloom filter says "definitely not here," the SSTable is skipped entirely - avoiding expensive disk I/O. At large scale this can eliminate 80%+ of disk reads for non-existent keys.

---

## 35. Service Discovery

### The Problem
In microservices, instances start and stop dynamically (auto-scaling, crashes, deployments). How does Service A find the current IP and port of Service B?

```
Without service discovery:
  User Service hardcodes: http://10.0.1.5:8080 (Payment Service)
  Payment Service restarts on a new IP: 10.0.1.9
  User Service breaks - it's still calling the old IP
```

### Client-Side Discovery
The client queries a service registry for the current list of healthy instances, then load-balances itself:

```
  User Service -> Service Registry: "Where are Payment Service instances?"
               -> ["10.0.1.5:8080", "10.0.1.6:8080"] (healthy ones only)
  User Service picks one (round-robin, random) -> calls it directly
```

**Tools:** Netflix Eureka, HashiCorp Consul
**Pros:** Client controls load balancing logic
**Cons:** Client library must implement discovery; language-specific

### Server-Side Discovery
Client calls a load balancer; the load balancer queries the registry:

```
  User Service -> Load Balancer ──► Service Registry = healthy instances
                       │           (picks one)
                       └─────────► forwards request
```

**Tools:** AWS ALB + ECS/EKS, Kubernetes Services
**Pros:** Client is simple - just calls a hostname
**Cons:** Load balancer is an extra hop

### Kubernetes - Built-In Service Discovery
Every Kubernetes Service gets a stable DNS name that automatically resolves to healthy pod IPs:

```
  Payment pods: 10.0.1.5:8080, 10.0.1.6:8080, 10.0.1.7:8080
  Kubernetes Service: "payment-service"
  DNS: payment-service.default.svc.cluster.local

  User Service calls: http://payment-service:8080
  Kubernetes DNS resolves -> load-balances across healthy pods automatically
  No external registry needed
```

### Health Checks and Deregistration
A service is only in the registry if it passes health checks:

```
  Service registers itself on startup:
    POST /register -> { name: "payment-svc", ip: "10.0.1.5", port: 8080 }

  Registry pings health endpoint every 30s:
    GET http://10.0.1.5:8080/health

  If 3 consecutive health checks fail -> deregister -> no new traffic routed to it
```

### Real-Life Scenario
> **Netflix Eureka:** Each microservice (Zuul, Ribbon, etc.) registers on startup and sends heartbeats every 30 seconds. Netflix's Ribbon client library reads from Eureka to get instance lists and performs client-side load balancing. When a host fails, Eureka stops receiving it within ~90 seconds (3 missed heartbeats).

> **HashiCorp Consul** is used at companies like Cloudflare and Lyft for service discovery + health checking + distributed configuration. Consul agents run on every host; the Consul server cluster maintains the service catalog using Raft consensus.

