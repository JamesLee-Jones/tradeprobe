from abc import ABCMeta, abstractmethod
from typing import List

from tradeprobe.events import SignalEvent, EventQueue, MarketEvent
from tradeprobe.observer import Observer


class Strategy(Observer):
    """
    An abstract base class to be inherited from.

    Generates signals for particular symbols based on inputs of bars.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.event_queue = EventQueue()
        self.event_queue.register_observer(self, MarketEvent)

    @abstractmethod
    def calculate_signals(self, event: MarketEvent) -> List[SignalEvent]:
        """
        Calculate a list of signals
        :return:  calculated by the strategy
        :type: List[SignalEvent]
        """
        raise NotImplementedError("Implement calculate_signals()")

    def handle_event(self, event):
        # The Strategy object only cares about MarketEvents
        if isinstance(event, MarketEvent):
            self.calculate_signals(event)
