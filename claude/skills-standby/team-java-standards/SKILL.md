---
name: team-java-standards
model: sonnet
effort: medium
description: Java implementation patterns for Spring Boot + Maven. Service interfaces, configuration, testing, logging, error handling.
user_invocable: false
---

# Java Standards (Spring Boot + Maven)

## Service Layer

### Interface + Implementation Pattern

```java
// Interface defines contract
public interface OrderService {
    Order create(CreateOrderRequest request);
    Optional<Order> findById(Long id);
}

// Implementation is Spring-managed
@Service
public class OrderServiceImpl implements OrderService {
    private final OrderRepository orderRepository;

    // Constructor injection (not field injection)
    public OrderServiceImpl(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Override
    public Order create(CreateOrderRequest request) { ... }
}
```

### Why Interfaces?

- **Testability:** Easy to mock in unit tests
- **Loose coupling:** Controller depends on interface, not implementation
- **Swappable:** Can replace implementation without changing consumers

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `@Autowired` field injection | Constructor injection |
| Concrete service in controller | Interface type |
| Service without interface | Always define interface |

## Configuration

### File Structure

```
src/main/resources/
├── application.properties      # Defaults, feature flags
├── application-dev.properties  # Dev environment
├── application-prod.properties # Prod environment
```

### Separation Rules

| application.properties | application-{env}.properties |
|------------------------|------------------------------|
| `app.feature.enabled=true` | `spring.datasource.url=...` |
| `app.page.size=20` | `external.api.base-url=...` |
| `app.retry.max-attempts=3` | `spring.redis.host=...` |

### Secrets Handling

```properties
# Reference environment variable
spring.datasource.password=${DB_PASSWORD}
external.api.key=${API_KEY}

# NEVER hardcode secrets
```

### @ConfigurationProperties vs @Value

```java
// For grouped config - type-safe, validated
@ConfigurationProperties(prefix = "app.retry")
public record RetryConfig(int maxAttempts, Duration delay) {}

// For single values
@Value("${app.feature.enabled}")
private boolean featureEnabled;
```

## Testing (JUnit 5 + Mockito)

### Service Test Pattern

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceImplTest {
    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderServiceImpl orderService;

    @Test
    void create_validRequest_savesAndReturnsOrder() {
        // Arrange
        var request = new CreateOrderRequest(...);
        when(orderRepository.save(any())).thenReturn(new OrderEntity(1L, ...));

        // Act
        var result = orderService.create(request);

        // Assert
        assertThat(result.id()).isEqualTo(1L);
        verify(orderRepository).save(any());
    }
}
```

### Integration Test Pattern

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIT {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");

    @Autowired
    private OrderRepository orderRepository;

    @Test
    void findByCustomerId_existingOrders_returnsAll() { ... }
}
```

## Logging (Logback)

### Logger Setup

```java
@Service
public class OrderServiceImpl implements OrderService {
    private static final Logger log = LoggerFactory.getLogger(OrderServiceImpl.class);

    public Order create(CreateOrderRequest request) {
        log.info("create_order customerId={}", request.customerId());
        try {
            // logic
            log.info("create_order_success orderId={} customerId={}", order.id(), request.customerId());
            return order;
        } catch (Exception ex) {
            log.error("create_order_failed customerId={}", request.customerId(), ex);
            throw ex;
        }
    }
}
```

### logback-spring.xml (JSON for CloudWatch)

```xml
<configuration>
    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <includeMdcKeyName>correlationId</includeMdcKeyName>
        </encoder>
    </appender>
    <root level="INFO">
        <appender-ref ref="JSON"/>
    </root>
</configuration>
```

## Error Handling

### Exception Classes

```java
public class OrderNotFoundException extends RuntimeException {
    private final String code = "ORDER_NOT_FOUND";
    private final Long orderId;

    public OrderNotFoundException(Long orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }

    // getters for code, orderId
}
```

### Global Handler

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(OrderNotFoundException.class)
    ResponseEntity<ApiError> handle(OrderNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ApiError(ex.getCode(), ex.getMessage()));
    }
}
```

## Review Checklist

- [ ] Service without interface
- [ ] Field injection (`@Autowired` on field)
- [ ] Hardcoded config values
- [ ] Secrets in properties files
- [ ] Missing `@Transactional` on write operations
- [ ] Raw SQL in service layer
- [ ] Empty catch blocks
