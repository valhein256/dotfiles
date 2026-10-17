---
name: team-typescript-standards
model: sonnet
effort: medium
description: TypeScript implementation patterns for Express/Node. Service interfaces, configuration, testing, logging, error handling.
user_invocable: false
---

# TypeScript Standards (Express/Node)

## Service Layer

### Interface + Class Pattern

```typescript
// Interface defines contract
interface OrderService {
  create(request: CreateOrderRequest): Promise<Order>;
  findById(id: string): Promise<Order | null>;
}

// Implementation
class OrderServiceImpl implements OrderService {
  constructor(private readonly repository: OrderRepository) {}

  async create(request: CreateOrderRequest): Promise<Order> {
    ...
  }
}
```

### Dependency Injection

```typescript
// Simple factory pattern
function createOrderService(): OrderService {
  return new OrderServiceImpl(createOrderRepository());
}

// Or with DI container (tsyringe, inversify)
@injectable()
class OrderServiceImpl implements OrderService {
  constructor(@inject("OrderRepository") private repository: OrderRepository) {}
}
```

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Service without interface | Define interface |
| Use of `any` type | Proper typing |
| Concrete dependencies | Interface types |

## Configuration

### File Structure

```
src/
├── config/
│   ├── index.ts        # Config loader
│   └── schema.ts       # Zod validation
├── .env               # Local dev (git-ignored)
├── .env.example       # Template
```

### Typed Config with Zod

```typescript
import { z } from "zod";

const configSchema = z.object({
  // Defaults
  pageSize: z.number().default(20),
  maxRetries: z.number().default(3),

  // Environment-specific (required)
  databaseUrl: z.string(),
  apiKey: z.string(),
});

type Config = z.infer<typeof configSchema>;

export const config: Config = configSchema.parse({
  pageSize: parseInt(process.env.PAGE_SIZE || "20"),
  maxRetries: parseInt(process.env.MAX_RETRIES || "3"),
  databaseUrl: process.env.DATABASE_URL,
  apiKey: process.env.API_KEY,
});
```

### Secrets Handling

```typescript
// From environment, validated - required
databaseUrl: z.string(),

// NEVER hardcode
// databaseUrl: z.string().default("postgresql://user:secret@localhost/db"),
```

## Testing (Jest)

### Service Test Pattern

```typescript
describe("OrderServiceImpl", () => {
  let service: OrderService;
  let mockRepository: jest.Mocked<OrderRepository>;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
    };
    service = new OrderServiceImpl(mockRepository);
  });

  it("create_validRequest_savesAndReturnsOrder", async () => {
    // Arrange
    mockRepository.save.mockResolvedValue({ id: "1", ... });

    // Act
    const result = await service.create({ ... });

    // Assert
    expect(result.id).toBe("1");
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
  });
});
```

### Integration Test Pattern

```typescript
import { PostgreSqlContainer } from "@testcontainers/postgresql";

describe("OrderRepository Integration", () => {
  let container: PostgreSqlContainer;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
  });

  afterAll(async () => {
    await container.stop();
  });

  it("findByCustomerId_existingOrders_returnsAll", async () => {
    // Test against real PostgreSQL
  });
});
```

## Logging (pino)

### Logger Setup

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
});

class OrderServiceImpl implements OrderService {
  private readonly log = logger.child({ service: "OrderService" });

  async create(request: CreateOrderRequest): Promise<Order> {
    this.log.info({ customerId: request.customerId }, "create_order");
    try {
      const order = await this.repository.save(...);
      this.log.info({ orderId: order.id }, "create_order_success");
      return order;
    } catch (error) {
      this.log.error({ customerId: request.customerId, error }, "create_order_failed");
      throw error;
    }
  }
}
```

## Error Handling

### Error Classes

```typescript
class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly context: Record<string, unknown> = {}
  ) {
    super(message);
    this.name = "AppError";
  }
}

class OrderNotFoundError extends AppError {
  constructor(orderId: string) {
    super("ORDER_NOT_FOUND", `Order not found: ${orderId}`, { orderId });
  }
}
```

### Express Middleware

```typescript
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof AppError) {
    const statusMap: Record<string, number> = {
      ORDER_NOT_FOUND: 404,
      VALIDATION_ERROR: 400,
    };
    return res.status(statusMap[err.code] || 500).json({
      error: err.code,
      message: err.message,
    });
  }

  // Unexpected error
  logger.error({ error: err }, "unhandled_error");
  res.status(500).json({ error: "INTERNAL_ERROR" });
}

app.use(errorHandler);
```

## Review Checklist

- [ ] Service without interface
- [ ] Use of `any` type
- [ ] Hardcoded config values
- [ ] Secrets in code or committed .env
- [ ] Missing strict null checks
- [ ] Empty catch blocks
- [ ] Console.log instead of structured logger
