from typing import Callable, Any, TypeAlias, TypeVarTuple, Unpack
import inspect

_EventParams: TypeAlias = list[tuple[str, Any]]
_ModuleGlobals: TypeAlias = dict[str, Any]
_NestedCallable: TypeAlias = Callable[[Callable], Callable]
_EventRegistry: TypeAlias = dict[str, list[Callable]]

_Args = TypeVarTuple("_Args")
# Type alias for event callback functions
# EXAMPLE: EventOf[int, float] = Callable[[int, float], None]
EventOf: TypeAlias = Callable[[Unpack[_Args]], None]
EventDict: TypeAlias = dict[str, _EventParams]

_event_registry: _EventRegistry = {}


def generate_event_raisers(events: EventDict, module_globals: _ModuleGlobals) -> None:
    """
    Generate corresponding event decorators and trigger functions based on the EVENTS dictionary.

    :param events: Event dictionary, format: `{"event_name": [("param_name", param_type), ...]}`
    :param module_globals: The global namespace of the module, used to add generated functions
    :param generate_stubs: Whether to generate stub file, default is False
    :param module_name: Module name used for generating stub file name, default is "events"
    """
    for event_name, params in events.items():
        # Generate decorator function
        def create_decorator(name: str) -> _NestedCallable:
            def decorator(func: Callable) -> Callable:
                if name not in _event_registry:
                    _event_registry[name] = []
                _event_registry[name].append(func)
                return func
            return decorator

        # Generate trigger function
        def create_raiser(name: str, event_params: _EventParams) -> Callable:
            def raiser(*args: Any, **kwargs: Any) -> None:
                for callback in _event_registry.get(name, []):
                    try:
                        callback(*args, **kwargs)
                    except Exception as e:
                        print(f"[NOTICE] Error in event '{name}':", e)

            # Set function signature
            sig_params = []
            for param_name, param_type in event_params:
                sig_params.append(inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type
                ))

            raiser.__signature__ = inspect.Signature(sig_params)
            raiser.__name__ = f"raise_{name}"
            raiser.__doc__ = f"Trigger the {name} event"

            return raiser

        # Create and add decorator function to module namespace
        decorator_func = create_decorator(event_name)
        decorator_func.__name__ = event_name
        decorator_func.__doc__ = f"Register a callback function for the {event_name} event"
        module_globals[event_name] = decorator_func

        # Create and add trigger function to module namespace
        raiser_func = create_raiser(event_name, params)
        module_globals[f"raise_{event_name}"] = raiser_func


def clear_event_registry() -> None:
    """
    Clear the event registry
    """
    _event_registry.clear()


def get_event_registry() -> _EventRegistry:
    """
    Get the event registry

    :return: Event registry dictionary
    """
    return _event_registry
