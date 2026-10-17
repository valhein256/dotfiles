---
name: team-testing-standards
model: sonnet
effort: medium
description: Testing standards for unit, integration, and E2E tests. Covers shared concepts; see language skills for framework-specific patterns.
user_invocable: false
---

# Team Testing Standards

Shared testing concepts for all languages. See language skills for framework-specific patterns.

## Unit Testing

### What to Unit Test

| Layer | Test Focus | Mock |
|-------|------------|------|
| Service | Business logic, orchestration | Repository, external clients |
| Repository | Query logic (if custom) | Database (use in-memory) |
| Transformations | Data mapping, calculations | Nothing (pure functions) |
| Validators | Validation rules | Nothing (pure functions) |

### Test Structure (AAA Pattern)

All tests follow **Arrange → Act → Assert**:
- **Arrange:** Set up test data and mocks
- **Act:** Call the method under test
- **Assert:** Verify the outcome

### Naming Convention

```
test_<method>_<scenario>_<expected_outcome>
```

### What NOT to Unit Test

- Getters/setters, constructors (no logic)
- Framework code (annotations, ORM mappings)
- Private methods directly (test via public interface)
- Simple pass-through methods

### Coverage Targets

| Scope | Target |
|-------|--------|
| Overall | 85% |
| Service layer | 90%+ |
| Repository layer | 70%+ |

Exclude from coverage: Config classes, DTOs, generated code

## Mocking

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Pure functions |
| Databases (in unit tests) | Value objects / DTOs |
| Message queues | The class under test |
| File system | Simple dependencies |

### Mock vs Real by Test Type

| Test Type | Database | External APIs | Message Queues |
|-----------|----------|---------------|----------------|
| Unit | Mock | Mock | Mock |
| Integration | Real (testcontainers) | Mock or sandbox | Real (testcontainers) |
| E2E | Real | Real (staging) | Real |

### Anti-Patterns

| Don't | Why |
|-------|-----|
| Mock everything | Brittle, tests implementation |
| Verify every call | Over-specification |
| Mock the class under test | Testing nothing |
| Deep mock chains | Hard to maintain |

## Integration Testing

### What to Integration Test

| Component | Test Focus |
|-----------|------------|
| Repository layer | Real queries against real DB |
| External API clients | Contract validation |
| Message consumers | Full processing flow |
| Data pipelines | End-to-end transformation |

### Test Data Management

- **< 5 cases:** Inline in test code
- **≥ 5 cases:** Externalize to `tests/data/*.json`

### Rules

1. Isolate test data - each test sets up/tears down its own
2. No shared state - tests run independently
3. Use realistic data - production-like samples
4. Test failure paths - DB down, API timeout, malformed messages

## E2E Testing

### When to Write

| Use Case | Example |
|----------|---------|
| Critical business flows | Order processing end-to-end |
| Cross-service integration | Data flows through multiple services |
| Smoke tests | Basic health check after deployment |

### Rules

- Keep count low (5-10 max per service)
- Test happy paths only
- Idempotent cleanup
- Run separately from unit tests

## Test Pyramid

```
        /\        E2E (few)
       /──\
      /    \      Integration (moderate)
     /──────\
    /        \    Unit (many)
   /──────────\
```

| Level | Speed | When to Run |
|-------|-------|-------------|
| Unit | Fast (<1s) | Every commit |
| Integration | Medium (seconds) | Every PR |
| E2E | Slow (minutes) | Pre-deploy |

## Language-Specific Patterns

For framework-specific testing patterns:
- Java (JUnit 5/Mockito) → `team-java-standards`
- Python (pytest) → `team-python-standards`
- TypeScript (Jest) → `team-typescript-standards`

## Review Checklist

### Unit Test Violations
- [ ] Missing AAA structure
- [ ] Unclear test names
- [ ] Testing implementation instead of behavior
- [ ] No tests for edge cases / error paths

### Mocking Violations
- [ ] Mocking the class under test
- [ ] Over-mocking (mocking everything)
- [ ] Deep mock chains

### Integration Test Violations
- [ ] Shared state between tests
- [ ] Missing cleanup / teardown
- [ ] Not using testcontainers

### Coverage Violations
- [ ] Below 85% overall coverage
- [ ] Service layer below 90%
- [ ] Critical paths not tested
