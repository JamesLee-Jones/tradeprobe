from abc import ABCMeta, abstractmethod

from tradeprobe.events import Event, EventQueue


class Portfolio(object):
    """
    An abstract class to hold the position and market value of
    all instruments at the resolution of a bar.
    """

    __metaclass__ = ABCMeta

    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.event_queue = EventQueue()

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
        self.current_positions = {}
        self.current_holdings = {}

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
