from typing import Callable
from threading import Lock
from dataclasses import dataclass
from collections import deque


@dataclass
class _EventItem:
    """
    Represents an event item with a priority.
    """
    event: Callable[[], None]
    priority: int = 0


class EventScheduler:
    """
    A simple queue-based event scheduler.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the EventScheduler class.
        """
        self.__pending_events: deque[_EventItem] = deque()
        self.__lock = Lock()

    def schedule_event_action(self, event_action: Callable[[], None], priority: int = 0) -> None:
        """
        Schedules an event action to be raised at a later time.
        """
        with self.__lock:
            self.__pending_events.append(_EventItem(event_action, priority))
            

    def raise_scheduled_events(self) -> None:
        """
        Raises all scheduled events in the order of their priority.
        """
        with self.__lock:
            self.__pending_events = \
                deque(sorted(self.__pending_events,
                    key=lambda x: x.priority, reverse=True))
            while self.__pending_events:
                self.__pending_events.popleft().event()

    @property
    def pending_event_count(self) -> int:
        """
        Gets the count of pending events.
        """
        with self.__lock:
            return len(self.__pending_events)
        
    def clear_scheduled_events(self) -> None:
        """
        Clears all scheduled events.
        """
        with self.__lock:
            self.__pending_events.clear()
