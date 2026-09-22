---
title: Distributed Rate Limiting with Redis
---
# Distributed Rate Limiting with Redis and Lua Scripting

## 1. Introduction

Rate limiting means controlling how many requests a user (or client) can make to an API in a given time. If the user crosses the limit, the server rejects the request with HTTP `429 Too Many Requests`.

Building an API rate limiter on a single server is simple. But enforcing a strict global rate limit across 50 server instances, without adding a lot of latency or race conditions, is a complex engineering challenge.

!!! note "The Basic Idea"
    Keep the rate limiting state in one shared place (Redis), and make the "check and update" step a single atomic operation (a Lua script).

The final flow will look like this:

`Request` → `App Server` → `Redis (Lua script)` → `Allow` or `Reject (429)`

---

## 2. The Problem: In-Memory Counters

### The Naive Approach

A developer uses a thread-safe `ConcurrentHashMap<String, Integer>` (in Java) or `std::unordered_map` with a `std::mutex` (in C++) on the application server to track requests per user IP.

### Why It Fails in a Distributed System

Modern microservices sit behind a Load Balancer. Suppose User A gets routed to Server 1 on the first request and to Server 2 on the second request. Now the in-memory state is siloed, because each server only knows about its own requests.

```text
User A → Load Balancer → Server 1 (count = 1)
User A → Load Balancer → Server 2 (count = 1)   ← Server 2 doesn't know about Server 1
```

So a user could bypass a "10 requests/minute" limit by making 50 requests, if they are load-balanced evenly across 5 different servers (each server allows 10).

### The Sticky Session Band-Aid

You could configure the load balancer to always route User A to Server 1 (Sticky Sessions). But this has its own problems:

* It destroys load distribution (hotspotting), because a heavy user always hits the same server.
* If Server 1 crashes, the user is moved to another server and the counter is lost, so their limit gets reset.

That is why it is considered an anti-pattern in modern stateless microservice architectures.

---

## 3. Core Algorithms: Token Bucket vs Sliding Window Log

To move the state out of the servers, we first need to agree on the algorithm which will run in our distributed cache.

### Token Bucket (The Industry Standard)

**Mechanics:**

* A bucket holds a maximum of $N$ tokens.
* Tokens are added to the bucket at a fixed rate $R$ (tokens per second).
* Every API request costs 1 token.
* If the bucket is empty, the request is dropped (HTTP 429).

!!! info
    We don't actually need a background process to refill the bucket. Instead, on every request we calculate how many tokens should have been added since the last request (`elapsed time x rate`). This is called a **lazy refill**, and our implementation below uses it.

**Pros:**

* Extremely memory efficient. It only needs to store 2 values per user: `tokens_left` and `last_refill_timestamp`.
* It handles traffic bursts elegantly. A user can burst up to $N$ requests at once, while the long-term average is still limited to $R$ per second.
* Stripe and Amazon API Gateway use this.

### Sliding Window Log (The High-Accuracy Alternative)

**Mechanics:**

* Instead of counting tokens, the system logs the exact Unix timestamp of every single request a user makes.
* To check if the limit is breached, it drops all timestamps older than the window (e.g. older than 1 minute ago) and counts the remaining logs.

**The Memory Flaw:**

If the limit is 10,000 requests per hour, you must store 10,000 timestamps per active user. Even at 8 bytes each, that is at least 80 KB per user (and a Redis sorted set uses more than the raw bytes). Multiply that by millions of users and you need tens or hundreds of GB of RAM just for rate limiting. Furthermore, removing old entries and counting the log on every request burns CPU cycles.

### Comparison

| Feature            | Token Bucket                      | Sliding Window Log                   |
| :----------------- | :-------------------------------- | :----------------------------------- |
| Memory per user    | Tiny (2 values)                   | Large (one entry per request)        |
| Accuracy           | Good                              | Very high (exact)                    |
| Burst handling     | Allows bursts up to bucket size   | No bursts beyond the limit           |
| Work per request   | Constant (O(1))                   | Cleanup + count of the log           |

