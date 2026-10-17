---
name: team-secure-coding
model: sonnet
effort: medium
description: Secure coding standards for data pipelines and internal services. Covers input validation, secrets management, data protection, and dependency security.
user_invocable: false
---

# Team Secure Coding Standards

Secure coding standards for data pipelines and internal services.

---

## Input Validation

### Validate at System Boundaries

**Where to validate:**
- File ingestion (CSV, JSON, XML, Parquet)
- Message queues (Kafka, SQS, RabbitMQ)
- External API responses
- Database query results from external DBs
- User-provided configuration

**NOT internal service-to-service calls** (trust internal contracts)

### Validation Rules

| Data Type | Validate | Example |
|-----------|----------|---------|
| Strings | Max length, allowed characters, format | Email regex, no control chars |
| Numbers | Range, type (int vs float) | `0 < quantity < 10000` |
| Dates | Format, reasonable range | Not year 9999, not before 1900 |
| Arrays | Max size, element validation | Max 1000 items, each validated |
| Files | Size limit, type check, path traversal | No `../`, max 100MB |

### Path Traversal Prevention

```python
# BAD - allows ../../../etc/passwd
file_path = user_input
open(file_path)

# GOOD - resolve and validate
import os
base_dir = "/app/data"
requested = os.path.realpath(os.path.join(base_dir, user_input))
if not requested.startswith(base_dir):
    raise ValidationError("Invalid path")
```

### Command Injection Prevention

```python
# BAD - shell injection
os.system(f"process_file {filename}")

# GOOD - no shell, use list
subprocess.run(["process_file", filename], shell=False)
```

### SQL Injection (Even in Pipelines)

```python
# BAD - string interpolation
query = f"SELECT * FROM table WHERE id = '{user_id}'"

# GOOD - parameterized
query = "SELECT * FROM table WHERE id = %s"
cursor.execute(query, (user_id,))
```

---

## Secrets Management

### Never Hardcode Secrets

```python
# BAD - hardcoded
db_password = "super_secret_123"
api_key = "sk-abc123xyz"

# BAD - in config file committed to git
config.yaml:
  database:
    password: "super_secret_123"

# GOOD - environment variable
db_password = os.environ["DB_PASSWORD"]

# GOOD - secrets manager
from aws_secrets import get_secret
db_password = get_secret("prod/db/password")
```

### Secrets Sources (Preferred Order)

| Source | Use For | Example |
|--------|---------|---------|
| Secrets Manager (AWS/GCP/Azure) | Production credentials | DB passwords, API keys |
| Environment variables | Container/runtime injection | Injected by K8s, ECS |
| Encrypted config | Deploy-time secrets | Sealed secrets, SOPS |

**Never use:**
- `.env` files in production
- Config files committed to git
- Hardcoded values anywhere

### Service Account Best Practices

1. **One service account per service** - no shared credentials
2. **Least privilege** - only permissions needed
3. **Rotate regularly** - automated rotation preferred
4. **No long-lived tokens** - use short-lived or auto-rotating

### Secrets in Logs

No secrets in logs — see `team-logging-standards` for full rules. Mask if must reference: `api_key=sk-***xyz`

### Git Protection

```bash
# .gitignore - always include
.env
*.pem
*.key
credentials.json
secrets.yaml
```

Pre-commit hook to block secrets (use tools like `gitleaks`, `detect-secrets`)

---

## Data Protection

### PII Handling

**What is PII in pipelines:**
- Email addresses, phone numbers
- Names, addresses
- SSN, national IDs
- IP addresses, device IDs
- Any data that identifies a person

### Rules by Data Lifecycle

| Stage | Rule |
|-------|------|
| Ingestion | Identify and tag PII fields early |
| Processing | Minimize - only pass PII where needed |
| Storage | Encrypt at rest, separate from non-PII if possible |
| Output | Mask/redact in reports, no PII in logs |
| Retention | Delete when no longer needed |

### Encryption

**At rest:**
- Use platform encryption (S3 SSE, RDS encryption, Redshift encryption)
- Don't roll your own crypto

**In transit:**
- TLS for all external connections
- Internal service mesh handles internal traffic

### Data Masking Patterns

```python
# Email
"user@example.com" → "u***@example.com"

# Phone
"+1-555-123-4567" → "+1-555-***-4567"

# Credit card (if ever encountered)
"4111111111111111" → "************1111"

# Generic
def mask(value, visible=4):
    return "*" * (len(value) - visible) + value[-visible:]
```

### Access Control

- **Need-to-know basis** - not everyone needs PII access
- **Audit trail** - log who accessed PII (not the PII itself)
- **Separate environments** - prod PII never in dev/staging

---

## Dependency Security

### Keep Dependencies Updated

```bash
# Check for vulnerabilities
npm audit                    # Node
pip-audit                    # Python
mvn dependency-check:check   # Java
```

### Rules

1. **Pin versions** - no `latest` or `*` in production
2. **Review updates** - don't blindly upgrade major versions
3. **Automated scanning** - Dependabot, Snyk, or similar in CI
4. **Minimal dependencies** - fewer deps = smaller attack surface

### Trusted Sources Only

| Language | Trusted Source |
|----------|----------------|
| Python | PyPI (official), internal mirror |
| Node | npm (official), internal registry |
| Java | Maven Central, internal Nexus |

**Never:**
- Install from random GitHub repos directly
- Use unverified mirrors
- Disable SSL verification for package managers

### Responding to Vulnerabilities

| Severity | Action |
|----------|--------|
| Critical | Patch immediately, same day |
| High | Patch within 1 week |
| Medium | Patch in next release |
| Low | Track, address when convenient |

---

## Review Checklist

When reviewing code for security, check for:

### Input Validation Violations
- [ ] External data used without validation
- [ ] File paths not checked for traversal
- [ ] Shell commands with user input (`shell=True`)
- [ ] SQL queries with string interpolation
- [ ] Missing size/length limits

### Secrets Violations
- [ ] Hardcoded credentials
- [ ] Secrets in config files (committed)
- [ ] `.env` files not in `.gitignore`
- [ ] Secrets logged or printed
- [ ] Shared service accounts

### Data Protection Violations
- [ ] PII in logs
- [ ] Unencrypted PII storage
- [ ] Prod PII in non-prod environments
- [ ] Missing data masking in outputs

### Dependency Violations
- [ ] Unpinned versions
- [ ] Known vulnerable packages
- [ ] Dependencies from untrusted sources

