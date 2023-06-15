import queue
from datetime import datetime
from multiprocessing import Queue
from dataclasses import dataclass
from enum import Enum

from tradeprobe.broker import Broker
from tradeprobe.data_handler import DataHandler
from tradeprobe.portfolio import Portfolio


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


@dataclass
class MarketEvent(Event):
    """
    Handle receiving market updates.
    """


@dataclass
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


class TradingEngine:
    """The main object used to run a backtest."""

    def __init__(self, start_datetime, end_datetime, portfolio: Portfolio, broker: Broker, data_handler: DataHandler):
        self.portfolio = portfolio
        self.broker = broker
        self.data_handler: DataHandler = data_handler

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.current_datetime = self.start_datetime

        self.event_queue: Queue[Event] = Queue()

    def register_event(self, event: Event):
        self.event_queue.put_nowait(event)

    def run(self):
        """The main loop for handling events."""
        while self.current_datetime < self.end_datetime:
            [self.event_queue.put_nowait(bar) for bar in self.data_handler.get_bars()]
            self.current_datetime = self.data_handler.get_current_tick()

            while True:
                try:
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
                # No more events for this tick
                except queue.Empty:
                    break
