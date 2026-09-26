# Multi-Version Concurrency Control (MVCC)

## 1. Introduction

How do PostgreSQL and MySQL allow 10,000 users to read a row at the exact same time that 500 other users are trying to update it, all without the database crashing or grinding to a halt?

The secret is **Multi-Version Concurrency Control (MVCC)**. Let's break down why traditional locking struggles here, and how MVCC fixes it.

!!! note "The Basic Idea"
    Don't lock a row to update it. Instead, keep the old version around and insert a new version next to it, so readers can keep reading the old version while the write is happening.

---

## 2. The Problem: Pessimistic Locking

### The Architecture

Imagine you are building a banking app. User A is checking their balance (a read) while a direct deposit is updating their balance (a write) at the same time.

### The Naive Solution

You use a lock, for example a Read-Write Lock. When the direct deposit starts, it takes a write lock on the row. While that lock is held, User A (and anyone else) is blocked from reading the balance, because a write lock conflicts with a read lock.

### The Hardware Reality

This hurts performance. When a database thread has to wait on a lock, it gets put to sleep and another thread is scheduled in its place, which is a context switch. Every context switch has a cost, and it also disturbs the CPU cache, since the new thread's data usually isn't the data sitting in the cache anymore. If you have thousands of concurrent transactions all fighting over the same rows, a meaningful chunk of your CPU cycles go into putting threads to sleep and waking them up again, instead of doing actual work.

!!! warning
    In a pessimistic locking model, writers block readers, and readers block writers, for the same row. If someone runs a slow analytical query that takes 10 seconds to read a table, every update to that table can pile up in a queue behind it, exhausting your database connection pool and taking down your API.

---

## 3. The Solution: MVCC

To achieve high throughput, modern databases like PostgreSQL and MySQL's InnoDB engine follow a simple rule: **never overwrite data in place.**

### The Concept

Instead of locking a row to update it, the database inserts a brand new version of the row right next to the old one.

### The Analogy

Think of MVCC like Git. When you edit a file on a branch, you don't lock the `main` branch so nobody else can look at it. You just make a new commit. Other developers keep seeing the old version of the code until you finally merge your changes.

### The Result

A read query looks at a snapshot of the database as it stood at the moment the query started, so readers don't need to wait for writers to finish, and writers don't need to wait for readers to finish.

!!! info
    This mainly removes read-write blocking. Two writers updating the *same row* at the same time can still block each other, since only one of them can hold the row-level write lock at a time. What MVCC removes is readers having to wait on writers, and writers having to wait on readers.

---

## 4. Under the Hood: How Postgres Does This

Let's look at the physical disk layout of PostgreSQL to see how this works.

Every table in Postgres secretly carries a few hidden system columns on every row. The two most important are:

