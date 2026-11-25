# Leases, Failure Detection, and Fencing Tokens: Preventing Zombie Writers

**Date:** 2026-11-25  
**Domain:** Distributed Systems  
**Level:** Intermediate–Advanced  
**Prerequisites:** Distributed failure modes, consensus basics, concurrency control, atomic writes

## 1. Why this matters

A common design requirement is: *only one worker may update a resource at a time*. Examples include a scheduler running a job, a leader updating replicated metadata, a worker processing a customer's account, or a service rebuilding a cache.

A distributed lock or lease seems to solve this. But it only coordinates what the lock service believes. It cannot forcibly stop a client that has paused, lost connectivity, or whose request is delayed. A process may wake up after ownership has changed and still send a write—the **zombie/stale owner** problem.

This lesson develops a robust contract between a coordination service and the resource being protected.

## 2. Lock vs. lease vs. fencing

- **Lock:** an ownership grant intended to exclude competing actors. A distributed lock's guarantee depends on its protocol and assumptions.
- **Lease:** ownership with a time-to-live (TTL). The coordinator expires it if renewals stop, improving recovery from crashed clients.
- **Failure detector:** infers that a node may be unavailable from missing heartbeats/timeouts. In an asynchronous network, timeout is suspicion, not proof of death.
- **Fencing token:** a monotonically increasing generation number attached to each ownership grant. The protected resource rejects operations from older generations.

A lease is mainly a **liveness/recovery mechanism**. Fencing is a **safety mechanism** at the write boundary.

## 3. The stale-owner failure timeline

Suppose worker A receives a 10-second lease and token 41.

1. A reads a record and begins a calculation.
2. A is paused for 15 seconds (GC, VM suspension, CPU starvation, or network delay).
3. Its lease expires. The coordinator grants B a new lease with token 42.
4. B writes a newer result.
5. A resumes and sends its old write with token 41.

Without resource-side validation, A's late write can overwrite B's result—even if the lock service never granted both leases simultaneously. The coordinator cannot revoke A's CPU or retract an in-flight packet.

Checking the lease locally immediately before writing is insufficient: A may pause *after* the check. The check and protected write need an atomic enforcement point at the resource.

## 4. Fencing-token protocol

The invariant at the protected resource is:

> Once the resource has accepted token T, it must never accept a write carrying a token less than T.

### Granting ownership

The coordinator grants leases with increasing generations: 41, 42, 43, ...

Tokens must be monotonic for the resource's ownership domain and must not reset after coordinator restart. Ideally, token allocation is tied to a linearizable/consensus-backed operation, or uses a durable generation/epoch.

### Validating writes

The resource stores `highest_fence` (or a generation associated with the record). A write carries its token. The validation and update must be atomic:

```text
write(resource, token, payload):
  transaction:
    if token < resource.highest_fence:
       reject STALE_OWNER
    resource.highest_fence = max(resource.highest_fence, token)
    resource.payload = payload
    commit
```

Rejecting `token < highest_fence` allows equal-token writes from the same owner. If the protocol requires exactly one operation or strict sequencing, add a request sequence number or compare-and-set version. For a fencing-only guarantee, tokens order ownership epochs, not operations within an epoch.

A safe database implementation could lock the resource row and compare/update the fence in one transaction, or use a conditional update. Never read the fence, validate in application memory, and then write in a separate unprotected transaction.

## 5. Worked example

A batch job writes the latest report for account 900.

| Time | Actor | Action | Fence | Storage result |
|---|---|---|---:|---|
| 10:00:00 | A | Lease acquired | 41 | — |
| 10:00:01 | A | Begins calculation | 41 | — |
| 10:00:12 | B | Lease acquired after A expires | 42 | — |
| 10:00:13 | B | Writes report | 42 | Accept; highest=42 |
| 10:00:16 | A | Resumes and writes stale report | 41 | Reject (41 < 42) |

The token makes the order of ownership visible to storage. It does not rely on the old client noticing that its lease expired.

## 6. Where to put the fence

The check must live at the **actual side-effect boundary**:

- Database: include fence comparison and write in one transaction/conditional statement.
- Object storage: use a conditional write/version mechanism if available; otherwise route writes through a service that can enforce fencing.
- Message processing: include the generation in messages and validate it at the consumer or state store.
- External APIs: if the provider cannot check tokens, use idempotency keys, conditional requests, or a single controlled gateway; fencing alone cannot protect an uncooperative system.
- Multiple resources: all protected resources must enforce the token. A leader that fences its database writes but sends unguarded emails or payments can still create stale side effects.

## 7. Leases and renewal: practical design

A worker periodically renews its lease. If renewal fails or the worker cannot establish that it still owns the lease, it should stop initiating new protected work and fail closed. However, client-side step-down is defense in depth—not the correctness mechanism.

A rough configuration example:
- TTL: 15 seconds
- Renew every 5 seconds
- On renewal failure: immediately stop work; don't assume the lease remains valid
- Add jitter to renewal to avoid synchronized bursts
- Ensure the coordinator's clock/TTL implementation and client timeout assumptions are understood

