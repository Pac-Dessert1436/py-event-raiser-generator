from typing import Callable, Any, TypeAlias, TypeVarTuple, Unpack, Awaitable
import inspect

_EventParams: TypeAlias = list[tuple[str, Any]]
# Extended event registry supporting synchronous and asynchronous callbacks
EventRegistry: TypeAlias = dict[str, list[Callable[..., Any | Awaitable[Any]]]]

_Args = TypeVarTuple("_Args")
# Extended event callback type - supports async functions
EventOf: TypeAlias = Callable[[Unpack[_Args]], None | Awaitable[None]]
EventDict: TypeAlias = dict[str, _EventParams]


class EventRaiserGenerator:
    """
    A class-based event generator that creates event decorators and trigger functions
    as instance attributes.
    
    This class encapsulates the event generation logic and manages the event registry,
    providing a cleaner API that works better with static type checkers.
    
    Usage:
        erg = EventRaiserGenerator()
        erg.generate_event_raisers(EVENTS)
        
        @erg.user_login
        def handle_login(user_id: int, timestamp: float) -> None:
            print(f"User {user_id} logged in at {timestamp}")
        
        erg.raise_user_login(user_id=123, timestamp=1718987654.123)
    """
    
    def __init__(self) -> None:
        """Initialize a new EventGenerator instance with an empty event registry."""
        self._event_registry: EventRegistry = {}
    
    def generate_event_raisers(self, events: EventDict) -> None:
        """
        Generate corresponding event decorators and trigger functions (sync/async) as 
        instance attributes based on the event dictionary.

        :param events: Event dictionary, format: `{"event_name": [("param_name", param_type), ...]}`
        """
        for event_name, params in events.items():
            self._generate_event_decorator(event_name)
            self._generate_async_raiser(event_name, params)
            self._generate_sync_raiser(event_name, params)
    
    def _generate_event_decorator(self, event_name: str) -> None:
        """Generate and register an event decorator as an instance attribute."""
        def decorator(func: EventOf) -> EventOf:
            if event_name not in self._event_registry:
                self._event_registry[event_name] = []
            self._event_registry[event_name].append(func)
            return func

        decorator.__name__ = event_name
        decorator.__doc__ = f"Register a callback function (sync/async) for the {event_name} event"
        setattr(self, event_name, decorator)
    
    def _generate_async_raiser(self, event_name: str, event_params: _EventParams) -> None:
        """Generate and register an async event trigger function as an instance attribute."""
        async def async_raiser(*args: Any, **kwargs: Any) -> None:
            for callback in self._event_registry.get(event_name, []):
                try:
                    if inspect.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    print(f"[NOTICE] Error in event '{event_name}':", e)

        sig_params = []
        for param_name, param_type in event_params:
            sig_params.append(inspect.Parameter(
                param_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=param_type
            ))
        async_raiser.__signature__ = inspect.Signature(sig_params)
        async_raiser.__name__ = f"raise_{event_name}_async"
        async_raiser.__doc__ = f"Asynchronously trigger the {event_name} event (supports sync/async callbacks)"
        setattr(self, f"raise_{event_name}_async", async_raiser)
    
    def _generate_sync_raiser(self, event_name: str, event_params: _EventParams) -> None:
        """Generate and register a synchronous event trigger function as an instance attribute."""
        def sync_raiser(*args: Any, **kwargs: Any) -> None:
            for callback in self._event_registry.get(event_name, []):
                try:
                    if inspect.iscoroutinefunction(callback):
                        print(f"[WARNING] Async callback in sync raiser '{event_name}' - will not be awaited")
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"[NOTICE] Error in event '{event_name}':", e)

        sig_params = []
        for param_name, param_type in event_params:
            sig_params.append(inspect.Parameter(
                param_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=param_type
            ))
        sync_raiser.__signature__ = inspect.Signature(sig_params)
        sync_raiser.__name__ = f"raise_{event_name}"
        sync_raiser.__doc__ = f"Trigger the {event_name} event (async callbacks are not awaited)"
        setattr(self, f"raise_{event_name}", sync_raiser)
    
    def clear_event_registry(self) -> None:
        """Clear the event registry"""
        self._event_registry.clear()
    
    def get_event_registry(self) -> EventRegistry:
        """Get the event registry (includes sync/async callbacks)"""
        return self._event_registry
    
    def __getattr__(self, name: str) -> Any:
        """
        Dynamically resolve event decorators and trigger functions.
        
        This method tells static type checkers that any attribute access on EventGenerator
        is valid and will return a callable. This is similar to how PyGame's event.key works.
        
        :param name: The name of the attribute to get
        :return: The event decorator or trigger function
        :raises AttributeError: If the attribute doesn't exist
        """
        raise AttributeError(
            f"'EventRaiserGenerator' object has no attribute '{name}'. Did you forget to call generate_event_raisers()?")


# Global instance for backward compatibility
_global_generator = EventRaiserGenerator()

def generate_event_raisers(events: EventDict, module_globals: dict[str, Any]) -> None:
    """
    Generate corresponding event decorators and trigger functions (sync/async) based on the 
    event dictionary.
    
    This function maintains backward compatibility with version 1.0.x by using a global 
    EventRaiserGenerator instance. It generates events and adds them to the provided module
    globals.

    :param events: Event dictionary, format: `{"event_name": [("param_name", param_type), ...]}`
    :param module_globals: The global namespace of the module, used to add generated functions
    """
    _global_generator.generate_event_raisers(events)
    for event_name in events.keys():
        module_globals[event_name] = getattr(_global_generator, event_name)
        module_globals[f"raise_{event_name}_async"] = getattr(_global_generator, f"raise_{event_name}_async")
        module_globals[f"raise_{event_name}"] = getattr(_global_generator, f"raise_{event_name}")


def clear_event_registry() -> None:
    """Clear the event registry"""
    _global_generator.clear_event_registry()


def get_event_registry() -> EventRegistry:
    """Get the event registry (includes sync/async callbacks)"""
    return _global_generator.get_event_registry()