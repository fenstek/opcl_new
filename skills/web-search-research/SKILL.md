---
name: web-search-research
description: Perform web research through the local searxng service with source verification
---

Use this skill when an agent needs fresh external information.

Workflow:

1. Start with the local `searxng` search capability available on `opcl`.
2. Prefer primary sources, official documentation, vendor pages, and directly relevant publications.
3. Verify time-sensitive facts with explicit dates before answering.
4. Cross-check important claims across at least two sources when possible.
5. Return a concise summary with links, dates, and source notes.

Rules:

- distinguish facts from inference
- avoid relying on one low-quality source
- call out uncertainty when evidence is incomplete
- for product, policy, pricing, ranking, or trend claims, always note when the source was published
