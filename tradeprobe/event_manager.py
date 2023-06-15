from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum


class EventManager:
    """The main object used to run a backtest."""

    def __init__(self):
        self.event_queue: PriorityQueue[Event] = PriorityQueue()

    def run(self):
        """The main loop for handling events."""
        while not self.event_queue.empty:
            match self.event_queue.get_nowait().type:
                case EventType.TICK:
                    pass
                case EventType.FILL:
                    pass
                case EventType.ORDER:
                    pass
                case EventType.SIGNAL:
                    pass
                case _:
                    # TODO: Throw error as this is invalid.
                    pass


class EventType(Enum):
    TICK = 1
    SIGNAL = 2
    ORDER = 3
    FILL = 4


@dataclass
class Event:
    timestamp: float
    type: EventType
