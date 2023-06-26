import queue
from queue import Queue
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SignalType(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'


class Direction(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


@dataclass
class Event(object):
    pass


class QueueEmptyEvent(Event):
    pass


@dataclass(eq=True)
class MarketEvent(Event):
    """
    Handle receiving market updates.
    """
    timestamp: datetime


@dataclass(eq=True)
class OLHCVIMarketEvent(MarketEvent):
    """Used to post market updates in the OLHCVI format."""
    timestamp: datetime
    symbol: str
    open: float
    low: float
    high: float
    close: float
    volume: int


@dataclass
class SignalEvent(Event):
    """
    Handle the sending of a Signal from a strategy object.
    Used by the portfolio to decide trades.
    """
    timestamp: datetime
    symbol: str
    signal_type: SignalType


@dataclass
class OrderEvent(Event):
    """Handle sending an Order."""
    timestamp: datetime
    symbol: str
    quantity: int
    direction: Direction

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("The order quantity must be non-negative.")

    def __str__(self):
        return f"Order: Symbol={self.symbol}, Quantity={self.quantity}, Direction={self.direction}"


@dataclass
class FillEvent(Event):
    """Encapsulate a filled order from a brokerage."""
    timestamp: datetime
    symbol: str
    quantity: int
    direction: Direction
    fill_price: float
    commission: float

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("The order quantity must be non-negative.")


class EventQueue(Queue):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.observers = {}

    def put(self, event: Event, block: bool = False, timeout: float | None = None) -> None:
        self.notify_observers(event)
        super().put(event, block, timeout)

    def register_observer(self, observer, event_type):
        if observer in self.observers:
            self.observers[observer].append(event_type)
        else:
            self.observers[observer] = [event_type]

    def notify_observers(self, event):
        for observer in self.observers:
            for event_type in self.observers[observer]:
                if isinstance(event_type, event):
                    observer.handle_event(event)

    def process_events(self):
        while True:
            try:
                event = self.get_nowait()
                self.notify_observers(event)
            except queue.Empty:
                self.put(QueueEmptyEvent())
                break
