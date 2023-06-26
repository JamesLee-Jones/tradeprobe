from abc import ABCMeta, abstractmethod

from tradeprobe.events import Event, EventQueue, MarketEvent, SignalEvent, FillEvent
from tradeprobe.observer import Observer


class Portfolio(Observer):
    """
    An abstract class to hold the position and market value of
    all instruments at the resolution of a bar.
    """

    __metaclass__ = ABCMeta

    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.event_queue = EventQueue()
        self.current_positions = {}
        self.current_holdings = {}

        self.event_queue.register_observer(self, MarketEvent)
        self.event_queue.register_observer(self, SignalEvent)
        self.event_queue.register_observer(self, FillEvent)

    @abstractmethod
    def update_on_signal(self, event: Event):
        """
        Acts on a signal event to generate orders.
        """
        raise NotImplementedError("Implement update_on_signal()")

    @abstractmethod
    def update_on_fill(self, event: Event):
        """
        Update the portfolio's current position based on fill events.
        """
        raise NotImplementedError("Implement update_on_fill()")

    @abstractmethod
    def update_timeindex(self, event: MarketEvent):
        """
        Add a new record to the positions matrix for current market data
        bar.
        """

    def handle_event(self, event):
        if isinstance(event, MarketEvent):
            self.update_timeindex(event)
        elif isinstance(event, SignalEvent):
            self.update_on_signal(event)
        elif isinstance(event, FillEvent):
            self.update_on_fill(event)


class NaivePortfolio(Portfolio):
    """
    A Portfolio that will send order to a brokerage with a constant
    quantity and size.

    This includes no risk management or position sizing and should
    not be used in practice.

    It is useful for testing simpler strategies, such as BuyAndHoldStrategy.
    """

    def __init__(self, initial_capital=100000):
        super().__init__(initial_capital)

    @abstractmethod
    def update_on_signal(self, event: Event):
        """
        Acts on a signal event to generate orders.
        """
        raise NotImplementedError("Implement update_on_signal()")

    @abstractmethod
    def update_on_fill(self, event: Event):
        """
        Update the portfolio's current position based on fill events.
        """
        raise NotImplementedError("Implement update_on_fill()")
