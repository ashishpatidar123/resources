---
title: Consistent Hashing
---
# Consistent Hashing and Virtual Nodes

## 1. Introduction

If you are building an app with millions of users, a single Redis server will run out of RAM pretty fast. You have to split the data across multiple servers. But doing this the wrong way can take your whole system down the moment a server crashes or a new one is added.

!!! note "The Basic Idea"
    Don't decide a key's server using the *count* of servers (like `hash(key) % N`). Instead, place both the servers and the keys on the same ring, so that adding or removing a server only affects its nearby neighbors.

In this article we go through why naive hashing breaks, how the consistent hashing ring fixes it, and why virtual nodes are needed on top of it.

---

## 2. The Problem: Modulo Hashing

### How It Works

Let's say you have 4 Redis servers (Server 0, 1, 2, 3). You want to cache a user's profile. You take the `userId`, run it through a hash function to get a big number, and then use the modulo operator (`% 4`). If the result is `2`, you save the data on Server 2.

```text
server_index = hash(userId) % N
```

### The Analogy

Think of this like sorting playing cards into 4 buckets by dealing them out one by one. It works great and keeps the buckets perfectly even, as long as the number of buckets never changes.

### The Massive Flaw

What happens if Server 2 catches on fire and dies? You now have 3 servers, so your math changes to `hash(userId) % 3`.

* A key that used to map to Server 1 (`hash % 4 == 1`) might now map to Server 0 (`hash % 3 == 0`).
* A key that used to map to Server 3 might now map to Server 1.
* Since `% 4` and `% 3` are unrelated calculations, almost every single key ends up mapping to a different server, not just the keys that were on Server 2.

!!! info
    This isn't just a rough guess. Changing `N` in `hash(key) % N` causes roughly `(N-1)/N` of *all* keys to move, on average, not only the fraction that was on the removed server. For our 4-server example, that's about 75% of all keys.

When your app tries to read the cache, it gets a "miss" for most of its data. The app then panics and asks your main database (like PostgreSQL) for all that data at once. Your database gets hammered by a sudden flood of queries and can crash. This is called a **cache stampede**.

---

## 3. The Fix: The Consistent Hashing Ring

To fix this, we need a way to add or remove servers where only a small fraction of the data has to move. This is what **Consistent Hashing** gives us.

### The Ring Concept

Imagine a giant circle, or a clock face, representing all possible outputs of a hash function (for example, from `0` to `2^32 - 1`).

### Placing Servers

You take the IP addresses of your 4 servers, hash them, and place them on this ring. So Server A might land at 12 o'clock, Server B at 3, Server C at 6, and Server D at 9.

### Placing Data

When a user requests data, you hash their `userId` and find its spot on the same ring.

### The Routing Rule

To figure out which server holds the data, you walk clockwise around the ring from the data's position until you hit a server.

### Why This Works

