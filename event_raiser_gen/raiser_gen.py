from typing import Callable, Any, TypeAlias, TypeVarTuple, Unpack, Awaitable
import inspect

_EventParams: TypeAlias = list[tuple[str, Any]]
_ModuleGlobals: TypeAlias = dict[str, Any]
_NestedCallable: TypeAlias = Callable[[Callable], Callable]
# Extended event registry supporting synchronous and asynchronous callbacks
_EventRegistry: TypeAlias = dict[str, list[Callable[..., Any | Awaitable[Any]]]]

_Args = TypeVarTuple("_Args")
# Extended event callback type - supports async functions
EventOf: TypeAlias = Callable[[Unpack[_Args]], None | Awaitable[None]]
EventDict: TypeAlias = dict[str, _EventParams]

_event_registry: _EventRegistry = {}


def generate_event_raisers(events: EventDict, module_globals: _ModuleGlobals) -> None:
    """
    Generate corresponding event decorators and trigger functions (sync/async) based on the EVENTS dictionary.

    :param events: Event dictionary, format: `{"event_name": [("param_name", param_type), ...]}`
    :param module_globals: The global namespace of the module, used to add generated functions
    """
    for event_name, params in events.items():
        # Generate event decorator for sync/async callbacks
        def create_decorator(name: str) -> _NestedCallable:
            def decorator(func: EventOf) -> EventOf:
                if name not in _event_registry:
                    _event_registry[name] = []
                _event_registry[name].append(func)
                return func

            decorator.__name__ = name
            decorator.__doc__ = f"Register a callback function (sync/async) for the {name} event"
            return decorator

        # Generate async event trigger function
        def create_async_raiser(name: str, event_params: _EventParams) -> Callable[..., Awaitable[None]]:
            async def async_raiser(*args: Any, **kwargs: Any) -> None:
                # Iterate through all registered callbacks
                for callback in _event_registry.get(name, []):
                    try:
                        # Execute with 'await' for async callbacks, direct call for sync callbacks
                        if inspect.iscoroutinefunction(callback):
                            await callback(*args, **kwargs)
                        else:
                            callback(*args, **kwargs)
                    except Exception as e:
                        print(f"[NOTICE] Error in event '{name}':", e)

            # Set function signature to match event parameters
            sig_params = []
            for param_name, param_type in event_params:
                sig_params.append(inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type
                ))
            async_raiser.__signature__ = inspect.Signature(sig_params)
            async_raiser.__name__ = f"raise_{name}_async"
            async_raiser.__doc__ = f"Asynchronously trigger the {name} event (supports sync/async callbacks)"
            return async_raiser

        # Generate synchronous event trigger function
        def create_sync_raiser(name: str, event_params: _EventParams) -> Callable:
            def sync_raiser(*args: Any, **kwargs: Any) -> None:
                for callback in _event_registry.get(name, []):
                    try:
                        # Produce a warning for async callbacks in sync raiser
                        if inspect.iscoroutinefunction(callback):
                            print(f"[WARNING] Async callback in sync raiser '{name}' - will not be awaited")
                        callback(*args, **kwargs)
                    except Exception as e:
                        print(f"[NOTICE] Error in event '{name}':", e)

            sig_params = []
            for param_name, param_type in event_params:
                sig_params.append(inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type
                ))
            sync_raiser.__signature__ = inspect.Signature(sig_params)
            sync_raiser.__name__ = f"raise_{name}"
            sync_raiser.__doc__ = f"Trigger the {name} event (async callbacks are not awaited)"
            return sync_raiser
        
        # Add event decorator and trigger functions to module globals
        module_globals[event_name] = create_decorator(event_name)
        module_globals[f"raise_{event_name}_async"] = create_async_raiser(event_name, params)
        module_globals[f"raise_{event_name}"] = create_sync_raiser(event_name, params)


def clear_event_registry() -> None:
    """Clear the event registry"""
    _event_registry.clear()


def get_event_registry() -> _EventRegistry:
    """Get the event registry (includes sync/async callbacks)"""
    return _event_registry