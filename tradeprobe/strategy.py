from abc import ABCMeta, abstractmethod
from typing import List

from tradeprobe.events import SignalEvent, EventQueue


class Strategy:
    """
    An abstract base class to be inherited from.

    Generates signals for particular symbols based on inputs of bars.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.event_queue = EventQueue()

    @abstractmethod
    def calculate_signals(self) -> List[SignalEvent]:
        """
        Calculate a list of signals
        :return:  calculated by the strategy
        :type: List[SignalEvent]
        """