If Server C (at 6 o'clock) crashes, the only data affected is the stuff between 3 o'clock and 6 o'clock. When the app looks for that data, it walks clockwise, skips the dead Server C, and lands on Server D instead. Only the data that belonged to Server C moves, and it all moves to Server D.

The rest of the ring — Servers A, B, and the data they hold — is completely untouched. No cache stampede.

```text
     A (12:00)
   /            \
 D (9:00)      B (3:00)
   \            /
     C (6:00) ✗  crashed → its data (3:00-6:00) moves to D
```

---

## 4. The New Flaw: Hotspots and Uneven Data

The ring sounds perfect, but hashing IP addresses is essentially random. What if your servers end up at 12 o'clock, 1 o'clock, 2 o'clock, and 3 o'clock?

Going clockwise, the server at 12 o'clock is now responsible for the entire gap from 3 o'clock all the way around back to 12, which is 9 out of 12 hours, or 75% of the ring. It gets slammed with 75% of the traffic, while the other three servers sit around mostly idle.

We call this a **hotspot**.

---

## 5. The Final Polish: Virtual Nodes (vNodes)

### The Trick

Instead of putting Server A on the ring just once, we put it on the ring 100 times, using different labels (for example `ServerA_1`, `ServerA_2`, and so on). We do this for every server.

### The Result

Now there are 400 "virtual" servers scattered randomly all over the ring. With enough virtual nodes, the law of large numbers takes over: the gaps between them average out to be roughly equal, and each physical server ends up owning a similar-sized share of the ring.

Virtual nodes also give us a flexible way to balance load based on actual hardware. If you add a powerful new server with lots of RAM, give it 200 virtual nodes so it handles more traffic. If a server is weak, give it 50.

!!! tip
    More virtual nodes per server give a more even distribution, but each vnode is one more entry to store and look up on the ring. In practice, somewhere between 100 and a few hundred virtual nodes per physical server is a common starting point; you can tune it based on how even the load looks in production.

---

## 6. Practical Implementation (Java)

In Java, we can implement the ring easily using a `TreeMap`. A `TreeMap` is built on a Red-Black tree, which keeps all the keys sorted in memory. It has a handy method called `ceilingEntry()`, which does exactly what we want: "find the next item greater than or equal to my current spot", and wraps around to the first entry if we've gone past the end.

```java
import java.util.Map;
import java.util.TreeMap;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class ConsistentHashRing {
    // The ring, storing the hash and the Server name
    private final TreeMap<Long, String> ring = new TreeMap<>();
    private final int virtualNodes;

    public ConsistentHashRing(int virtualNodes) {
        this.virtualNodes = virtualNodes;
    }

    // Add a server to the ring with virtual clones
    public void addServer(String serverName) {
        for (int i = 0; i < virtualNodes; i++) {
            long hash = getHash(serverName + "_vnode_" + i);
            ring.put(hash, serverName);
        }
    }

    // Remove a server and all of its virtual clones
    public void removeServer(String serverName) {
        for (int i = 0; i < virtualNodes; i++) {
            long hash = getHash(serverName + "_vnode_" + i);
            ring.remove(hash);
        }
    }

    // Find the right server for a given data key
    public String getServer(String dataKey) {
        if (ring.isEmpty()) return null;

        long hash = getHash(dataKey);

        // Find the next server clockwise on the ring
        Map.Entry<Long, String> entry = ring.ceilingEntry(hash);

        // If we went past the end of the ring, loop back to the first server
        if (entry == null) {
            entry = ring.firstEntry();
        }

        return entry.getValue();
    }

    // Helper: MD5 hash, folded down into a long
    private long getHash(String key) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(key.getBytes());
            // Use the first 8 bytes of the MD5 digest as a long
            long hash = 0;
            for (int i = 0; i < 8; i++) {
                hash = (hash << 8) | (digest[i] & 0xFF);
            }
            return hash;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5 not supported", e);
        }
    }
}
```

!!! note
    We're using `ceilingEntry()` directly here, which is simpler than searching a `tailMap()` for its first key — both approaches work, but `ceilingEntry()` says exactly what we mean: find the next key clockwise, or wrap around if none exists.

---

## 7. Trade-offs and Practical Considerations

### Choice of Hash Function

MD5 works fine for building the ring, and is common in reference implementations, but it is a cryptographic hash, which is slower than it needs to be for this job. Real systems often use a faster, non-cryptographic hash instead, like MurmurHash or FNV, since we only need a good spread of values here, not cryptographic security.

### Memory and Lookup Cost of the Ring

Every virtual node is one more entry in the `TreeMap`. With 10 physical servers and 200 virtual nodes each, that's 2,000 entries to hold in memory, and `ceilingEntry()` is an `O(log n)` lookup on top of that. This is usually a small cost, but it does grow with the number of virtual nodes and servers.

### Where This Is Used in Practice

Consistent hashing (with virtual nodes) isn't just a textbook idea. It is the technique behind how Amazon DynamoDB, Apache Cassandra, and several CDNs distribute data across their nodes, and it's also used by client libraries like the Ketama algorithm for Memcached.

---

## 8. Summary

Splitting data across multiple cache servers using simple modulo math (`hash(key) % N`) is risky, because adding or removing a server changes almost every key's target server, causing a flood of cache misses that can crash your database.

Consistent Hashing fixes this by mapping both servers and data onto the same circular ring, where a key simply goes to the next server it finds going clockwise. This means only the data belonging to a crashed (or newly added) server needs to move. To stop one unlucky server from taking all the traffic, we use Virtual Nodes: placing hundreds of clones of each server onto the ring, which evens out the load and lets us tune how much traffic a given physical server takes on.

---

## Resources for Further Deep Diving

* **Guide:** [Consistent Hashing Explained (ByteByteGo)](https://bytebytego.com/guides/consistent-hashing/) - Covers the rehashing problem, the ring, virtual nodes, and where the technique is used in the real world (DynamoDB, Cassandra, Discord, Akamai).
* **Article:** [Consistent Hashing (Eli Bendersky)](https://eli.thegreenplace.net/2025/consistent-hashing/) - A hands-on walkthrough with working Go code, including the same MD5-folding trick used above.