---

## 4. The Distributed Race Condition

To solve the siloed state problem, we move the Token Bucket state to a centralized Redis cluster. But this introduces a severe concurrency bug: the **Read-Modify-Write Race Condition**.

Suppose User123 has `tokens = 5` and two requests arrive at almost the same time on different servers:

| Step | Server 1 (Thread A)      | Server 2 (Thread B)      | `tokens` in Redis |
| :--- | :----------------------- | :----------------------- | :---------------- |
| 1    | Reads `tokens = 5`       |                          | 5                 |
| 2    |                          | Reads `tokens = 5`       | 5                 |
| 3    | Calculates `5 - 1 = 4`   | Calculates `5 - 1 = 4`   | 5                 |
| 4    | Writes `tokens = 4`      |                          | 4                 |
| 5    |                          | Writes `tokens = 4`      | 4                 |

**The Result:** Two requests went through, but the token count only decreased by 1.

The problem is that "read, calculate, write" are three separate steps, and another request can sneak in between them.

---

## 5. The Solution: Atomicity via Redis Lua Scripting

### Why Not a Distributed Lock?

The first idea is to use a distributed lock (like Redlock) around the read-modify-write. But this is not a good fit here:

1. Acquire the lock (network call)
2. Read the data (network call)
3. Write the data (network call)
4. Release the lock (network call)

That is at least 4 network round-trips for *every single API call*. Even if one round-trip takes around 1 ms inside a data center, we are adding several milliseconds of latency to each request. Also, all the requests of a busy user have to wait for the same lock.

!!! tip
    Redis also has `WATCH` / `MULTI` / `EXEC` (optimistic locking), but under high contention the transaction fails and the client has to retry. A Lua script avoids this completely.

### The Redis Reality

Redis executes commands using a **single-threaded** event loop. It executes one command at a time.

!!! note
    Since Redis 6, extra threads can be used for network I/O (reading and writing sockets), but command execution is still done by one thread.

### Lua Scripting

Redis allows you to upload custom Lua scripts directly to the Redis server. Redis guarantees that the entire Lua script is executed **atomically**. No other Redis commands or scripts can run while your script is executing.

### Performance

By pushing the "Read-Modify-Write" logic directly into the Redis server, we avoid the extra network round-trips. The application server makes exactly one network call: "Execute this script."

`App Server` → `EVAL script` → `Redis runs read + calculate + write atomically` → `returns 1 or 0`

---

## 6. Practical Implementation (Java + Redis Lua)

Here is how we can implement a globally atomic Token Bucket in Java using the Jedis client.

```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

public class DistributedRateLimiter {
    // A pool is used because a single Jedis connection is not thread-safe
    private final JedisPool jedisPool;

    // The Lua script executed directly inside Redis.
    // KEYS[1] = bucket_key, ARGV[1] = capacity, ARGV[2] = refill_rate, ARGV[3] = current_time
    private static final String TOKEN_BUCKET_SCRIPT = """
        local bucket_key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        -- Read current state (a new bucket starts full)
        local last_tokens = tonumber(redis.call('HGET', bucket_key, 'tokens')) or capacity
        local last_refill = tonumber(redis.call('HGET', bucket_key, 'last_refill')) or now

        -- Calculate refills based on elapsed time (lazy refill)
        local elapsed_time = math.max(0, now - last_refill)
        local new_tokens = math.min(capacity, last_tokens + (elapsed_time * refill_rate))

        -- Evaluate limit
        if new_tokens >= 1 then
            redis.call('HSET', bucket_key, 'tokens', new_tokens - 1)
            redis.call('HSET', bucket_key, 'last_refill', now)
            redis.call('EXPIRE', bucket_key, math.ceil(capacity / refill_rate)) -- Cleanup
            return 1 -- Allowed
        else
            return 0 -- Blocked
        end
        """;

    public DistributedRateLimiter(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    public boolean isAllowed(String userId, int capacity, double tokensPerSecond) {
        String bucketKey = "rate_limit:" + userId;
        long currentTimeSeconds = System.currentTimeMillis() / 1000;

        // Only one network round-trip. Guaranteed atomic execution.
        try (Jedis jedis = jedisPool.getResource()) {
            Object result = jedis.eval(TOKEN_BUCKET_SCRIPT, 1, bucketKey,
                                       String.valueOf(capacity),
                                       String.valueOf(tokensPerSecond),
                                       String.valueOf(currentTimeSeconds));

            return Long.valueOf(1L).equals(result);
        }
    }
}
```

