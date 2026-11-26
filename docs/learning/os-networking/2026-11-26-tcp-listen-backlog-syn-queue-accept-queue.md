# TCP Listen Backlog: SYN Queue, Accept Queue, and Connection Overload

**Date:** 2026-11-26  
**Domain:** Operating Systems & Computer Networks  
**Level:** Intermediate–Advanced  
**Prerequisites:** TCP three-way handshake, sockets, Linux process scheduling, basic networking

---

## 1. Why a server can complete TCP handshakes but still be overloaded

A TCP server does not receive a connection directly into application code the moment a client sends a SYN. The kernel participates in the three-way handshake and stages connections until the application calls `accept()`.

That staging area is a **listen backlog**. It is easy to misunderstand because Linux has distinct populations of connections waiting at different stages:

- **SYN queue (incomplete connections):** requests that have received a SYN and usually a SYN-ACK, but whose handshake has not yet been completed by the final ACK.
- **Accept queue (completed connections):** handshakes that are complete, but the application has not yet dequeued them with `accept()`.

These queues protect the application from short bursts, but they are not extra processing capacity. If the application cannot accept connections as fast as they arrive over a sustained period, queues fill, and clients may experience delayed connects, timeouts, or resets.

This is especially relevant for web servers, API gateways, RPC services, reverse proxies, database servers, and any service with a high rate of short-lived connections.

---

## 2. The lifecycle of an inbound connection

Assume client C connects to server S on port 8080.

### Three-way handshake and kernel queues

1. C sends **SYN**.
2. S's kernel creates a lightweight request state and sends **SYN-ACK**. The request is tracked as incomplete (commonly observed as `SYN-RECV`).
3. C sends the final **ACK**.
4. The kernel completes the connection and makes it eligible for the accept queue.
5. The server process calls `accept()`; the kernel removes one completed connection from the queue and returns a new file descriptor.

The listening file descriptor remains in `LISTEN` state. Each accepted client receives a separate connected socket/file descriptor.

### Conceptual flow

    Client                   Linux kernel                     Application
      | SYN ----------------->|                                  |
      |                       | create request state              |
      |<---------------- SYN-ACK                                  |
      | ACK ---------------->| complete handshake                |
      |                       | queue established socket          |
      |                       |                                  |
      |                       |<------------- accept() ------------|
      |                       | dequeue socket                    |
      |                       |-------------- new fd ------------>|
      |                       |                                  |

The important point: the application is not involved in each handshake packet. It becomes involved when it accepts the completed connection.

---

## 3. The two queues—and what they mean

### SYN queue

Contains incomplete handshakes. Entries consume kernel resources while waiting for the final ACK. Legitimate clients with high RTTs, packet loss, or delayed ACKs can occupy entries for longer. Spoofed-source SYN floods deliberately exploit this by causing SYN-ACKs to be sent to clients that never respond.

### Accept queue

Contains fully established sockets waiting for userspace to call `accept()`. A process can be delayed by CPU starvation, a long stop-the-world pause, overload, a blocked event loop, or an accept loop that is not scheduled often enough.

On Linux, since the 2.2 change, the `listen(fd, backlog)` argument primarily limits the completed-connection queue—not the incomplete SYN queue. The accept-queue limit is capped by `net.core.somaxconn`. The SYN queue has a separate system control, `net.ipv4.tcp_max_syn_backlog`, though exact behavior is kernel-version/configuration dependent and SYN cookies can change how state is retained.

**Don't assume every OS uses Linux's queue model.** BSD-derived stacks and other implementations may count backlog differently. Treat the syscall's documented semantics and the OS version as the source of truth.

---

## 4. What does the backlog parameter actually control?

Example:

    listen(server_fd, 512);

This requests a queue limit of 512 completed connections waiting for `accept()`. Linux silently caps the requested value at `net.core.somaxconn`. For example, if the app requests 8,192 but the host has `somaxconn=1,024`, the effective accept backlog is capped at 1,024.

The backlog is a **burst buffer**. It buys time for the application to catch up; it does not raise the sustainable accept rate.

### Queueing intuition

Let:

- `λ` = rate at which completed connections arrive at the accept queue (connections/sec)
- `μ` = rate at which the application accepts connections (connections/sec)
- `B` = available queue capacity

When `λ > μ` for sustained time, the queue grows at approximately `λ - μ`. A rough fill time is:

\[
t_{fill} \approx \frac{B}{\lambda-\mu}
\]

Example: completed connections arrive at 2,000/s; the service can accept 1,500/s; effective backlog capacity is 4,000.

\[
t_{fill} = \frac{4000}{2000-1500}=8\text{ seconds}
\]

So a larger backlog can absorb an 8-second burst in this scenario, but if the imbalance continues it will still overflow. The real fix is to increase accept capacity, reduce connection churn, or shed traffic upstream—not endlessly enlarge queues.

---

## 5. What happens when the queues fill?

### Accept queue full

