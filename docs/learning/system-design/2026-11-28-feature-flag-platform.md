---
title: "Designing a Feature Flag Platform: Evaluation, Rollouts, and Safe Operations"
date: 2026-11-28
domain: LLD/HLD
level: Intermediate–Advanced
prerequisites:
  - REST APIs and basic distributed systems
  - Caching and hashing
  - Observability and deployment fundamentals
---

# Designing a Feature Flag Platform: Evaluation, Rollouts, and Safe Operations

**Domain:** LLD/HLD · **Level:** Intermediate–Advanced · **Date:** 2026-11-28

## 1. Why feature flags are more than `if` statements

A feature flag lets a deployed application decide at runtime which behavior to expose. This separates **deployment** (put code in production) from **release** (make behavior available to a chosen audience).

That distinction unlocks several workflows:

- **Progressive rollout:** expose a change to 1%, 5%, 25%, then 100% of users while observing metrics.
- **Kill switch:** disable an expensive or unhealthy feature without waiting for a new deployment.
- **Early access:** enable a feature for employees, beta users, or selected tenants.
- **Experimentation:** assign users to stable variants and compare outcomes.
- **Migration:** route traffic between old and new implementations while both coexist.

A flag also introduces a second source of runtime behavior. Every flag has a carrying cost: branches, tests, monitoring, configuration, and eventually cleanup. The goal is not to flag every small code change; it is to use flags where independent release control is valuable.

## 2. Separate the kinds of flags

Flag categories have different lifetimes and operational needs.

| Kind | Typical lifetime | Main use | Cleanup expectation |
|---|---|---|---|
| Release | Days/weeks | Hide incomplete code or decouple deploy from release | Remove after rollout |
| Experiment | Until experiment concludes | Stable cohort assignment and variants | Remove after decision |
| Operational | Short or long-lived | Degrade/disable risky functionality | Keep only intentional controls |
| Entitlement | Long-lived | Product/plan access | Treat as product policy |

**Do not use a feature flag as an authorization boundary.** Entitlement flags may shape the product experience, but permission checks must still be enforced by trusted authorization logic. Never put secrets or credentials in flag configuration.

## 3. Requirements for a production design

### Functional

1. Create flags with typed values (boolean, string, number, or small structured variants).
2. Configure flags independently for development, staging, and production.
3. Target contexts using attributes, explicit allow/deny lists, segments, and percentage rollouts.
4. Evaluate locally in the application with a safe default.
5. Publish configuration changes and expose audit history.
6. Preview rule outcomes and rollouts before publishing.
7. Disable a flag quickly and roll back configuration.

### Non-functional

- Flag evaluation should be local, predictable, and low-latency—typically no network round-trip per request.
- The SDK should continue operating during control-plane outages using a last-known-good configuration.
- Config changes should propagate within a bounded time, with a clear stale-data policy.
- Rule evaluation must be deterministic for a given flag version and context.
- Admin operations need authentication, authorization, validation, auditability, and rate limiting.
- The platform must avoid sending unnecessary personal data to the flag service.

## 4. High-level architecture

```text
                    CONTROL PLANE
 Admin UI / CLI
      |
      v
 API + Auth/RBAC + Validation
      |                    \\----> Audit log
      v
 Configuration DB
      |
      v
 Publish / Version service -----> Stream or polling endpoint
                                      |
                                      v
                                  SDK clients
                                  (local snapshot)
                                      |
 Request context -------------------->|
                                      v
                              Local evaluator
                                      |
                           flag value + reason
```

### Control plane

The control plane handles changes, not every application request:

- **Admin API:** create/update flags, targeting rules, rollout percentage, environment.
- **Validation:** type-check variations, validate operators and attributes, reject invalid or contradictory rules.
- **Persistence:** store the canonical configuration and version it.
- **Audit:** record who changed what, before/after values, timestamp, environment, and reason.
- **Distribution:** notify SDKs that a new version exists (streaming/SSE/WebSocket) or let them poll.

### Data plane

Each SDK maintains a local, immutable configuration snapshot:

