# MVCC and Snapshot Isolation: How Databases Let Readers and Writers Coexist

**Date:** 2026-11-22  
**Domain:** DBMS  
**Level:** Intermediate → Advanced

## 1. Why MVCC exists

With a single lock held for every read and write, long readers can block writers and vice versa. Multi-Version Concurrency Control (MVCC) lets a database maintain multiple logical row versions. Readers select a version visible to their snapshot while concurrent transactions can create newer versions. Writes can still conflict, wait, or abort. MVCC is a concurrency-control technique—not an isolation level and not a guarantee of lock-free execution.

## 2. Versions and visibility

Imagine a row whose balance changed from 100 → 80 → 50. A transaction's snapshot determines which committed version it may see. A version is visible according to engine-specific transaction metadata and visibility rules; this is not necessarily a physical copy of every row.

- PostgreSQL stores tuple metadata and obsolete tuple versions that VACUUM eventually reclaims.
- InnoDB stores current records and undo information used to reconstruct older versions.
- Other engines use their own version chains, timestamps, transaction IDs, or storage mechanisms.

Don't assume one engine's implementation describes all MVCC databases.

## 3. Snapshot example

Initial state: `inventory(product_id=7, quantity=10)`.

- T1 begins and reads quantity = 10.
- T2 updates quantity to 8 and commits.
- T1 reads again.

Under transaction-level snapshot semantics, T1 may continue seeing 10. Under Read Committed, the second statement may see 8 because it gets a newer snapshot. Exact behavior depends on engine and isolation level.

Snapshots are logical views, not necessarily physical copies of all data.

## 4. Isolation levels are not synonyms for MVCC

| Level | Typical visibility | Common anomaly / nuance |
|---|---|---|
| Read Uncommitted | May permit dirty reads (some engines implement it as Read Committed) | Dirty reads |
| Read Committed | A committed snapshot per statement | Non-repeatable reads; some write-skew cases |
| Repeatable Read | Often transaction-level snapshot | May still permit serialization anomalies under snapshot isolation |
| Serializable | Behaves as if transactions executed in a serial order | Conflicting executions may block/abort; retry may be needed |

PostgreSQL Repeatable Read is snapshot isolation and prevents phantoms in its implementation, but can still allow serialization anomalies. MySQL InnoDB has its own consistent-read and locking-read behavior. Always verify engine-specific semantics.

## 5. Write skew: a subtle anomaly

Invariant: at least one doctor must remain on call. Alice and Bob are both on call.

- T1 reads both rows and sees two doctors; sets Alice off-call.
- T2 independently reads both rows; sets Bob off-call.
- The transactions update different rows and both commit.

Final state violates the invariant. Each decision was valid against its snapshot, but the combination is not.

Prevent it using:
1. Serializable isolation, with application retries for serialization failures.
2. Explicit locking of the shared decision rows before checking/updating; all code paths must follow the same lock protocol.
3. A database constraint or single-row representation that can enforce the invariant atomically, where possible.
4. An atomic conditional statement if the invariant can be expressed in one statement.

Locking only the row being changed may not protect a multi-row invariant.

## 6. MVCC does not eliminate locks

Locks remain necessary for write-write conflicts, explicit locking reads, schema changes, foreign-key checks, constraint enforcement, and coordination. A normal snapshot read may avoid blocking an updater, but concurrent updates to the same row may wait or conflict. A locking read is not equivalent to a plain snapshot read.

## 7. Version cleanup and long transactions

Old versions must remain while active snapshots may need them. Long-lived transactions can retain versions, leading to table/index bloat, cache pressure, cleanup overhead, and in some systems replication/recovery lag.

Operational habits:
- Don't leave transactions idle and open.
- Keep DB transactions short; don't hold them during slow external calls.
- Monitor vacuum, undo/history, and version-retention metrics for the engine.
- Space may become reusable without the physical file shrinking.

PostgreSQL uses VACUUM and visibility metadata; InnoDB manages undo/history and purge. These mechanisms differ.

## 8. Safer inventory decrement

The application-side SELECT → check → UPDATE sequence is vulnerable to races if multiple callers observe the same stock.

Prefer a conditional atomic update:

```sql
UPDATE inventory
SET quantity = quantity - :requested
WHERE product_id = :id
  AND quantity >= :requested;
```

Check affected rows: 1 means decrement succeeded; 0 means product absent or insufficient stock (distinguish with a follow-up query if needed). This protects the single-row condition. Multi-row invariants still need appropriate constraints, locks, or isolation.

## 9. Retry discipline

Concurrency-control mechanisms may abort transactions. Retry only known transient concurrency errors and only if replay is safe.

- Retry the entire transaction, not only the failed statement.
- Use bounded retries and exponential backoff with jitter.
- Avoid non-idempotent external side effects inside the transaction.
- Use idempotency keys or an outbox for side effects that follow commit.
- Record retry counts and conflict reasons.

Don't retry syntax, permissions, validation, or persistent constraint failures indiscriminately.

## 10. Interview checkpoints

1. What does MVCC improve, and what costs does it add?
2. Why might a stable snapshot not contain the latest commit?
3. Compare Read Committed with Repeatable Read snapshot behavior.
4. Why can snapshot isolation permit write skew but detect conflicting writes to the same row?
5. Why is “MVCC means no locks” incorrect?
6. What is the impact of a long-running transaction?
7. How would you enforce “at least one active member” across several rows?
8. What should the application do after a serialization failure?

## 11. Coding / design exercise

Design `reserve(productId, quantity, requestId)` with these requirements: stock never becomes negative; duplicate request IDs never reserve twice; concurrency is safe; responses distinguish duplicate from insufficient stock; reservation and idempotency record commit atomically.

Sketch using a transaction, unique constraint on requestId, conditional decrement, and an idempotency table. Explain a client timeout after the server commits and how retrying with the same key returns the original outcome.

## 12. Takeaways

- MVCC versions data and applies visibility rules to provide coherent reads.
- Snapshot semantics depend on isolation level and database engine.
- Snapshot isolation can allow write skew; protect invariants explicitly or use serializable isolation.
- MVCC still uses locks and incurs version cleanup costs.
- Keep transactions short and retries carefully bounded.

## References

- PostgreSQL: [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- PostgreSQL: [MVCC Introduction](https://www.postgresql.org/docs/current/mvcc-intro.html)
- PostgreSQL: [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- MySQL: [InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)
- MySQL: [InnoDB Multi-Versioning](https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html)
- Berenson et al.: [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/)