!!! note
    The multi-line string (`"""`) is a Java text block, available from Java 15. On older versions you can join the Lua lines with `+` instead.

### How the Script Works

1. Read the current `tokens` and `last_refill` of the user from a Redis hash. If the key doesn't exist, start with a full bucket.
2. Calculate how many tokens were refilled since the last request, and cap it at the bucket capacity.
3. If at least 1 token is available, consume it, save the new state, and return `1` (allowed).
4. Otherwise return `0` (blocked).
5. The `EXPIRE` removes the key of inactive users after the time needed to fill the bucket completely, so Redis doesn't keep old buckets forever.

---

## 7. Architecture Trade-offs and Flaws

### The Single Point of Failure (SPOF)

If your Redis cluster goes down, your API has to choose between two bad options:

* **Block all traffic** (fail closed): bad availability.
* **Allow all traffic** (fail open): can cause cascading failure to the databases behind the API.

This risk can be reduced by running Redis with replicas and automatic failover. Some systems also keep a rough local in-memory limiter as a fallback when Redis is not reachable.

### The NTP Clock Drift Flaw

Notice the `ARGV[3] = current_time` passed from the application server. In a distributed system, Server 1 and Server 2 will have slightly different system clocks due to Network Time Protocol (NTP) drift. If Server 1 is 5 seconds ahead of Server 2, passing the time from the application nodes will cause erratic token refilling (a fast clock gives extra tokens for free).

**The Fix:** Use Redis's internal `TIME` command inside the Lua script, so the source of truth for time is always the Redis node itself.

```lua
-- Replace ARGV[3] with Redis's own clock
local t = redis.call('TIME')
local now = tonumber(t[1]) + tonumber(t[2]) / 1000000  -- seconds with microsecond precision
```

!!! note
    Calling `TIME` inside a script and then writing data is allowed from Redis 5 onwards. It also gives us sub-second precision, which the `System.currentTimeMillis() / 1000` in our Java code doesn't.

### Long Scripts Block Redis

Since a script runs atomically, Redis cannot serve any other client while the script is running. So keep the script short and simple, like our token bucket which only does a few O(1) operations.

### Sending the Script Every Time

`EVAL` sends the whole script text on every call. In production we should load the script once (`SCRIPT LOAD`) and call it using its SHA1 hash (`EVALSHA`), so less data goes over the network.

---

## 8. Summary

Distributed rate limiting prevents systemic API collapse, but naive in-memory counters fail behind load balancers. The Token Bucket algorithm offers the best balance of memory efficiency and burst tolerance.

To implement this across many servers, we centralize the state in Redis. To overcome the Read-Modify-Write race condition without the latency penalty of distributed locks, we push the rate limiting logic directly into Redis via a Lua script. This uses Redis's single-threaded command execution to guarantee atomicity, with just one fast network call per request.

---

## Resources for Further Deep Diving

* **Article:** [Scaling your API with rate limiters (Stripe Engineering Blog)](https://stripe.com/blog/rate-limiters) - How Stripe enforces limits using Token Buckets and Redis.
* **Article:** [Design a Rate Limiter (ByteByteGo)](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter) - Explains the different rate limiting algorithms and their trade-offs.
* **Docs:** [Scripting with Lua (Redis Documentation)](https://redis.io/docs/latest/develop/programmability/eval-intro/) - How Redis executes Lua scripts atomically.