1. Start with an embedded safe fallback or bootstrap configuration.
2. Fetch the latest snapshot and wait for the provider to become ready (or explicitly accept defaults).
3. Subscribe to change events or poll periodically.
4. Validate a received snapshot.
5. Atomically swap the active snapshot.
6. Evaluate flags in memory; do not call the control plane for each evaluation.

A snapshot is better than mutating individual rules in place: readers see either the old complete version or the new complete version, never a partially updated configuration.

## 5. Data model

A practical model separates a flag definition from environment-specific state.

```text
Flag
- key: string (stable, unique)
- type: BOOLEAN | STRING | NUMBER | JSON
- variations: [typed values]
- owner/team
- category: RELEASE | EXPERIMENT | OPS | ENTITLEMENT
- created_at, expires_at (optional)

EnvironmentFlag
- flag_key
- environment
- enabled
- default_variation
- rules: ordered list
- rollout: optional
- config_version

Rule
- id
- priority/order
- conditions: AND of clauses
- result: variation OR rollout

Clause
- attribute_path
- operator: EQ, IN, GT, CONTAINS, EXISTS, ...
- operand

Rollout
- targeting_key
- salt / allocation_key
- percentage per variation
```

Keep the rule language deliberately small. Arbitrary code in rules creates security, portability, debugging, and performance problems. Validate attribute types and support explicit behavior for missing/null attributes.

## 6. Evaluation algorithm: precedence must be explicit

For a boolean flag, one defensible evaluation order is:

1. **Flag disabled in this environment?** Return its configured off/default variation.
2. **Explicit exclusion?** Return off (or a designated safe variation).
3. **Explicit inclusion?** Return the included variation.
4. **Evaluate ordered rules:** the first matching rule wins.
5. **Rule's percentage rollout:** choose a stable variation using the context's targeting key.
6. **Fallthrough:** return the environment's default variation.

The actual order is a product decision, but it must be documented, consistent across SDKs, and testable. Explicit exclusions commonly override inclusion/rollout to make emergency controls unambiguous.

### Deterministic percentage assignment

Do **not** randomly select a user on every request. That would make one person alternate between old and new code and contaminate experiments.

Instead compute a stable bucket:

```text
bucket = HASH(flag_key + ":" + targeting_key + ":" + allocation_salt)
         mod 10,000

enabled if bucket < percentage * 100
```

For a 7.5% rollout, buckets 0–749 are enabled. The same flag and targeting key map to the same bucket on every evaluation.

- The **targeting key** should identify the subject consistently: user ID, account/tenant ID, or another chosen unit.
- Include a flag-specific salt/key so different flags usually select different cohorts.
- If related flags need the same cohort, deliberately share an allocation key.
- Use a stable, specified hash algorithm. Changing the algorithm or salt can reshuffle users.
- As a percentage increases, threshold-based buckets preserve the earlier cohort (e.g., 10% remains included when moving to 30%).

For multi-variation experiments, map the bucket to weighted ranges. Validate that weights sum to 100%, or define an explicit remainder policy.

## 7. Worked example: new checkout flow

Suppose we are rolling out `checkout-v2`:

- Default: `false`
- Environment: production
- Rule 1: internal employee cohort → `true`
- Rule 2: enterprise accounts in region `IN` → 100% `true`
- Fallthrough: 5% rollout → `true`, otherwise `false`

For a request with context:

```json
{
  "targetingKey": "user-8472",
  "accountTier": "standard",
  "region": "IN",
  "isEmployee": false
}
```

The employee rule doesn't match. The enterprise rule doesn't match. We evaluate the percentage rollout. Assume the deterministic bucket for `checkout-v2:user-8472` is 3,412. Since 5% corresponds to buckets 0–499, the flag is false for this user.

If the rollout increases to 20%, the bucket range becomes 0–1,999. This user remains off. Another user whose bucket is 1,234 changes to on and will consistently receive the new checkout on subsequent requests.

The key is that rollout percentage is a **cohort boundary**, not a fresh random decision.

## 8. Operational rollout workflow

A flag should have an owner, category, creation date, and (for temporary flags) an expiry/removal issue.

A safer release sequence:

