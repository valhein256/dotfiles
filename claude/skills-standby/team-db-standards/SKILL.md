---
name: team-db-standards
model: sonnet
effort: medium
description: Database naming conventions, schema design patterns, and query best practices for relational (PostgreSQL/MySQL), NoSQL (MongoDB/DynamoDB), and Redshift. Use during design/planning, development, and PR reviews.
user_invocable: false
---

# Team Database Standards

Database naming conventions, schema design patterns, and query best practices.

---

## Naming Conventions

### General Rules (All Databases)
- `snake_case` for everything (tables, columns, indexes)
- Singular nouns for tables (`user`, not `users`)
- No prefixes like `tbl_` or `col_`
- Avoid reserved words (`user` → `app_user`, `order` → `purchase_order`)

### Relational (PostgreSQL/MySQL)

| Element | Convention | Example |
|---------|------------|---------|
| Table | singular noun | `customer`, `order_item` |
| Primary key | `id` | `id` |
| Foreign key | `<referenced_table>_id` | `customer_id` |
| Boolean | `is_` or `has_` prefix | `is_active`, `has_subscription` |
| Timestamp | `_ts` suffix | `created_ts`, `updated_ts`, `deleted_ts` |
| Date | `_dt` suffix | `hired_dt`, `due_dt`, `birth_dt` |
| Index | `ix_<table>_<columns>` | `ix_customer_email` |
| Unique constraint | `uq_<table>_<columns>` | `uq_customer_email` |

### NoSQL (MongoDB/DynamoDB)

| Element | Convention | Example |
|---------|------------|---------|
| Collection/Table | singular noun | `customer`, `event_log` |
| Partition key | descriptive name | `tenant_id`, `customer_id` |
| Sort key | descriptive with purpose | `created_ts`, `event_type#timestamp` |
| GSI | `gsi_<access_pattern>` | `gsi_by_email`, `gsi_by_status` |

### Redshift

| Element | Convention | Example |
|---------|------------|---------|
| Schema | `<domain>` | `sales`, `marketing`, `raw` |
| Fact table | `fact_<noun>` | `fact_order`, `fact_page_view` |
| Dimension table | `dim_<noun>` | `dim_customer`, `dim_product` |
| Staging table | `stg_<source>_<noun>` | `stg_salesforce_account` |

---

## Schema Design Patterns

### Relational - When to Normalize vs Denormalize

**Normalize (3NF) by default:**
- Transactional data with frequent updates
- Data integrity is critical
- Storage efficiency matters
- Queries are flexible/unpredictable

**Denormalize when:**
- Read-heavy with predictable access patterns
- Joins cause measurable performance issues (measure first!)
- Audit/history tables (snapshot the state)

### NoSQL - Design for Access Patterns

**DynamoDB Rules:**
1. Start with access patterns, not entities
2. Single table design preferred - multiple entities in one table
3. Composite sort keys for hierarchical data: `ORDER#123#ITEM#456`
4. Overload GSIs - one GSI can serve multiple access patterns

**MongoDB Rules:**
1. Embed when data is queried together and updated together
2. Reference when data is large, updated independently, or shared
3. Avoid unbounded arrays (cap at ~500 items, then bucket)

| Pattern | Embed | Reference |
|---------|-------|-----------|
| Order → Items | Yes (queried together) | No |
| User → Posts | No (unbounded) | Yes |
| Product → Category | Embed category name | Reference if category updates matter |

### Redshift - Star Schema

**Rules:**
1. Fact tables: narrow, append-only, numeric measures
2. Dimension tables: wide, descriptive attributes, slowly changing
3. Use surrogate keys (`dim_customer.id`), not natural keys
4. Denormalize dimensions (no snowflake schema)
5. Distribution keys: pick high-cardinality column used in joins
6. Sort keys: columns used in WHERE/ORDER BY clauses

---

## Query Patterns

### N+1 Prevention

**The problem:**
```python
# BAD - N+1 queries
users = get_all_users()           # 1 query
for user in users:
    orders = get_orders(user.id)  # N queries
```

**Solutions by database:**

| Database | Solution |
|----------|----------|
| Relational | JOIN or batch fetch with `WHERE id IN (...)` |
| MongoDB | `$lookup` aggregation or embed related data |
| DynamoDB | Query with begins_with on sort key, or BatchGetItem |

**Code pattern (all languages):**
```
# GOOD - batch fetch
users = get_all_users()
user_ids = [u.id for u in users]
orders_by_user = get_orders_for_users(user_ids)  # 1 query, returns map
```

### Index Usage Rules

**Relational:**
1. Index foreign keys (always)
2. Index columns in WHERE clauses (if selective)
3. Composite indexes: left-to-right column order matters
4. Don't index low-cardinality columns alone (`is_active`)
5. Cover queries when possible (include all SELECT columns)

**When NOT to index:**
- Tables under 1000 rows (full scan is fine)
- Columns updated very frequently
- Low selectivity (boolean, status with 3 values)

**DynamoDB:**
- Design GSIs for each access pattern
- Sparse indexes: only items with the attribute are indexed
- Avoid scan operations - always query with partition key

**Redshift:**
- No traditional indexes - use sort keys instead
- Zone maps: Redshift skips blocks automatically for sorted data
- Avoid `SELECT *` - columnar storage benefits from specific columns

### Query Anti-Patterns to Flag in Reviews

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `SELECT *` | Fetches unused columns | List specific columns |
| Missing WHERE on UPDATE/DELETE | Dangerous | Require WHERE clause |
| LIKE with leading wildcard | Can't use index | Full-text search or redesign |
| OR conditions on different columns | Often can't use indexes | UNION or redesign |
| Functions on indexed columns | Invalidates index | Compute before query or functional index |

---

## Review Checklist

When reviewing database changes, check for:

### Naming Violations
- [ ] Table/column not in snake_case
- [ ] Plural table names
- [ ] Missing `_ts` or `_dt` suffix on time columns
- [ ] Foreign key doesn't match `<table>_id` pattern
- [ ] Index/constraint missing standard prefix

### Schema Violations
- [ ] Denormalization without justification
- [ ] Unbounded arrays in MongoDB
- [ ] DynamoDB table without clear access patterns documented
- [ ] Redshift fact table with non-numeric measures
- [ ] Missing distribution/sort key rationale

### Query Violations
- [ ] N+1 query pattern in code
- [ ] Missing index on foreign key
- [ ] `SELECT *` in production code
- [ ] UPDATE/DELETE without WHERE clause
- [ ] Leading wildcard in LIKE

