# Python Event Raiser Code Generator

## Description
This project provides a lightweight and flexible Python package (`event_raiser_gen`) for dynamically generating event decorators and trigger functions for custom events. It allows developers to define custom events with specific parameters, register callback functions to those events via decorators, and trigger the events with auto-generated raise functions.

A few key points about the `event_raiser_gen` package:
- The package uses only Python's standard library (`typing`, `inspect`) - no external dependencies.
- The package is tested with Python 3.9+. It might work with older 3.x versions but is not guaranteed.
- The generated decorators and raiser functions are added directly to the provided namespace (typically the global scope of the calling module).

### Key Features
- Dynamically generate event decorators for registering callback functions
- Auto-create type-annotated event trigger functions (i.e. event raisers)
- Simple event registry management (clear/retrieve registered callbacks)
- Graceful error handling for callback execution failures
- No external dependencies (uses only Python standard library)

### Known Limitation
The auto-generated event trigger functions cannot be fully recognized by static type checkers (e.g., mypy, Pylance) due to dynamic signature modification. Attempts to resolve this by generating stub files (`.pyi` files) have not succeeded, and this limitation persists as an unavoidable tradeoff for the dynamic generation approach.

One possible solution is to manually write stubs for event raisers **before** they are generated:
```python
from event_raiser_gen import EventOf, EventDict, generate_event_raisers

# Define your custom events (name: list of (param_name, param_type) tuples)
CUSTOM_EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# Hand-written stubs for event decorators and trigger functions
# NOTE: These stubs are required for type checking and IDE support
def user_login(func: EventOf[int, float]) -> EventOf[int, float]: ...
def order_placed(func: EventOf[str, float]) -> EventOf[str, float]: ...
def raise_user_login(user_id: int, timestamp: float) -> None: ...
def raise_order_placed(order_id: str, total_amount: float) -> None: ...

# Generate decorators and raiser functions (adds to global namespace)
generate_event_raisers(CUSTOM_EVENTS, globals())
```

## Installation (From Source)
```bash
git clone https://github.com/Pac-Dessert1436/py-event-raiser-generator.git
cd py-event-raiser-generator
```
- Pure Python, standard library only
- No additional installation steps required

## Basic Usage
### 1. Define Events and Generate Raisers/Decorators
```python
from event_raiser_gen import EventOf, EventDict, generate_event_raisers

# Define your custom events (name: list of (param_name, param_type) tuples)
CUSTOM_EVENTS: EventDict = {
    "user_login": [("user_id", int), ("timestamp", float)],
    "order_placed": [("order_id", str), ("total_amount", float)]
}

# TODO: Write stubs for event decorators and trigger functions here.
#       This can prevent type checkers from reporting errors.

# Generate decorators and raiser functions (adds to global namespace)
generate_event_raisers(CUSTOM_EVENTS, globals())
```

### 2. Register Callback Functions
```python
# Use the generated decorator to register a callback for "user_login"
@user_login
def handle_user_login(user_id: int, timestamp: float) -> None:
    print(f"User {user_id} logged in at {timestamp}")

# Register another callback for "order_placed"
@order_placed
def handle_order_placed(order_id: str, total_amount: float) -> None:
    print(f"Order {order_id} placed (total: ${total_amount:.2f})")
```

### 3. Trigger Events
```python
# Use the generated raiser function to trigger the event
raise_user_login(user_id=123, timestamp=1718987654.123)
raise_order_placed(order_id="ORD-9876", total_amount=49.99)
```

### 4. Manage Event Registry
```python
from event_raiser_gen import get_event_registry, clear_event_registry

# Get all registered callbacks for an event
registry = get_event_registry()
print(f"Registered 'user_login' callbacks: {len(registry.get('user_login', []))}")

# Clear all registered event callbacks
clear_event_registry()
```

## API Reference
### Core Functions
#### `generate_event_raisers(events: EventDict, module_globals: ModuleGlobals) -> None`
Generates event decorators and trigger functions based on the provided event definition.
- **Parameters**:
  - `events`: Dictionary of events (keys = event names, values = list of (param_name, param_type) tuples)
  - `module_globals`: Global namespace of the module (use `globals()` to add functions to current scope)

#### `clear_event_registry() -> None`
Clears all registered event callbacks from the internal registry.

#### `get_event_registry() -> _EventRegistry`
Returns the current event registry (dictionary mapping event names to lists of registered callback functions).

### Type Aliases
#### `EventOf: TypeAlias = Callable[[Unpack[_Args]], None | Awaitable[None]]`
Type alias for event trigger functions (accepts any number of arguments, supports both synchronous and asynchronous callbacks).

#### `EventDict: TypeAlias = dict[str, _EventParams]`
Type alias for event definition dictionary (keys = event names, values = list of (param_name, param_type) tuples).

#### Private Type Aliases (For Reference)
- `_EventParams = list[tuple[str, Any]]`: List of parameter name/type tuples for an event
- `_EventRegistry = dict[str, list[Callable[..., Any | Awaitable[Any]]]]`: Internal registry of event-to-callbacks mapping, which supports both synchronous and asynchronous callbacks.

## Error Handling
When triggering events, any exceptions raised by registered callbacks are caught and printed to stdout (without interrupting other callbacks):
```
[NOTICE] Error in event 'user_login': [Exception message]
```

## Contributing
Contributions are welcome! Please open an issue to discuss proposed changes or submit a pull request with improvements. Note that the type checker limitation is a known issue and contributions to resolve it are particularly appreciated.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
