from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum

import pandas as pd


class EventManager:
    """The main object used to run a backtest."""

    def __init__(self):
        self.event_queue: PriorityQueue[Event] = PriorityQueue()

    def run(self):
        """The main loop for handling events."""
        while not self.event_queue.empty:
            match self.event_queue.get_nowait().type:
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
    SIGNAL = 1
    ORDER = 2
    FILL = 3


@dataclass
class Event:
    timestamp: float
    type: EventType