1. **Deploy dark:** code is present but flag is off for everyone. Verify both code paths and rollback safety.
2. **Internal cohort:** turn on for employees/test accounts.
3. **Small stable cohort:** 1% or a carefully chosen low-risk group.
4. **Observe:** compare error rate, conversion, latency, resource usage, and dependency health against baseline.
5. **Ramp:** 5% → 25% → 50% → 100%, pausing at each step when metrics warrant.
6. **Rollback:** disable the flag or reduce rollout; confirm propagation and that the old path is still safe.
7. **Cleanup:** after full release and confidence, remove the old branch, flag config, tests that only cover the temporary toggle, and stale targeting.

For experiments, use a fixed assignment during the experiment and avoid changing the cohort allocation midway unless the experiment plan accounts for it.

## 9. Consistency, caching, and failure modes

### Push vs. poll

| Approach | Advantages | Costs / risks |
|---|---|---|
| Polling | Simple, easy to recover after missed events | Change propagation bounded by poll interval; repeated requests |
| Push/stream | Faster updates, less polling traffic | Connections, reconnects, missed events, operational complexity |
| Hybrid | Push invalidation + periodic full snapshot | More moving parts, often a practical balance |

A push event should generally carry a version or tell the SDK to fetch the latest snapshot. The client must not apply an older version after a newer one.

### Failure policy

- **Control-plane outage:** continue using the last known good snapshot.
- **SDK not initialized:** return a code-level default and expose a readiness/error signal. Do not silently pretend configuration is ready.
- **Malformed update:** reject the whole snapshot; keep the previous valid one.
- **Stale snapshot:** monitor age and decide per flag whether stale evaluation is acceptable. Most release flags can tolerate short staleness; a critical operational kill switch needs tighter propagation and an explicit mitigation path.
- **Network partitions:** no system can guarantee instant global propagation. Define the target (e.g., 99% of connected SDKs within a chosen interval) and alert when it is violated.

For a kill switch, consider whether SDKs should receive push updates, use a shorter poll interval, and/or have a separate emergency control path. Measure the time from operator action to effective disablement.

## 10. LLD: an evaluator that is testable

Keep the evaluator pure: it receives a validated snapshot, flag key, and context; it returns a value plus reason. It should not fetch data or mutate state.

```pseudo
evaluate(flag, context):
    if flag.disabled:
        return result(flag.offVariation, DISABLED)

    if matches(flag.exclusions, context):
        return result(flag.offVariation, EXCLUDED)

    if matches(flag.inclusions, context):
        return result(flag.includedVariation, TARGETED)

    for rule in flag.rules in priority_order:
        if rule.matches(context):
            if rule.rollout exists:
                variation = deterministicBucket(rule.rollout, context.targetingKey)
                return result(variation, RULE_ROLLOUT, rule.id)
            return result(rule.variation, RULE_MATCH, rule.id)

    return result(flag.fallthrough, FALLTHROUGH)
```

A production result should include metadata such as flag key, config version, reason code, matched rule ID, and provider status. Avoid logging full targeting context or sensitive attributes.

Useful LLD abstractions:

- `FlagProvider`: obtains/updates snapshots and reports readiness.
- `SnapshotStore`: atomic read/swap of immutable configuration.
- `Evaluator`: pure rule and rollout evaluation.
- `Context`: typed attributes + targeting key.
- `EvaluationResult`: typed value + reason + version.
- `FlagAdminService`: validation, persistence, authorization, audit, publish.

Don't over-engineer a generic rule engine at first. Add operators only when real use cases require them.

## 11. Testing strategy

Test the evaluator and distribution system separately.

### Evaluator tests

- disabled flag beats every targeting rule;
- exclusion beats inclusion/rollout;
- rule ordering is stable and first-match semantics work;
- missing or null attributes behave as documented;
- typed variation mismatches are rejected;
- same flag + key yields same bucket;
- different flags produce different cohorts unless allocation is shared;
- increasing percentage is monotonic;
- 0% and 100% boundaries are exact;
- invalid weights/config fail validation.

### SDK/config tests

- startup fallback and readiness behavior;
- snapshot update is atomic;
- out-of-order versions are ignored;
- reconnect fetches the latest full snapshot;
- malformed config leaves last-known-good snapshot intact;
- timeout/stale snapshot policy is followed;
- kill-switch propagation is measured;
- evaluation emits reason/version without PII.

### Integration and release tests

