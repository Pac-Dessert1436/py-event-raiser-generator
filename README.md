# EventRaisers (`eventraisers`) - Dynamic Event System for Python

[![PyPI version](https://img.shields.io/pypi/v/eventraisers.svg)](https://pypi.org/project/eventraisers/)
[![Python versions](https://img.shields.io/pypi/pyversions/eventraisers.svg)](https://pypi.org/project/eventraisers/)
[![License](https://img.shields.io/pypi/l/eventraisers.svg)](https://pypi.org/project/eventraisers/)

**EventRaisers** (formerly "py-event-raiser-generator") is a lightweight, zero-dependency Python library that dynamically generates event decorators and trigger functions at runtime. Define your events once, and EventRaisers automatically creates the necessary infrastructure for event registration and triggering.

> **Note**: Type annotation for event registry is not supported until version 1.0.1 (see [Event Registry Example](#4-event-registry-management) for more details).

## Key Features

🚀 **Dynamic Generation** - Automatically create event decorators and trigger functions from simple definitions

⚡ **Zero Dependencies** - Built entirely on Python's standard library (`typing`, `inspect`)

🔧 **Type Annotated** - Full type hint support for better IDE integration and code clarity

🔄 **Async/Sync Support** - Handle both synchronous and asynchronous callback functions

⏰ **Event Scheduling** - Built-in priority-based event scheduling system

🐍 **Python 3.9+** - Compatible with Python 3.9 through 3.14

## Quick Start

```python
from eventraisers import EventDict, generate_event_raisers

# Define your events
EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# Generate decorators and trigger functions
generate_event_raisers(EVENTS, globals())

# Register event handlers
@user_login
def handle_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

# Trigger events
raise_user_login(user_id=123, timestamp=1718987654.123)
```

## Installation

### From PyPI (Recommended)
```bash
pip install eventraisers
```

### From Source
```bash
git clone https://github.com/Pac-Dessert1436/py-event-raiser-generator.git
cd py-event-raiser-generator
pip install .
```

## Usage Guide

### 1. Define Your Events
Start by defining your events as a dictionary mapping event names to parameter specifications.

```python
from eventraisers import EventDict, generate_event_raisers

# Define events with their parameter names and types
EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)],
    "system_alert": [("message", str), ("severity", str)]
}

# Generate the event infrastructure
generate_event_raisers(EVENTS, globals())
```

### 2. Register Event Handlers
Use the generated decorators to register callback functions for your events.

```python
# Register synchronous handlers
@user_login
def handle_user_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

@order_placed  
def handle_order_placed(order_id: str, total_amount: float) -> None:
    print(f"Order {order_id} placed (total: ${total_amount:.2f})")

# Register asynchronous handlers (Python 3.5+)
@system_alert
async def handle_system_alert(message: str, severity: str) -> None:
    print(f"[{severity.upper()}] {message}")
```

### 3. Trigger Events
Use the generated `raise_*` functions to trigger your events.

```python
# Trigger events with parameters
raise_user_login(user_id=123, timestamp=1718987654.123)
raise_order_placed(order_id="ORD-9876", total_amount=49.99)
raise_system_alert(message="Database connection lost", severity="error")
```

### 4. Event Registry Management
Manage registered callbacks and clear the event registry when needed.

```python
from eventraisers import get_event_registry, clear_event_registry, EventRegistry

# New in 1.0.1: Type annotation for event registry
registry: EventRegistry = get_event_registry() # Inspect registered callbacks
print(f"Registered 'user_login' callbacks: {len(registry.get('user_login', []))}")
clear_event_registry()  # Clear all registered callbacks
```

### 5. Event Scheduling
Schedule events with priority-based execution using the `EventScheduler` class.

```python
from eventraisers import EventScheduler
from time import sleep

scheduler = EventScheduler()

# Schedule events with different priorities
scheduler.schedule_event_action(
    lambda: raise_user_login(user_id=123, timestamp=1718987654.123), 
    priority=30
)
scheduler.schedule_event_action(
    lambda: print("Medium priority event"), 
    priority=50
)
scheduler.schedule_event_action(
    lambda: print("High priority event"), 
    priority=80
)

# Execute all scheduled events in priority order
scheduler.raise_scheduled_events()
print(f"Pending events: {scheduler.pending_event_count}")
```

## Advanced Features

### Type Checking Support
For better IDE integration and type checking, you can provide stub definitions before generating events:

```python
from eventraisers import EventOf, EventDict, generate_event_raisers

EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# Stub definitions for type checkers
def user_login(func: EventOf[int, float]) -> EventOf[int, float]: ...
def order_placed(func: EventOf[str, float]) -> EventOf[str, float]: ...
def raise_user_login(user_id: int, timestamp: float) -> None: ...
def raise_order_placed(order_id: str, total_amount: float) -> None: ...

# Generate the actual implementation
generate_event_raisers(EVENTS, globals())
```

### Error Handling
EventRaisers provides graceful error handling - exceptions in callbacks don't interrupt other handlers:

```python
@user_login
def problematic_handler(user_id: int, timestamp: float) -> None:
    raise ValueError("Something went wrong!")

@user_login  
def working_handler(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} handled successfully")

# Both handlers are called, errors are logged but don't stop execution
raise_user_login(user_id=123, timestamp=1718987654.123)
# Output: [NOTICE] Error in event 'user_login': Something went wrong!
# Output: User 123 handled successfully
```

## API Reference

### Core Functions

#### `generate_event_raisers(events: EventDict, module_globals: dict[str, Any]) -> None`
Generates event decorators and trigger functions based on the provided event definitions.

**Parameters:**
- `events`: Dictionary mapping event names to parameter specifications
- `module_globals`: Global namespace (use `globals()` to add functions to current scope)

#### `clear_event_registry() -> None`
Clears all registered event callbacks from the internal registry.

#### `get_event_registry() -> dict[str, list[Callable[..., Any | Awaitable[Any]]]]`
Returns the current event registry as a dictionary mapping event names to lists of registered callbacks.

### Type Aliases

#### `EventOf: TypeAlias = Callable[[Unpack[_Args]], None | Awaitable[None]]`
Generic type for event callback functions, supporting both synchronous and asynchronous handlers.

#### `EventDict: TypeAlias = dict[str, list[tuple[str, Any]]]`
Type for event definition dictionaries (event name → parameter specifications).

### EventScheduler Class

Priority-based event scheduling system.

#### `EventScheduler()`
Creates a new event scheduler instance.

#### `schedule_event_action(event_action: Callable[[], None], priority: int = 0) -> None`
Schedules an event action with the specified priority (higher numbers execute first).

#### `raise_scheduled_events() -> None`
Executes all scheduled events in priority order.

#### `pending_event_count: int` (property)
Returns the number of pending events in the scheduler.

## Use Cases

EventRaisers is ideal for:

- **Plugin Systems** - Allow plugins to register event handlers
- **Game Development** - Handle game events like collisions, achievements, etc.
- **Web Applications** - Process user actions, notifications, and system events
- **IoT Applications** - Handle sensor data and device state changes
- **Microservices** - Coordinate actions between different service components

## Best Practices

1. **Define events early** - Generate event infrastructure at module initialization
2. **Use descriptive event names** - Make events self-documenting
3. **Provide type stubs** - For better IDE support and type checking
4. **Handle errors gracefully** - Use the built-in error handling for robust applications
5. **Clear registry when needed** - Use `clear_event_registry()` for cleanup

## Known Limitations

- **Type Checker Support**: Generated functions may not be fully recognized by static type checkers
- **Global Namespace**: Functions are added to the provided namespace, which may cause conflicts
- **Dynamic Nature**: Runtime generation means some IDE features may not work perfectly

## Contributing

Contributions are welcome! Please feel free to:

1. Open an issue to report bugs or suggest features
2. Submit a pull request with improvements
3. Help improve type checking support
4. Add more examples and documentation

## License

EventRaisers is released under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

**EventRaisers** - Simplify your event-driven programming in Python! 🚀