---
name: google-search-console
description: Read Google Search Console properties and search analytics for approved sites
---

Use this skill when the user asks for Google Search Console data such as clicks,
impressions, CTR, positions, queries, pages, or SEO trends.

Approved properties:

- `sc-domain:tools.utildesk.de`
- `sc-domain:fensteco.de`

Workflow:

1. Use the `exec` tool with `host: gateway`.
2. Confirm access with:
   `python3 ~/.openclaw/credentials/gsc/gsc_query.py list-sites`
3. Run queries with:
   `python3 ~/.openclaw/credentials/gsc/gsc_query.py query --site sc-domain:tools.utildesk.de --days 28 --dimensions query --limit 20`
4. For page analysis, use `--dimensions page`.
5. Always report the exact date range used in the response.

Rules:

- Only use the approved properties listed above.
- Treat the credential file as secret and never print its contents.
- Summarize GSC data instead of dumping raw JSON unless the user explicitly asks for raw output.
