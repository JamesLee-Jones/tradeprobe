from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'


class Direction(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class EventManager:
    """The main object used to run a backtest."""

    def __init__(self):
        self.event_queue: PriorityQueue[Event] = PriorityQueue()

    def run(self):
        """The main loop for handling events."""
        while not self.event_queue.empty:
            match self.event_queue.get_nowait().__class__.__name__:
                case 'MarketEvent':
                    pass
                case 'SignalEvent':
                    pass
                case 'OrderEvent':
                    pass
                case 'FillEvent':
                    pass
                case _:
                    # TODO: Throw error as this is invalid.
                    pass


@dataclass
class Event(object):
    timestamp: float


class MarketEvent(Event):
    """
    Handle receiving market updates
    """


class SignalEvent(Event):
    """
    Handle the sending of a Signal from a strategy object.
    Used by the portfolio to decide trades.
    """
    symbol: str
    signal_type: SignalType


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
