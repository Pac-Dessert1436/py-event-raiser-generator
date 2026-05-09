from eventraisers import (
    EventDict, EventRaiserGenerator, EventScheduler
)

# Define events
MY_EVENTS: EventDict = {
    "on_temperature_changed": [("temperature", float)],
    "on_humidity_changed": [("humidity", float)],
    "on_light_level_changed": [("light_level", int)],
}

# Create an EventRaiserGenerator instance
erg = EventRaiserGenerator()

# Generate event decorators and trigger functions as instance attributes
erg.generate_event_raisers(MY_EVENTS)


@erg.on_temperature_changed
def handle_temperature_change(temp: float) -> None:
    print(f"Temperature changed to: {temp}°C")


@erg.on_humidity_changed
def handle_humidity_change(humidity: float) -> None:
    print(f"Humidity changed to: {humidity}%")


@erg.on_light_level_changed
def handle_light_level_change(light: int) -> None:
    print(f"Light level changed to: {light} lux")


scheduler = EventScheduler()
if __name__ == "__main__":
    # Trigger events using instance attributes
    print("=== Triggering events ===")
    erg.raise_on_temperature_changed(25.5)
    erg.raise_on_humidity_changed(60.0)
    erg.raise_on_light_level_changed(800)

    @erg.on_temperature_changed
    def handle_temperature_error(_: float) -> None:
        raise ValueError("Intentionally triggered error")

    # Test error handling
    print("=== Testing error handling ===")
    # Error handled and logged automatically
    erg.raise_on_temperature_changed(30.0)

    # Test event scheduling
    print("=== Testing event scheduling ===")
    scheduler.schedule_event_action(
        lambda: erg.raise_on_temperature_changed(35.0), 20
    )
    scheduler.schedule_event_action(
        lambda: erg.raise_on_humidity_changed(70.0), 40
    )
    scheduler.schedule_event_action(
        lambda: erg.raise_on_light_level_changed(1200), 60
    )
    print(f"Pending event count: {scheduler.pending_event_count}")
    scheduler.raise_scheduled_events()
    print(f"Pending event count after raise: {scheduler.pending_event_count}")
    
    # Demonstrate registry management of EventRaiserGenerator
    print("=== Testing `EventRaiserGenerator` registry ===")
    registry = erg.get_event_registry()
    print(f"Registered 'on_temperature_changed' callbacks: {len(registry.get('on_temperature_changed', []))}")
    erg.clear_event_registry()
    print(f"After clearing - Registered callbacks: {len(registry.get('on_temperature_changed', []))}")