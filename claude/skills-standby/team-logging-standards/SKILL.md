---
name: team-logging-standards
model: sonnet
effort: medium
description: Logging standards for structured logging. Covers shared concepts; see language skills for framework-specific patterns.
user_invocable: false
---

# Team Logging Standards

Shared logging concepts for all languages. See language skills for framework-specific patterns.

---

## Log Levels

### Level Definitions

| Level | When to Use | Example |
|-------|-------------|---------|
| `ERROR` | Operation failed, needs attention | DB connection lost, payment failed |
| `WARN` | Unexpected but recoverable | Retry succeeded, fallback used, deprecated API called |
| `INFO` | Business events, state changes | User logged in, order created, job completed |
| `DEBUG` | Diagnostic details for troubleshooting | Request payload, query params, cache hit/miss |
| `TRACE` | Very detailed flow (rarely used in prod) | Method entry/exit, loop iterations |

### Rules

1. **Production default:** `INFO` level
2. **Never log at ERROR and continue silently** - if it's ERROR, handle it
3. **No sensitive data at any level** - no passwords, tokens, PII
4. **DEBUG should be safe to enable in prod** - no performance-killing logs

### Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| `log.error("Error occurred")` | No context | Include what failed and why |
| `log.info("Processing...")` then `log.info("Done")` | Noise | Single log with duration |
| `log.debug(largeObject)` | Performance hit | Log specific fields |
| `log.error(exception)` only | Loses context | Add operation context + exception |

---

## Structured Logging Format

### Required Fields (All Logs)

```json
{
  "timestamp": "2026-02-06T10:30:00.123Z",
  "level": "INFO",
  "service": "order-service",
  "message": "Order created"
}
```

| Field | Source | Purpose |
|-------|--------|---------|
| `timestamp` | Auto (framework) | When it happened |
| `level` | Auto (framework) | Severity |
| `service` | Config/env var | Which service |
| `message` | Developer | What happened |

### Optional Context Fields

```json
{
  "correlation_id": "abc-123-def",
  "user_id": "user-456",
  "tenant_id": "tenant-789",
  "duration_ms": 234,
  "error_code": "PAYMENT_DECLINED",
  "request_id": "req-111"
}
```

### Correlation ID (When Available)

1. API-facing services: generate or propagate `X-Correlation-ID` header
2. Internal services: include if passed, omit if not available
3. Pass through all downstream calls when present
4. Store in thread-local / async context

---

## What to Log

### Must Log (INFO)

| Event | Fields to Include |
|-------|-------------------|
| Request received | method, path, user_id (if auth'd) |
| Request completed | method, path, status_code, duration_ms |
| Business event | event_type, entity_id, outcome |
| External call made | target_service, duration_ms, success |
| Job started/completed | job_name, duration_ms, records_processed |

### Must Log (ERROR)

| Event | Fields to Include |
|-------|-------------------|
| Operation failed | operation, error_code, message, context |
| External call failed | target_service, error_code, retry_count |
| Unhandled exception | exception class, message, stack trace |

### Never Log

- Passwords, API keys, tokens
- Full credit card numbers (last 4 only)
- Email addresses
- PII beyond what's needed (no SSN, full address)
- Request/response bodies in production (DEBUG only)
- Health check requests (noise)

---

## CloudWatch Integration

### Format Rules

1. **One JSON object per line** - no pretty printing
2. **Keep messages short** - CloudWatch charges by ingestion volume
3. **Use consistent field names** - enables CloudWatch Insights queries
4. **Log group per service** - `/app/{env}/{service-name}`

### CloudWatch Insights Examples

```sql
-- Find errors for a correlation ID
fields @timestamp, message, error_code
| filter correlation_id = "abc-123"
| sort @timestamp asc

-- Error rate by service
filter level = "ERROR"
| stats count() by service
| sort count desc

-- Slow requests
filter duration_ms > 1000
| fields @timestamp, service, message, duration_ms
| sort duration_ms desc
```

---

## Language-Specific Patterns

For framework-specific logging patterns:
- Java (Logback) → `team-java-standards`
- Python (structlog) → `team-python-standards`
- TypeScript (pino) → `team-typescript-standards`

---

## Review Checklist

When reviewing logging in code, check for:

### Level Violations
- [ ] ERROR level but no error handling
- [ ] INFO level for debug/diagnostic data
- [ ] Missing ERROR log when operation fails

### Format Violations
- [ ] Unstructured log messages (string concatenation)
- [ ] Missing required fields (service, message)
- [ ] Pretty-printed JSON (multi-line)

### Content Violations
- [ ] Passwords, tokens, or API keys logged
- [ ] Email addresses logged
- [ ] Full credit card numbers
- [ ] PII in log messages
- [ ] Large objects logged at DEBUG without field selection

### Pattern Violations
- [ ] Paired "Starting..." / "Done" logs (use single log with duration)
- [ ] Empty or generic error messages
- [ ] Exception logged without operation context

