# EventRaisers (`eventraisers`) - Dynamic Event System for Python

[![PyPI version](https://img.shields.io/pypi/v/eventraisers.svg)](https://pypi.org/project/eventraisers/)
[![Python versions](https://img.shields.io/pypi/pyversions/eventraisers.svg)](https://pypi.org/project/eventraisers/)
[![License](https://img.shields.io/pypi/l/eventraisers.svg)](https://pypi.org/project/eventraisers/)

**EventRaisers** (formerly "py-event-raiser-generator") is a lightweight, zero-dependency Python library that dynamically generates event decorators and trigger functions at runtime. Define your events once, and EventRaisers automatically creates the necessary infrastructure for event registration and triggering.

> **Fun Fact**: This Python library is heavily inspired by the NuGet package [ModuleEventRaiser.Generator](https://www.nuget.org/packages/ModuleEventRaiser.Generator/) that was designed for VB.NET.

## 🎉 What's New in 1.1.0

**EventRaisers 1.1.0** introduces a major architectural improvement with the new `EventRaiserGenerator` class, providing better static type checker support and a cleaner, more maintainable API:

- ✨ **New Class-Based API** - `EventRaiserGenerator` class with instance attributes for decorators and triggers
- 🔄 **Backward Compatible with 1.0.x** - Existing code using function-based API continues to work on the latest version without changes
- 🎯 **Better Type Safety** - Full static type checker support with instance-based event registration
- 🏗️ **Cleaner Architecture** - Encapsulated event generation logic with instance-based registries
- 📦 **Multiple Instances** - Create multiple independent event generators for different contexts
- 🔍 **Instance Attributes** - Events are now `@erg.event_name` and triggers are `erg.raise_event_name()`

## Key Features

🚀 **Dynamic Generation** - Automatically create event decorators and trigger functions from simple definitions

⚡ **Zero Dependencies** - Built entirely on Python's standard library (`typing`, `inspect`)

🔧 **Type Annotated** - Full type hint support for better IDE integration and code clarity

🔄 **Async/Sync Support** - Handle both synchronous and asynchronous callback functions

⏰ **Event Scheduling** - Built-in priority-based event scheduling system

🏗️ **Class-Based API** - New in 1.1.0: `EventRaiserGenerator` class for better type checker compatibility

🐍 **Python 3.9+** - Compatible with Python 3.9 through 3.14

## Quick Start

### Using the New `EventRaiserGenerator` Class (Recommended)

```python
from eventraisers import EventRaiserGenerator, EventDict

# Create an EventRaiserGenerator instance
erg = EventRaiserGenerator()

# Define your events
EVENT_DICT: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# Generate decorators and trigger functions as dynamic attributes
erg.generate_event_raisers(EVENT_DICT)

# Register event handlers using dynamic attributes
@erg.user_login
def handle_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

# Trigger events using dynamic attributes
erg.raise_user_login(user_id=123, timestamp=1718987654.123)
```

### Using the Function-Based API (Backward Compatible with 1.0.x)

```python
from eventraisers import EventDict, generate_event_raisers

# Define your events
EVENT_DICT: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# Generate decorators and trigger functions (uses global generator)
generate_event_raisers(EVENT_DICT, globals())

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

### 1. Using the `EventRaiserGenerator` Class

The new `EventRaiserGenerator` class provides a clean, instance-based approach to event generation with full static type checker support:

```python
from eventraisers import EventRaiserGenerator, EventDict

# Create an EventRaiserGenerator instance
erg = EventRaiserGenerator()

# Define events with their parameter names and types
EVENT_DICT: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)],
    "system_alert": [("message", str), ("severity", str)]
}

# Generate the event infrastructure as instance attributes
erg.generate_event_raisers(EVENT_DICT)

# Register event handlers using instance attributes
@erg.user_login
def handle_user_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

@erg.order_placed  
def handle_order_placed(order_id: str, total_amount: float) -> None:
    print(f"Order {order_id} placed (total: ${total_amount:.2f})")

# Trigger events using instance attributes
erg.raise_user_login(user_id=123, timestamp=1718987654.123)
erg.raise_order_placed(order_id="ORD-9876", total_amount=49.99)

# Access the event registry
registry = erg.get_event_registry()
print(f"Registered callbacks: {len(registry.get('user_login', []))}")

# Clear the event registry when needed
erg.clear_event_registry()
```

### 2. Multiple Independent Event Generators

Create multiple isolated event generators for different contexts:

```python
from eventraisers import EventRaiserGenerator, EventDict

# Create separate generators for different contexts
user_events = EventRaiserGenerator()
system_events = EventRaiserGenerator()

# Define different events for each context
USER_EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "user_logout": [("user_id", int)]
}

SYSTEM_EVENTS: EventDict = {
    "system_alert": [("message", str), ("severity", str)],
    "system_shutdown": [("reason", str)]
}

# Generate events as instance attributes
user_events.generate_event_raisers(USER_EVENTS)
system_events.generate_event_raisers(SYSTEM_EVENTS)

# Register handlers using instance attributes
@user_events.user_login
def handle_user_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

@system_events.system_alert
def handle_system_alert(message: str, severity: str) -> None:
    print(f"[{severity.upper()}] {message}")

# Trigger events using instance attributes
user_events.raise_user_login(user_id=123, timestamp=1718987654.123)
system_events.raise_system_alert(message="Low memory", severity="warning")

# Each generator maintains its own registry
user_registry = user_events.get_event_registry()
system_registry = system_events.get_event_registry()

# Clear one registry without affecting the other
user_events.clear_event_registry()  # Only clears user events
```

### 3. Backward Compatibility

The function-based API from version 1.x continues to work without changes:

```python
from eventraisers import EventDict, generate_event_raisers

EVENT_DICT: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)]
}

