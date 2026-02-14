from event_raiser_gen import EventOf, EventDict, generate_event_raisers

# Define events
MY_EVENTS: EventDict = {
    "on_temperature_changed": [("temperature", float)],
    "on_humidity_changed": [("humidity", float)],
    "on_light_level_changed": [("light_level", int)],
}

# Hand-written stubs for event decorators and trigger functions
# NOTE: These stubs are required for type checking and IDE support
def on_temperature_changed(func: EventOf[float]) -> EventOf[float]: ...
def on_humidity_changed(func: EventOf[float]) -> EventOf[float]: ...
def on_light_level_changed(func: EventOf[int]) -> EventOf[int]: ...
def raise_on_temperature_changed(temperature: float) -> None: ...
def raise_on_humidity_changed(humidity: float) -> None: ...
def raise_on_light_level_changed(light_level: int) -> None: ...

# Generate event decorators and trigger functions
generate_event_raisers(MY_EVENTS, globals())


@on_temperature_changed
def handle_temperature_change(temp: float) -> None:
    print(f"Temperature changed to: {temp}°C")


@on_humidity_changed
def handle_humidity_change(humidity: float) -> None:
    print(f"Humidity changed to: {humidity}%")


@on_light_level_changed
def handle_light_level_change(light: int) -> None:
    print(f"Light level changed to: {light} lux")


if __name__ == "__main__":
    # Trigger events
    print("=== Triggering events ===")
    raise_on_temperature_changed(25.5)
    raise_on_humidity_changed(60.0)
    raise_on_light_level_changed(800)

    @on_temperature_changed
    def handle_temperature_error(_: float) -> None:
        raise ValueError("Intentionally triggered error")

    # Test error handling
    print("=== Testing error handling ===")
    # Error handled and logged automatically
    raise_on_temperature_changed(30.0)