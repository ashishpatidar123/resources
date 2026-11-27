# API Evolution: Contracts, Compatibility, and Safe Deprecation

**Date:** 2026-11-27  
**Domain:** Software Engineering  
**Level:** Intermediate–Advanced  
**Prerequisites:** REST fundamentals, semantic versioning, testing, deployment basics

## 1. Why API evolution is an engineering problem

An API is a contract between independently changing components. Mobile clients, partner integrations, internal services, and data pipelines can remain on different versions for months. The challenge is changing behavior while old consumers continue operating.

A robust strategy balances compatibility, clarity, operability, and security. Compatibility is multidimensional: wire shape, semantics, errors, timing, authorization, and side effects.

## 2. What counts as breaking?

Structural changes that can break consumers:
- Removing or renaming a field, endpoint, query parameter, or enum value.
- Changing optional fields to required.
- Changing response types or accepted formats.
- Tightening validation or changing pagination/sort behavior.

Often compatible, but not guaranteed:
- Adding a response field.
- Adding an optional request field.
- Adding an endpoint.

Strict JSON decoders, exhaustive enum switches, schema validators, and clients that reject unknown fields may break on additions. Compatibility must be tested against actual client behavior.

Semantic changes can be breaking despite identical schemas:
- A status now means "queued" rather than "completed".
- Retries create duplicates.
- Timestamps change interpretation or units.
- Sort order becomes unspecified.
- Timeout or authorization behavior changes.

Treat the contract as behavior—not merely OpenAPI.

## 3. Compatibility matrix

| Change | Old client → new server | New client → old server | Risk |
|---|---|---|---|
| Add optional response field | Usually okay | Client may assume present | Medium |
| Add optional request field | Old client omits it | Old server may reject/ignore | Medium |
| Remove response field | Client may fail | — | Breaking |
| Add enum value | Exhaustive old client may fail | New client sees only old values | Risky |
| Tighten validation | Existing calls may fail | — | Breaking |
| Change meaning, same type | Silent wrong behavior | Silent wrong behavior | High |
| Add endpoint | Usually safe | Old server returns 404 | Usually additive |

Compatibility is directional. Define whether you mean backward compatibility (new provider supports old consumers) or forward compatibility (new consumers tolerate old providers).

## 4. Design for evolution

### Prefer additive changes
1. Add a field or endpoint.
2. Make it optional and define stable defaults.
3. Deploy provider support first.
4. Observe behavior and adoption.
5. Update clients.
6. Remove old behavior only after migration evidence.

### Defaults are part of the contract
If omission meant false, don't silently change it to true. Document defaults, or require explicit values when ambiguity is harmful.

### Unknown values
Clients should handle unknown enum values safely: preserve raw values, map to UNKNOWN, or use a fallback. Avoid assuming the server will never add a status.

### Errors
Use stable machine-readable error codes, not client parsing of prose. Define validation details, retryability, and request/correlation IDs.

## 5. Worked example: synchronous order creation becomes asynchronous

Existing request:

    POST /v1/orders
    {"sku":"A123","quantity":2}

Existing response:

    {"orderId":"o-781","status":"created"}

Fulfillment now takes minutes.

**Unsafe change:** Return status=accepted but let existing clients interpret created as fulfilled. Schema remains unchanged, semantics break.

**Safer evolution:**
- Define a lifecycle with explicit processing and terminal states.
- Add a status resource: GET /v1/orders/{id}.
- Introduce an explicit asynchronous workflow, such as a documented 202 Accepted with Location.
- Preserve the existing behavior during transition or create a separately versioned operation if semantics cannot remain compatible.
- Add idempotency keys so retries don't create duplicate orders.
- Publish migration notes and monitor old-client traffic.

Example:

    HTTP/1.1 202 Accepted
    Location: /v1/orders/o-781

    {"orderId":"o-781","status":"processing","statusUrl":"/v1/orders/o-781"}

Define polling limits, terminal states, failures, retry rules, and lifecycle—not just the status code.

## 6. Versioning strategies

**URI versioning:** /v1/orders, /v2/orders  
Visible, easy to route/document; may encourage parallel implementations.

