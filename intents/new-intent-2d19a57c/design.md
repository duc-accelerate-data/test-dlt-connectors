# Design: Notion Ingestion Pipeline (abc_2)

## Progress

| Phase / Gate | Date | Notes |
|---|---|---|
| Phase 0 — Issue scope confirmation | 2026-05-16 | Intent classified as work/ingestion |
| Phase 1 — Workspace | 2026-05-16 | DuckDB sandbox scaffolded, dbt debug passed, dlt env verified |
| Phase 2 — Requirements | 2026-05-16 | Intent approved by user |
| Phase 3a — Plan skeleton + change-impact | 2026-05-16 | ✅ Complete |
| Phase 3b — Specialized design (discover) | 2026-05-16 | ✅ Complete: notion_databases resource selected |
| Phase 3 — Design approval | 2026-05-16 | ✅ Complete |
| Phase 4a — Generate (per artifact) | 2026-05-16 | ✅ Complete: pipeline.py generated, dry-run passed |
| Phase 4b — Unit tests | 2026-05-16 | ✅ Complete: 6/6 unit tests passing |
| Phase 4c — Data tests (with tier pick) | 2026-05-16 | ✅ Complete: Tier 1, 9/9 data tests passing |
| Phase 4d — Validation (fixture replay) | 2026-05-16 | N/A for ingestion |
| Phase 4d.5 — Audit | 2026-05-16 | ✅ Complete: All quality checks passed |
| Phase 4e — Contract authoring (pinning) | 2026-05-16 | ✅ Complete: Schema frozen (columns/data_type/tables) |
| Phase 4f — Code review | | |
| Phase 5a — Schema delta approval | | |
| Phase 5b — Documentation | | |
| Phase 5e — PR Workflow | | |

## Pipeline Inventory

**Source:** Notion (abc_2 connection)  
**Target:** DuckDB (schema: `src_abc_2`)  
**Pipeline:** `dlt/pipeline.py`

| Object | Target Table | Write Disposition | Incremental Cursor | schema_contract | Status | Notes |
|---|---|---|---|---|---|---|
| notion_databases | src_abc_2.<database_title> | replace | None | freeze/freeze/freeze | pinned | Dynamic: one table per Notion database. Table names derived from database titles at runtime. 3 databases loaded: tasks (10,000 rows), tasks_tracker (12 rows), untitled_2e982b21 (1 row) |

**Resource Details:**

- **notion_databases**: Source that auto-discovers all accessible Notion databases. Each database yields a separate table with the database's title as the table name. Primary key: `id`. Full refresh on each run.

**Schema Evolution:** Resources default to `evolve` contract until pinned in Phase 4e. Notion schema can change as users add/remove properties in databases.

**User Selection:** Databases only (notion_pages excluded per user preference).

## Change Impact

Ingestion-side change impact deferred to Phase 5a (schema delta approval).

## Artifact List

**To be generated:**
- `dlt/pipeline.py` (complete implementation with selected resources)
- `tests/test_notion_pipeline.py` (unit tests - Phase 4b)
- `tests/data/test_notion_data.py` (data tests - Phase 4c)
- `dlt/docs/*.yml` (resource schema documentation - Phase 5b)

## Design Notes

### Connection Details
- **Connection name:** abc_2
- **Connector:** notion (dlt-verified source)
- **Dataset name:** src_abc_2
- **Pipeline name:** abc_2_bronze
- **Auth:** OAuth via `.dlt/secrets.toml`

### Next Steps
1. Run `discovering-source-schema` to introspect available Notion resources
2. Select which resources to include in Pipeline Inventory
3. Define write disposition and incremental strategy per resource
4. Proceed to generation phase
