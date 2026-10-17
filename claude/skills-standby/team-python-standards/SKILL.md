---
name: team-python-standards
model: sonnet
effort: medium
description: Python implementation patterns for FastAPI/Flask. Service abstractions, configuration, testing, logging, error handling.
user_invocable: false
---

# Python Standards (FastAPI/Flask)

## Service Layer

### Protocol-Based Abstraction

```python
from typing import Protocol, Optional

# Protocol defines contract (structural typing)
class OrderService(Protocol):
    def create(self, request: CreateOrderRequest) -> Order: ...
    def find_by_id(self, order_id: int) -> Optional[Order]: ...

# Implementation
class OrderServiceImpl:
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def create(self, request: CreateOrderRequest) -> Order:
        ...
```

### ABC Alternative (When Explicit Inheritance Preferred)

```python
from abc import ABC, abstractmethod

class OrderService(ABC):
    @abstractmethod
    def create(self, request: CreateOrderRequest) -> Order: ...
```

### Dependency Injection

```python
# FastAPI
def get_order_service() -> OrderService:
    return OrderServiceImpl(repository=get_repository())

@router.post("/orders")
def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service)
):
    return service.create(request)
```

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Service without Protocol/ABC | Define abstraction |
| Missing type hints | Type all public methods |
| Global service instances | Use dependency injection |

## Configuration

### File Structure

```
app/
├── config.py           # Pydantic settings
├── .env               # Local dev (git-ignored)
├── .env.example       # Template for required vars
```

### Pydantic Settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Defaults
    page_size: int = 20
    max_retries: int = 3

    # Environment-specific (no defaults = required)
    database_url: str
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### Secrets Handling

```python
# From environment - required, no default
database_url: str

# NEVER hardcode
# database_url: str = "postgresql://user:secret@localhost/db"
```

## Testing (pytest)

### Service Test Pattern

```python
import pytest
from unittest.mock import Mock

def test_create_order_saves_and_returns():
    # Arrange
    mock_repo = Mock()
    mock_repo.save.return_value = Order(id=1, ...)
    service = OrderServiceImpl(repository=mock_repo)

    # Act
    result = service.create(CreateOrderRequest(...))

    # Assert
    assert result.id == 1
    mock_repo.save.assert_called_once()

# Fixture for reuse
@pytest.fixture
def order_service(mock_repository):
    return OrderServiceImpl(repository=mock_repository)
```

### Integration Test Pattern

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres():
    with PostgresContainer("postgres:15") as pg:
        yield pg.get_connection_url()

def test_find_by_customer_id(postgres, repository):
    # Test against real PostgreSQL
    ...
```

## Logging (structlog)

### Logger Setup

```python
import structlog

logger = structlog.get_logger()

class OrderServiceImpl:
    def create(self, request: CreateOrderRequest) -> Order:
        logger.info("create_order", customer_id=request.customer_id)
        try:
            order = self._repository.save(...)
            logger.info("create_order_success", order_id=order.id)
            return order
        except Exception as ex:
            logger.error("create_order_failed", customer_id=request.customer_id, error=str(ex))
            raise
```

### structlog Config (JSON for CloudWatch)

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
```

## Error Handling

### Exception Classes

```python
class AppError(Exception):
    def __init__(self, code: str, message: str, context: dict = None):
        self.code = code
        self.message = message
        self.context = context or {}
        super().__init__(message)

class OrderNotFoundError(AppError):
    def __init__(self, order_id: int):
        super().__init__(
            code="ORDER_NOT_FOUND",
            message=f"Order not found: {order_id}",
            context={"order_id": order_id}
        )
```

### FastAPI Handler

```python
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_map = {
        "ORDER_NOT_FOUND": 404,
        "VALIDATION_ERROR": 400,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content={"error": exc.code, "message": exc.message}
    )
```

## Review Checklist

- [ ] Service without Protocol/ABC
- [ ] Missing type hints on public methods
- [ ] Hardcoded config values
- [ ] Secrets in code or committed .env
- [ ] Missing dependency injection
- [ ] Bare `except:` clauses
- [ ] No structured logging