# Generate event raise functions using the global generator
generate_event_raisers(EVENT_DICT, globals())

@user_login
def handle_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

raise_user_login(user_id=123, timestamp=1718987654.123)

# Access the global registry
from eventraisers import get_event_registry
registry = get_event_registry()

# Clear the global registry
from eventraisers import clear_event_registry
clear_event_registry()
```

### 4. Event Scheduling

Schedule events with priority-based execution using the `EventScheduler` class:

```python
from eventraisers import EventScheduler

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

# Clear scheduled events
scheduler.clear_scheduled_events()
```

### 5. Asynchronous Event Handling

EventRaisers supports both synchronous and asynchronous callback functions:

```python
from eventraisers import EventRaiserGenerator, EventDict
import asyncio

erg = EventRaiserGenerator()

EVENT_DICT: EventDict = {
    "data_received": [("data", str), ("source", str)],
    "async_process": [("task_id", int)]
}

erg.generate_event_raisers(EVENT_DICT)

# Synchronous handler
@erg.data_received
def handle_data_sync(data: str, source: str) -> None:
    print(f"[SYNC] Data from {source}: {data}")

# Asynchronous handler
@erg.data_received
async def handle_data_async(data: str, source: str) -> None:
    await asyncio.sleep(0.1)
    print(f"[ASYNC] Processed data from {source}: {data}")

# Use async raiser for better async support
async def main():
    await erg.raise_data_received_async(data="Hello", source="sensor")
    await erg.raise_data_received_async(data="World", source="api")

asyncio.run(main())
```

## API Reference

### `EventRaiserGenerator` Class

The main class for generating event decorators and trigger functions as instance attributes.

#### `EventRaiserGenerator()`
Creates a new EventRaiserGenerator instance with an empty event registry.

#### `generate_events(events: EventDict) -> None`
Generates event decorators and trigger functions as instance attributes based on the provided event definitions.

**Parameters:**
- `events`: Dictionary mapping event names to parameter specifications

#### `get_event_registry() -> EventRegistry`
Returns the current event registry as a dictionary mapping event names to lists of registered callbacks.

#### `clear_event_registry() -> None`
Clears all registered event callbacks from the internal registry.

### Core Functions (Backward Compatibility)

#### `generate_event_raisers(events: EventDict, module_globals: dict[str, Any]) -> None`
Generates event decorators and trigger functions using a global EventRaiserGenerator instance.

#### `clear_event_registry() -> None`
Clears all registered event callbacks from the global registry.

#### `get_event_registry() -> EventRegistry`
Returns the current global event registry.

### Type Aliases

#### `EventOf: TypeAlias = Callable[[Unpack[_Args]], None | Awaitable[None]]`
Generic type for event callback functions, supporting both synchronous and asynchronous handlers.

#### `EventDict: TypeAlias = dict[str, list[tuple[str, Any]]]`
Type for event definition dictionaries (event name → parameter specifications).

#### `EventRegistry: TypeAlias = dict[str, list[Callable[..., Any | Awaitable[Any]]]]`
Type for the event registry mapping event names to lists of registered callbacks.

### `EventScheduler` Class

Queue-based event scheduling system with priority support.

#### `EventScheduler()`
Creates a new event scheduler instance.

#### `schedule_event_action(event_action: Callable[[], None], priority: int = 0) -> None`
Schedules an event action with the specified priority (higher numbers execute first).

#### `raise_scheduled_events() -> None`
Executes all scheduled events in priority order.

#### `clear_scheduled_events() -> None`
Clears all scheduled events from the scheduler.

#### `pending_event_count: int` (property)
Returns the number of pending events in the scheduler.

## Migration Guide

### Migrating from 1.0.x to 1.1.0

The migration to 1.1.0 is straightforward and backward compatible:

**Option 1: Keep Existing Code (No Changes Required)**
```python
# Your existing code continues to work
from eventraisers import EventDict, generate_event_raisers