The application is not draining established sockets quickly enough. Linux may drop an incoming SYN when the accept queue is already full. If a final ACK arrives for a handshake whose completed socket cannot be queued, the behavior depends on kernel settings and path; with the usual non-abort behavior, the server can defer completion and retransmit SYN-ACK, making the client retry. The optional `net.ipv4.tcp_abort_on_overflow` setting changes overflow behavior, but should not be changed casually.

Symptoms can be deceptive:

- The client may report `connect()` latency of roughly 1, 3, or 7 seconds—retransmission backoff can make delays appear in these steps.
- Some connection attempts time out even though the service is alive.
- The server may show no application-level error because the connection never reached the process.
- A momentary accept-loop stall can overflow a queue even if a later snapshot shows it empty.

### SYN queue pressure

If incomplete requests accumulate, the kernel can drop requests or use SYN cookies when configured. SYN cookies encode enough information in the SYN-ACK sequence number to validate the final ACK without keeping ordinary per-request state.

Cookies are a defensive fallback against SYN floods, **not a general capacity tuning mechanism**. The Linux documentation warns that cookies have protocol trade-offs and should not be used as a way to mask a legitimately overloaded server.

---

## 6. A worked production incident

Imagine an API server normally handles 600 new TCP connections/s. A deployment causes a CPU spike and the event loop is paused for 1.5 seconds. Clients continue to arrive at 1,000 connections/s.

During the pause:

- Completed handshakes accumulate in the accept queue.
- At a 512-connection effective backlog, the queue can fill in roughly 0.512 seconds if the full 1,000/s arrival rate reaches it.
- Further attempts are delayed or dropped; clients retry.
- After the event loop resumes, it drains the queue, but the retry wave adds load and can create a second spike.

The team sees elevated p99 connection-establishment latency and sporadic connect timeouts, but HTTP request metrics look normal for connections that made it into the application.

### Root-cause investigation

1. Check whether the listener's accept queue is full or near full.
2. Correlate overflow/drop counters with incident timestamps.
3. Inspect CPU saturation, event-loop stalls, thread scheduling, GC pauses, and accept-loop throughput.
4. Check whether the client uses connection pooling. If every request opens a new connection, connection churn amplifies accept pressure.
5. Fix the bottleneck; then tune backlog for the expected burst duration.

A larger backlog may reduce the symptom during short pauses, but it can also let a queue of stale connections build up and increase latency before failure.

---

## 7. Observe it on Linux

### Listener queue snapshot

    ss -lnt

For a specific port:

    ss -lnt 'sport = :8080'

On a LISTEN row, the columns are generally:

- **Recv-Q:** current completed connections waiting to be accepted.
- **Send-Q:** configured backlog limit for that listening socket.

Example:

    State   Recv-Q Send-Q Local Address:Port
    LISTEN  480    512    0.0.0.0:8080

This listener is close to its requested/effective backlog limit. Confirm whether it is a persistent pattern or just a snapshot.

### Incomplete handshakes

    ss -nt state syn-recv 'sport = :8080'

This shows sockets in SYN-RECV state, useful for inspecting incomplete handshakes (but not a perfect direct measure of queue internals across kernel versions).

### Overflow counters

    nstat -az TcpExtListenOverflows TcpExtListenDrops

These counters are generally host/network-stack-wide, not necessarily per listener. Compare deltas over time and correlate with socket-level evidence.

### Configuration

    sysctl net.core.somaxconn
    sysctl net.ipv4.tcp_max_syn_backlog
    sysctl net.ipv4.tcp_syncookies
    sysctl net.ipv4.tcp_abort_on_overflow

Also inspect the application’s actual backlog setting (e.g. server framework, Nginx, Java server, Go runtime, or container proxy). Increasing a kernel limit alone may not help if the application requests a smaller backlog.

---

## 8. Practical tuning and architecture choices

### 1. Ensure the app's backlog is intentional

Framework defaults vary. Verify what is passed to `listen()` instead of assuming a large system setting is effective.

### 2. Tune `somaxconn` for burst tolerance

Raise it only after evidence of accept-queue overflow and after estimating memory and queueing-latency consequences. The application backlog and kernel cap must both allow the intended value.

### 3. Tune SYN backlog separately

If incomplete handshake pressure is the issue, investigate `tcp_max_syn_backlog`, SYN-ACK retry behavior, traffic patterns, and SYN cookies. Do not confuse this with accept-queue saturation.

### 4. Improve accept throughput and reduce connection churn

- Keep the accept path short; hand off accepted sockets quickly.
- Use a suitable event-driven or worker architecture.
- Avoid doing expensive initialization synchronously before accepting more connections.
- Reuse connections (HTTP keep-alive, HTTP/2 multiplexing, connection pools) when appropriate.
- Use load balancing and admission control to shed overload rather than allowing unbounded queues.

### 5. Size queues from burst characteristics

A rough backlog estimate:

\[
B \ge (\lambda_{peak}-\mu)\times T_{burst}
\]

This is only an approximation. It assumes the accept service rate is stable and ignores retransmission feedback, per-connection resource cost, and queueing latency. Load-test under realistic bursts and pauses.

---

## 9. SYN cookies: what they solve and what they don't