* `xmin`: the Transaction ID (TXID) that inserted this row version.
* `xmax`: the Transaction ID (TXID) that deleted or updated this row version (`0` by default, meaning it hasn't been touched).

### The UPDATE Illusion

When you run `UPDATE users SET balance = 100 WHERE id = 1;`, Postgres does not overwrite the row:

1. It finds the old row and sets its `xmax` to your current TXID (marking it as superseded).
2. It inserts a brand new row with the new balance of 100, setting its `xmin` to your current TXID.

```text
Before UPDATE:
  id=1, balance=50,  xmin=10, xmax=0

After UPDATE (by transaction 42):
  id=1, balance=50,  xmin=10, xmax=42   <- old version, now superseded
  id=1, balance=100, xmin=42, xmax=0    <- new version, currently live
```

### Visibility Rules

When another query reads the `users` table, the database engine compares the query's snapshot against the `xmin` and `xmax` of every row version. If a row was marked as deleted by a transaction that hadn't committed yet when the reading query's snapshot was taken, the database ignores that deletion and returns the old row instead.

!!! info
    This is more than just comparing transaction ID numbers. A snapshot in Postgres also tracks which transactions were still in progress when it was taken. That matters because a transaction's TXID being numerically smaller than yours doesn't tell you whether it actually committed, aborted, or is still running, and only a *committed* xmin makes a row visible. Section 5 simplifies this into plain number comparisons to keep the example approachable, but real Postgres also checks commit status via its commit log, not just TXID order.

---

## 5. Practical Code Example: Simulating MVCC in Java

To build intuition, here is a simplified Java class that mimics how a database might decide which version of a row to show a given transaction.

```java
public class MVCCDatabaseRow {
    public final long id;
    public final String data;

    // The hidden MVCC columns
    public final long xmin; // Transaction that created this version
    public long xmax;       // Transaction that deleted/replaced this version (0 if still live)

    public MVCCDatabaseRow(long id, String data, long xmin) {
        this.id = id;
        this.data = data;
        this.xmin = xmin;
        this.xmax = 0; // 0 means it hasn't been deleted or updated yet
    }

    /**
     * A simplified MVCC visibility check.
     * Determines if a specific transaction is allowed to see this row version,
     * assuming every transaction with a smaller TXID has already committed.
     */
    public boolean isVisibleTo(long currentTransactionId) {
        // Rule 1: Was this row created AFTER our transaction started?
        // If yes, we can't see it yet.
        if (this.xmin > currentTransactionId) {
            return false;
        }

        // Rule 2: Has this row been superseded (deleted or updated)?
        if (this.xmax != 0) {
            // Rule 3: Was it superseded BEFORE our transaction started?
            // If yes, it's dead to us.
            if (this.xmax <= currentTransactionId) {
                return false;
            }
            // If xmax > currentTransactionId, it was superseded by
            // something in our future, so for our snapshot it's still valid.
        }

        // If it passes the checks, this is the version we should read.
        return true;
    }
}
```

!!! note
    This example assumes every transaction with a smaller TXID has already committed, which keeps the logic easy to follow. Real Postgres cannot make that assumption: a transaction can also abort, and an aborted transaction's changes must never become visible, no matter what its TXID is. That's why a real snapshot also carries the list of transactions that were still in progress when it was taken, and checks each row's `xmin`/`xmax` against Postgres's commit log to see whether the relevant transaction actually committed.

---

## 6. The Trade-off: Table Bloat and VACUUM

You don't get this kind of concurrency for free.

### The Flaw (Dead Tuples)

If you run an `UPDATE` on a row a million times, you now have a million "dead" row versions sitting on disk. They are invisible to new transactions, but they still physically take up space.

### The Read Penalty

When you run a sequential scan (`SELECT * FROM users`, without an index), the database still has to physically read past all those dead versions to find the live one, which hurts your read throughput.

### The Fix: VACUUM

PostgreSQL relies on a background process called **VACUUM** (and its automatic counterpart, `autovacuum`). This process sweeps through the table's files, finds row versions whose `xmax` transaction has committed and is old enough that no active snapshot could still need them, and marks that space as reusable.

!!! note
    If your database has sustained, heavy write traffic, it can generate dead row versions faster than autovacuum can clean them up. This is called **table bloat**: your tables and indexes grow larger than the live data warrants, queries slow down, and disk usage keeps climbing. Left unmanaged for long enough, it can also block Postgres's transaction ID wraparound protection from running (this actually stops writes to protect data integrity, rather than causing a crash outright). Tuning autovacuum is a genuinely important skill for running Postgres at scale.

---

## 7. Summary

To handle heavy concurrent read and write traffic without constant thread locking, modern databases use Multi-Version Concurrency Control (MVCC). Instead of locking and overwriting data, the database treats row versions as mostly immutable: an `UPDATE` is really an `INSERT` of a new version alongside a soft-delete of the old one, using the hidden `xmin`/`xmax` transaction ID columns to mark which version applies when.

Each query gets a consistent snapshot of the database, so readers and writers can proceed at the same time without blocking each other on the same row. In exchange, the database pays a real cost in disk space, since old row versions have to be cleaned up by VACUUM before they pile up into table bloat.

---

## Resources

* **Article:** [How Postgres Makes Transactions Atomic (Brandur Leach)](https://brandur.org/postgres-atomicity) - Goes into the actual `xmin`/`xmax` fields at the source level, with real struct definitions from the Postgres codebase.
* **Article:** [Every UPDATE Leaves a Ghost: MVCC, Bloat, and VACUUM in PostgreSQL (PlanetScale)](https://planetscale.com/blog/postgresql-mvcc) - A practical walkthrough of how dead tuples accumulate and how VACUUM cleans them up.
