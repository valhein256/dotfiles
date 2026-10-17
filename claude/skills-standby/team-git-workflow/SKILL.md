---
name: team-git-workflow
model: sonnet
effort: medium
description: Git branching strategy, commit message conventions, release tagging, and hotfix workflow for trunk-based development.
user_invocable: false
---

# Team Git Workflow

Git branching strategy, commit message conventions, release tagging, and hotfix workflow.

---

## Branching Strategy

### Trunk-Based Development

```
develop (always deployable)
  │
  ├── pr/{TICKET}/add-feature    ← short-lived, squash merged
  ├── pr/PE-456/fix-bug         ← short-lived, squash merged
  │
  └── hotfix/{TICKET}/critical   ← branched from tag, not develop
```

### Branch Types

| Branch | Source | Merges To | Lifespan |
|--------|--------|-----------|----------|
| `develop` | - | - | Permanent |
| `pr/{TICKET}/description` | develop | develop (squash) | Days |
| `hotfix/{TICKET}/description` | tag (e.g., v1.2.3) | hotfix branch → tag, then PR to develop | Hours |

### Rules

1. **Develop is always deployable** - never commit directly
2. **Feature branches live < 1 week** - smaller PRs, faster merges
3. **Delete branches after merge** - keep repo clean
4. **No long-lived feature branches** - if it takes weeks, break it up

---

## Commit Messages

### During Development (Conventional Commits)

```
<type>: <description>

feat:     new feature
fix:      bug fix
refactor: code change (no new feature, no bug fix)
test:     adding/updating tests
docs:     documentation only
chore:    build, deps, config changes
```

**Examples:**
```
feat: add email validation to signup form
fix: handle null response from payment API
refactor: extract user lookup into service
test: add coverage for edge cases in OrderService
chore: upgrade Spring Boot to 3.2
```

**Rules:**
- Lowercase, no period at end
- Imperative mood ("add" not "added")
- Keep under 72 characters

### Squash Merge to Develop (Jira Prefix)

```
{TICKET}: Brief description of the change
```

**Examples:**
```
{TICKET}: Add user validation to signup flow
{TICKET}: Fix payment timeout handling
```

**Rules:**
- Ticket number from branch name
- Matches PR title format
- One line, describes the overall change (not individual commits)

---

## Releases & Tagging

### Semantic Versioning

```
v<major>.<minor>.<patch>

v1.0.0  → initial release
v1.1.0  → new features (backward compatible)
v1.1.1  → bug fixes only
v2.0.0  → breaking changes
```

### When to Bump

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking API change | Major | v1.2.3 → v2.0.0 |
| New feature (backward compatible) | Minor | v1.2.3 → v1.3.0 |
| Bug fix, patch, small improvement | Patch | v1.2.3 → v1.2.4 |

### Tagging Process

```bash
# Ensure develop is up to date
git checkout develop
git pull

# Create annotated tag
git tag -a v1.3.0 -m "Release v1.3.0: Brief description"

# Push tag
git push origin v1.3.0
```

### Artifact Promotion

```
v1.3.0 tag
    │
    └── Build artifact once
            │
            ├── Deploy to dev    (same artifact)
            ├── Deploy to staging (same artifact)
            └── Deploy to prod   (same artifact)
```

**Rules:**
- Never rebuild between environments
- Tag triggers CI/CD pipeline
- Artifact tagged with version for traceability

---

## Hotfix Workflow

### When to Use

- Critical bug in production
- Security vulnerability
- Cannot wait for normal release cycle

### Process

```
Production: v1.2.3
Develop: has unreleased features for v1.3.0

1. Branch from production tag (not develop)
   git checkout -b hotfix/{TICKET}/fix-critical v1.2.3

2. Make fix, commit with conventional commits
   git commit -m "fix: handle null in payment callback"

3. Create PR targeting a hotfix base branch
   gh pr create --base hotfix-v1.2.3 --title "{TICKET}: Fix critical payment bug"

4. After merge, tag new patch version
   git checkout hotfix-v1.2.3
   git tag -a v1.2.4 -m "Hotfix v1.2.4: Fix payment callback null handling"
   git push origin v1.2.4

5. Deploy v1.2.4 through artifact promotion

6. Merge fix back to develop (so it's not lost)
   git checkout develop
   git checkout -b pr/{TICKET}/merge-hotfix
   git cherry-pick <commit-hash>
   gh pr create --base develop --title "{TICKET}: Merge hotfix to develop"
```

### Hotfix Checklist

- [ ] Branched from production tag, not develop
- [ ] Fix is minimal (no extra changes)
- [ ] New patch tag created
- [ ] Artifact built from tag
- [ ] Fix merged back to develop

---

## Review Checklist

When reviewing git practices, check for:

### Branch Violations
- [ ] Direct commits to develop
- [ ] Branch not following `pr/{TICKET}/` naming
- [ ] Long-lived feature branches (> 1 week)
- [ ] Hotfix branched from develop instead of tag

### Commit Message Violations
- [ ] Missing type prefix (feat/fix/etc.)
- [ ] Capitalized or with period
- [ ] Past tense instead of imperative
- [ ] Over 72 characters

### Release Violations
- [ ] Tag without `v` prefix
- [ ] Non-semantic version format
- [ ] Rebuilding artifact between environments
- [ ] Missing tag annotation/message