EVENTS: EventDict = {"user_login": [("user_id", int)]}
generate_event_raisers(EVENTS, globals())

@user_login
def handle_login(user_id: int) -> None:
    print(f"User {user_id} logged in")

raise_user_login(user_id=123)
```

**Option 2: Adopt EventRaiserGenerator Class (Recommended)**
```python
# New recommended approach with instance attributes
from eventraisers import EventRaiserGenerator, EventDict

erg = EventRaiserGenerator()
EVENT_DICT: EventDict = {"user_login": [("user_id", int)]}
erg.generate_event_raisers(EVENT_DICT)

@erg.user_login
def handle_login(user_id: int) -> None:
    print(f"User {user_id} logged in")

erg.raise_user_login(user_id=123)
```

**Key Changes in 1.1.0:**
- Events are now instance attributes: `@generator.event_name` instead of `@event_name`
- Event triggers are instance methods: `generator.raise_event_name()` instead of `raise_event_name()`
- Use `generator.generate_events()` instead of `generator.generate_event_raisers(events, globals())`
- Better static type checker support with instance-based API

**Key Benefits of Migration:**
- Better static type checker support
- Instance-based registries for better isolation
- Cleaner API design
- Improved IDE autocomplete
- Full type inference for event handlers

## Advanced Features

### Type Checking Support

The new `EventRaiserGenerator` class provides better type checking support with instance attributes:

```python
from eventraisers import EventRaiserGenerator, EventDict, EventOf

erg = EventRaiserGenerator()

EVENT_DICT: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

erg.generate_event_raisers(EVENT_DICT)

# Type checkers can now properly infer callback signatures
@erg.user_login
def handle_user_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

# Static type checkers recognize these as instance attributes
erg.raise_user_login(user_id=123, timestamp=1718987654.123)
erg.raise_order_placed(order_id="ORD-9876", total_amount=49.99)
```

### Error Handling

EventRaisers provides graceful error handling - exceptions in callbacks don't interrupt other handlers:

```python
@erg.user_login
def problematic_handler(user_id: int, timestamp: float) -> None:
    raise ValueError("Something went wrong!")

@erg.user_login  
def working_handler(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} handled successfully")

# Both handlers are called, errors are logged but don't stop execution
erg.raise_user_login(user_id=123, timestamp=1718987654.123)
# Output: [NOTICE] Error in event 'user_login': Something went wrong!
# Output: User 123 handled successfully
```

## Use Cases

EventRaisers is ideal for:

- **Plugin Systems** - Allow plugins to register event handlers with isolated contexts
- **Game Development** - Handle game events like collisions, achievements, etc.
- **Web Applications** - Process user actions, notifications, and system events
- **IoT Applications** - Handle sensor data and device state changes
- **Microservices** - Coordinate actions between different service components
- **Event-Driven Architecture** - Implement clean event-driven patterns with type safety

## Best Practices

1. **Use Class-Based API** - Prefer the class-based API (the `EventRaiserGenerator` class) for better type safety and isolation
2. **Define events early** - Generate event infrastructure at module initialization
3. **Use descriptive event names** - Make events self-documenting
4. **Leverage multiple instances** - Use separate generators for different contexts
5. **Handle errors gracefully** - Use the built-in error handling for robust applications
6. **Clear registries when needed** - Use `clear_event_registry()` for cleanup
7. **Choose appropriate raisers** - Use async raisers for async-heavy applications

## Known Limitations

- **Generated Functions**: Dynamically generated functions may not be fully recognized by all static type checkers (improved in 1.1.0)
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

**EventRaisers 1.1.0** - Simplify your event-driven programming in Python with better type safety! 🚀