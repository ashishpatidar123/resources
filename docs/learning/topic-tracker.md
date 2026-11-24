
# Daily Engineering Learning — Topic Tracker

Canonical deduplication log. Before preparing each lesson, check this tracker and repository files. Avoid repeating the same topic or substantially overlapping treatment; choose a fresh subtopic or deeper progression.

## Covered lessons

| Date | Domain | Topic | Lesson |
|---|---|---|---|
| 2026-11-13 | Software Engineering | Secure CI/CD Architecture and Progressive Delivery | Previously reported as covered; file not located during repository inspection |
| 2026-11-22 | DBMS | MVCC and Snapshot Isolation: How Databases Let Readers and Writers Coexist | [Lesson](dbms/mvcc-and-snapshot-isolation.md) |
| 2026-11-23 | ML/AI | Probability Calibration: Making ML Confidence Trustworthy | [Lesson](ml-ai/probability-calibration.md) |
| 2026-11-24 | DSA | Rerooting DP on Trees: Compute Answers for Every Root in Linear Time | [Lesson](dsa/rerooting-dp-on-trees.md) |

## Weekly rotation
- Monday — ML/AI
- Tuesday — DSA
- Wednesday — Distributed Systems
- Thursday — Operating Systems & Computer Networks
- Friday — Software Engineering
- Saturday — LLD/HLD
- Sunday — DBMS

## Publishing protocol
- Use `docs/learning/<domain-slug>/<topic-slug>.md`; filenames are lowercase kebab-case and contain no dates.
- Domain folders: `ml-ai`, `dsa`, `distributed-systems`, `os-networking`, `software-engineering`, `system-design`, `dbms`.
- Include date, domain, level, and prerequisites in lesson metadata/body.
- Check this tracker and repository for duplicate topics before drafting.
- Lessons should include explanations, worked examples, trade-offs, pitfalls, interview questions, exercises, and authoritative references.
- Update this tracker, homepage, and MkDocs navigation after publishing.
- Preserve existing lesson content when reorganizing. No Obsidian or knowledge-graph content.
