# Intent: Notion Ingestion Pipeline (abc_2)

## Goal

Build an ingestion pipeline to extract data from Notion using the configured abc_2 connection and land it into DuckDB bronze tables. This establishes the raw data foundation for downstream analytics and reporting on Notion workspace content.

## Source System

**Notion** (via abc_2 connection configured in `.dlt/config.toml`)
- Connector: dlt-verified notion source
- Schema prefix: `src_abc_2`
- Authentication: OAuth (configured via `.dlt/secrets.toml`)

## Target

**DuckDB** 
- Database: `./data/prod.duckdb` (dev), `/Users/duc/Documents/accelerate_data/worktrees/feature/vd-1887-vd-1888-connector-search-and-resources/data/domains/vd1887-search-0516t105339/prod.duckdb` (prod)
- Schema: `main` (default)
- Tables will be prefixed per dlt convention with source name

## Objects in Scope

**To be determined** — which Notion databases, pages, or resources should be ingested.

Typical Notion resources available from dlt-verified connector:
- Databases
- Pages
- Blocks
- Users
- Comments

## Success Criteria

1. ✅ Bronze tables successfully landed in DuckDB with dlt metadata columns (`_dlt_id`, `_dlt_load_id`)
2. ✅ Tier 1 data tests passing:
   - `_dlt_id` is non-null on all tables
   - `_dlt_id` is unique on all tables
3. ✅ Pipeline runs without errors and can be re-executed idempotently
4. ✅ Schema contract pinned (freeze/freeze/freeze) to prevent drift
5. ✅ Documentation complete with source system details and incremental strategy

## Out of Scope

- Transformation work (staging models, marts, metrics)
- Data quality rules beyond Tier 1 tests
- Scheduling/orchestration setup
- Integration with downstream BI tools

## Open Questions

1. **Which Notion resources to ingest?** (databases, pages, blocks, users, comments, or all?)
2. **Refresh cadence?** (hourly, daily, on-demand?)
3. **Incremental strategy?** (full refresh or incremental based on last_edited_time?)
4. **Filters?** (specific databases only, date range limits, archived content handling?)
5. **Volume expectations?** (approximate record counts to inform testing strategy)

## Next Steps

1. Clarify open questions with user
2. Discover available Notion resources via dlt introspection
3. Design Pipeline Inventory with selected resources
4. Proceed to workspace setup and implementation