Short TTLs speed recovery but increase false expiry during pauses or transient network trouble. Long TTLs reduce churn but delay takeover after a crash. Fencing prevents stale writes when ownership changes; it does not remove the need to choose TTLs carefully.

## 8. Leases are not clocks

Do not use wall-clock timestamps as fencing generations. Clock drift, NTP adjustments, pauses, and different clock domains can make timestamps go backward or overlap. A fencing token represents **ordering**, not elapsed time.

A monotonically increasing counter, consensus term, or resource-scoped epoch is more appropriate. If the resource accepts only the latest token, a delayed old request becomes harmless after a newer owner has made its first accepted write. Be aware: before the new owner reaches the resource, an old token may still be accepted. If immediate invalidation on takeover is required, the new owner must establish a fencing barrier at the resource before acting (e.g., write/advance the generation first).

## 9. Trade-offs and limitations

**Advantages**
- Protects against paused/zombie clients and delayed requests.
- Makes ownership transitions explicit at the data boundary.
- Can be implemented as a small, testable invariant.

**Costs**
- Requires protected storage to participate.
- Token generation and validation need durable, well-defined ordering.
- Tokens must be propagated through asynchronous work and retries.
- Every write path must be fenced; bypasses create holes.
- Does not deduplicate repeated requests from the same token; idempotency/sequence checks are separate.

**When a plain lock may be enough:** If lock loss only causes duplicate work (cache warming, redundant computation) and results are harmless, a lock may be an optimization. If stale writes can corrupt state, oversell inventory, or trigger irreversible actions, design the resource-side guard.

## 10. Implementation sketch (SQL)

Assume a row stores `highest_fence`. In a database supporting atomic conditional updates, a write can be expressed conceptually as:

```sql
UPDATE report
SET payload = :payload,
    highest_fence = :fence
WHERE id = :id
  AND highest_fence <= :fence;
```

Check the affected-row count. Zero rows means stale or missing resource. The statement is atomic, but ensure the schema initializes `highest_fence`, concurrent semantics are correct for your DB, and equal-token concurrent writes are acceptable (or add a version/request sequence).

A stronger ownership transition can first advance the fence, even before the new leader's business write. That establishes a barrier so the resource rejects all earlier generations immediately.

## 11. Common pitfalls

1. **"The TTL expired, so the old process is dead."** It may merely be paused or partitioned.
2. **Client-only validation.** A pause can occur between validation and write.
3. **Non-monotonic token source.** Random UUIDs identify grants but cannot order them; timestamps are unsafe unless the ordering authority guarantees monotonicity.
4. **Non-atomic check then write.** A race can slip between the two operations.
5. **Fence only one path.** Background jobs, admin scripts, retries, or alternate APIs may bypass it.
6. **Fence and idempotency conflated.** Token 42 may be valid for many operations; duplicate operation IDs still need deduplication.
7. **Fail-open renewal.** Continuing work after uncertain lease state increases stale-owner risk.
8. **No takeover barrier.** If new ownership is granted but storage hasn't observed the new token, a late old-token write may still pass. Advance the fence at the resource before new-owner side effects when strict takeover semantics are needed.

## 12. Interview questions

1. Why doesn't a distributed lock with TTL guarantee that only one client can write?
2. Why is checking lease validity immediately before the write not sufficient?
3. What is a fencing token? Where must it be validated?
4. How would you generate fencing tokens if the coordinator is replicated?
5. Does fencing solve duplicate requests? Why or why not?
6. What if the protected system is a third-party API that cannot validate tokens?
7. How would you test a stale-owner bug deterministically?
8. Compare short and long lease TTLs. What are the safety and availability implications?

## 13. Exercise

Implement a toy `LeaseCoordinator` and `FencedStore` in Java, C++, or Python.

Requirements:
- `acquire(resource, worker)` grants a lease and returns a monotonically increasing token.
- `renew(token)` fails if the lease is no longer current.
- `write(resource, token, value)` atomically rejects stale tokens.
- Simulate worker A pausing past expiry, worker B acquiring and writing, then A resuming.
- Add a test for delayed messages and another for two concurrent writes with the same token.
- Stretch: make takeover advance the storage fence before B's business write; explain what this changes.

The critical test should assert that after storage has accepted token 42, a write with token 41 cannot change the stored value.

## 14. References

- [Martin Kleppmann — How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) — the stale-client failure and fencing-token argument.
- [etcd — Lease API documentation](https://etcd.io/docs/v3.5/learning/api/) — TTL, keep-alives, and lease behavior.
- [etcd — Locking example with fencing](https://github.com/etcd-io/etcd/tree/main/contrib/lock) — runnable example demonstrating expired lease holders and token validation.
- [Engineering Foundry — Leases & Fencing Tokens](https://engineeringfoundry.dev/system-design/patterns/leases-and-fencing-tokens) — practical failure timeline and design trade-offs.
- [Video: When a Lease Expires, Fencing Stops the Stale Write](https://www.youtube.com/watch?v=9V45TIXtYGI) — visual explanation of the stale-worker scenario.

## Key takeaway

A lease can tell the coordinator that it is time to replace an owner. It cannot stop the old owner from waking up. **Correctness lives at the protected resource: attach an ordered fencing token to every write and atomically reject stale generations.**