**Header/media-type versioning:** negotiate via Accept or custom header. Keeps URLs resource-oriented, but harder to inspect, cache, and debug.

**Additive evolution:** maintain one contract and deprecate gradually. Avoids version sprawl but demands discipline and consumer testing.

Choose based on consumer needs and migration capability. Don't introduce v2 for every small rename; don't force incompatible semantics into v1 merely to avoid versioning.

## 7. Deprecation is a migration

1. Inventory consumers through gateway logs, ownership metadata, SDKs, and service registries.
2. Announce what changes, why, replacement, deadline, and contact.
3. Provide examples, SDK updates, and migration guidance.
4. Measure usage by version and client; investigate unknown/long-tail consumers.
5. Warn via developer portal or response headers where useful.
6. Validate migrated clients with contract/integration tests.
7. Disable gradually using allowlists, canaries, then broad retirement.
8. Retain rollback until confidence is high.

Low aggregate traffic is not proof of no consumers—batch, seasonal, and rarely used clients matter.

## 8. Contract testing

- **Consumer-driven contracts:** consumer expectations are published and provider verifies them.
- **Provider tests:** validate provider behavior against agreed contracts.
- **Schema tests:** check OpenAPI changes for structural compatibility.
- **Integration tests:** cover semantics, auth, pagination, errors, retries, and side effects.

Avoid over-specification: assert only what a consumer depends on. Schema tooling catches shape changes but cannot prove semantic compatibility.

CI gate example:
- Diff OpenAPI documents.
- Flag removed/changed fields, requiredness, enum changes.
- Require review for breaking changes.
- Verify active consumer contracts.
- Generate changelog and migration notes.

## 9. Change review checklist

- [ ] Identify consumers, including older mobile and batch clients.
- [ ] Is the change additive?
- [ ] Are meaning, defaults, units, ordering, and errors unchanged?
- [ ] Can clients tolerate unknown fields and enum values?
- [ ] Are retries, idempotency, authorization, and side effects affected?
- [ ] Is rollout order safe (provider before consumer)?
- [ ] Are compatibility tests in CI?
- [ ] Are metrics tagged by API version/client?
- [ ] Is deprecation documented with migration steps and deadline?
- [ ] Is rollback possible?

## 10. Common pitfalls

1. Schema-only thinking: same JSON can hide a behavioral break.
2. Assuming additions are safe for strict decoders.
3. Deploying clients before provider support.
4. Vague errors that clients parse as text.
5. Version explosion and inconsistent parallel APIs.
6. Deprecation without usage data.
7. Silently changing defaults.
8. No idempotency strategy during migrations.
9. No ownership metadata to identify traffic.
10. Treating schema diff as a complete compatibility guarantee.

## 11. Interview questions

1. Define backward vs forward compatibility for HTTP APIs.
2. Why can adding an enum value break an old client?
3. Give an example of a same-schema breaking change.
4. URI vs media-type versioning: tradeoffs?
5. Design a safe synchronous-to-asynchronous order migration.
6. What metrics are required before retiring v1?
7. Consumer-driven contract tests vs integration tests?
8. How should clients handle unknown status and error codes?

## 12. Exercise

Design a migration for a payment API accepting amount, currency, and recipientId. It must add split payments, optional metadata, and a fraud-review status.

Deliver:
- Proposed additive contract.
- Compatibility matrix for old/new client and provider combinations.
- Rollout sequence (provider, SDK, clients, monitoring).
- Error, retry, and idempotency rules.
- Deprecation plan for anything removed.

Stretch: implement an OpenAPI compatibility CI gate with a reviewed exception process for deliberate breaking versions.

## 13. References

- [Google Cloud API Design Guide](https://cloud.google.com/apis/design) — resource-oriented design and API evolution.
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) — practical HTTP API standards.
- [Stripe API upgrades](https://docs.stripe.com/upgrades) — versioning and migration practices.
- [Pact documentation](https://docs.pact.io/) — consumer-driven contract testing.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — machine-readable API contracts.

## Key takeaway

An API contract includes semantics, errors, defaults, side effects, and timing—not just JSON. Evolve additively, validate with consumer contracts, and treat deprecation as a measured migration.