A SYN flood aims to exhaust state associated with incomplete handshakes. With SYN cookies, the server can encode connection information into a cryptographically derived sequence number and defer allocation of ordinary request state until the final ACK returns.

**They help:** preserving the ability to complete new handshakes during SYN-queue pressure.

**They do not help:** a slow application that cannot call `accept()`. Completed connections still need an accept queue slot and userspace processing. A SYN-cookie warning can also indicate legitimate overload; inspect evidence before treating it as an attack.

---

## 10. Trade-offs

| Choice | Benefit | Cost / risk |
|---|---|---|
| Larger accept backlog | Absorbs short accept stalls | More queued sockets; delays visible failure; not more throughput |
| Larger SYN backlog | More incomplete handshakes can wait | More kernel state/memory during pressure |
| SYN cookies | Reduce state held for half-open requests | Protocol-option trade-offs; not an overload fix |
| Faster accept loop | Reduces queue buildup | May require architecture changes and careful handoff |
| Connection reuse | Fewer handshakes and accepts per request | Long-lived connections consume resources; load distribution can change |
| Aggressive reset on overflow | Fail quickly | Can turn transient overload into immediate client-visible failure |

---

## 11. Common pitfalls

1. **Assuming `listen(backlog)` is the SYN queue size.** Linux semantics changed; it primarily describes completed connections waiting for accept.
2. **Assuming backlog = throughput.** It is capacity to absorb a temporary mismatch, not processing speed.
3. **Tuning `somaxconn` without checking the application's requested backlog.** The smaller effective limit wins.
4. **Using SYN cookies to solve accept-queue overload.** Cookies protect incomplete-handshake state, not userspace's ability to accept.
5. **Reading one `ss` snapshot as definitive.** Queue spikes can be brief; use metrics/counters and time-series sampling.
6. **Treating global counters as listener-specific.** `ListenDrops` and `ListenOverflows` need correlation with per-socket evidence.
7. **Ignoring client retries.** Queue drops create retry storms that amplify load.
8. **Increasing backlog without measuring latency.** Bigger queues may turn a fast rejection into long waiting and timeout behavior.

---

## 12. Interview questions

1. What exactly happens between a TCP SYN and the application's `accept()` call?
2. What is the difference between the SYN queue and accept queue?
3. On modern Linux, what does `listen(fd, backlog)` control? What caps it?
4. Can a client's `connect()` return successfully before the server calls `accept()`? Explain.
5. What symptoms might a full accept queue cause at the client?
6. Why doesn't raising backlog solve sustained overload?
7. How do SYN cookies help, and why are they not a performance tuning tool?
8. Which commands and counters would you use to diagnose listen-queue overflow?
9. Why can a connection spike after a pause create a retry storm?
10. How would HTTP keep-alive or HTTP/2 change accept pressure?

---

## 13. Exercise: reproduce and diagnose queue saturation

In a disposable Linux VM or network namespace—not on a production host—build a small TCP listener that calls `listen(fd, 5)` and deliberately delays calling `accept()`.

1. Launch several clients that attempt to connect concurrently.
2. Observe `ss -lnt` while the listener is paused.
3. Resume the accept loop and observe the queue drain.
4. Record connect latency and compare it with `TcpExtListenOverflows` / `TcpExtListenDrops` deltas.
5. Increase the backlog, repeat, and explain why the experiment only delays overflow if accept capacity remains lower than arrival rate.
6. Add client-side connection reuse and compare new connections per second.

**Safety:** use a local lab or isolated namespace and modest client counts. Do not run a SYN-flood experiment against shared, public, or production infrastructure.

---

## 14. References

- [Linux man-pages: `listen(2)`](https://man7.org/linux/man-pages/man2/listen.2.html) — authoritative backlog semantics, `somaxconn` cap, and Linux history.
- [Linux man-pages: `tcp(7)`](https://man7.org/linux/man-pages/man7/tcp.7.html) — SYN backlog, SYN retries, and SYN-cookie behavior.
- [Linux Kernel Documentation: IP sysctls](https://docs.kernel.org/networking/ip-sysctl.html) — current kernel guidance for `tcp_syncookies` and related tuning.
- [Cloudflare: SYN packet handling in the wild](https://blog.cloudflare.com/syn-packet-handling-in-the-wild/) — practical two-queue model, `ss` and `nstat` diagnostics, and queue overflow behavior.
- [TCP Socket Listen: A Tale of Two Queues — Arthur Chiao](https://arthurchiao.art/blog/tcp-listen-a-tale-of-two-queues/) — detailed explanation of TCP listen queues and implementation differences.
- [Video: Linux Networking — How The Kernel Handles A TCP Connection](https://www.youtube.com/watch?v=ck4WvYM9V4c) — kernel-level packet and connection handling walkthrough.

---

## Key takeaway

**The listen backlog is a queue between the TCP stack and your application—not a throughput knob.** Understand which queue is filling, verify the effective limits, and improve the accept path or reduce connection churn. Use larger queues to absorb measured bursts, not to hide a sustained capacity problem.