Use contract tests for the admin API and provider. Simulate a flag update while application instances are running. Test both code paths and rollback—not just the enabled path. Verify that a flag doesn't accidentally expose a client-side-only secret or bypass authorization.

## 12. Trade-offs and design choices

- **Local vs remote evaluation:** local is fast and resilient but requires config distribution and snapshot consistency; remote centralizes evaluation but adds latency, dependency failure, and per-request cost.
- **Polling vs streaming:** polling is simpler and more robust; streaming gives quicker changes but needs reconnect/version handling.
- **Simple booleans vs typed variations:** booleans are easy; variants support experiments but increase validation and code complexity.
- **Static vs dynamic targeting:** attribute/segment rules scale better than enormous per-user lists; direct targeting is useful for small exceptions but can become stale flag debt.
- **Fail-open vs fail-closed:** feature defaults should protect service availability, but the correct fallback is feature-specific. Neither is universally correct.
- **Control plane centralization:** one source of truth improves governance; regional replicas and local snapshots reduce latency and blast radius but complicate propagation.

## 13. Common pitfalls

1. Random assignment on every request—users flicker between variants.
2. Targeting key missing or unstable—rollout cohort changes between sessions.
3. Rules with unclear precedence—contradictory targeting becomes difficult to debug.
4. Calling the flag service in the request path—availability and latency become coupled to the control plane.
5. Treating a flag as authorization—client-controlled or stale flag values can expose protected actions.
6. Sending PII in targeting context—privacy, compliance, and data retention risks.
7. Never removing flags—permanent branches multiply test combinations and confuse future changes.
8. No owner/expiry—nobody knows whether a flag is safe to delete.
9. Testing only the new branch—rollback path may be broken.
10. Assuming instant propagation—SDKs can be disconnected; measure and define the bound.

## 14. Interview questions

1. Why should feature-flag evaluation usually be local rather than a network call?
2. How do you guarantee stable cohort assignment across requests?
3. What changes if the targeting key is a tenant instead of a user?
4. How do you handle a control-plane outage or invalid config update?
5. How would you design a kill switch whose propagation must be very fast?
6. Why is feature-flag state not an authorization mechanism?
7. How do you avoid all flags selecting the same 5% cohort?
8. What metrics would you watch during a rollout?
9. What are the consistency implications of a push-based config channel?
10. How would you reduce flag debt and avoid testing every combination of N flags?

## 15. Exercise

Design a feature-flag platform for an e-commerce service with 5 million daily users and 300 backend instances.

Requirements:
- An operator can disable recommendations within 10 seconds.
- Rollout is stable by user ID.
- Rules support country, account tier, and employee targeting.
- SDK evaluations add less than 1 ms in the hot path.
- A flag-service outage must not break checkout.
- Configuration changes are audited.

Deliver:
1. A component diagram and the control-plane/data-plane boundary.
2. The flag schema and rule precedence.
3. Your hash/bucket strategy and how you preserve cohorts during a ramp.
4. Polling/streaming choice, reconnect strategy, and version handling.
5. Fallback behavior for checkout vs. recommendations.
6. A rollout plan with the metrics and rollback thresholds you would choose.
7. Tests for the 10-second kill-switch objective and failure scenarios.

## References

- [Martin Fowler — Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html) — toggle categories, implementation and flag debt.
- [OpenFeature — Providers](https://openfeature.dev/docs/reference/concepts/provider/) — provider abstraction between application SDKs and flag systems.
- [OpenFeature — Evaluation Context](https://openfeature.dev/docs/reference/concepts/evaluation-context/) — context layering, targeting keys and PII considerations.
- [OpenFeature Specification — Flag Evaluation API](https://openfeature.dev/specification/sections/flag-evaluation/) — typed evaluation and defaults.
- [LaunchDarkly — Flag Evaluation Rules](https://github.com/launchdarkly/LaunchDarkly-Docs/blob/main/src/content/topics/sdk/concepts/flag-evaluation-rules.mdx) — ordered rule matching and fallthrough behavior.
- [LaunchDarkly — Deciding between flag targeting strategies](https://launchdarkly.com/docs/guides/flags/targeting-recommendations) — scalable attribute/segment targeting vs. individual targets.
