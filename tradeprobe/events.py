from asyncio import Queue
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
    timestamp: datetime

    def __lt__(self, other):
        assert isinstance(other, Event)
        return self.timestamp < other.timestamp


@dataclass(eq=True)
class MarketEvent(Event):
    """
    Handle receiving market updates.
    """


@dataclass(eq=True)
class OLHCVIMarketEvent(MarketEvent):
    """Used to post market updates in the OLHCVI format."""
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
    symbol: str
    signal_type: SignalType


@dataclass
class OrderEvent(Event):
    """Handle sending an Order."""
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
    symbol: str
    quantity: int
    direction: Direction
    fill_price: float
    commission: float

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("The order quantity must be non-negative.")


class EventQueue:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__()
        return cls._instance

    def __init__(self):
        self.queue = Queue()

    def put_event(self, event: Event):
        self.queue.put_nowait(event)

    def get_event(self) -> Event:
        return self.queue.get_nowait()
