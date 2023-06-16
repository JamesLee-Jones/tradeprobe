from abc import ABCMeta, abstractmethod
from typing import List

from tradeprobe.events import SignalEvent


class Strategy:
    """
    An abstract base class to be inherited from.

    Generates signals for particular symbols based on inputs of bars.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self) -> List[SignalEvent]:
        """
        Calculate a list of signals
        :return:  calculated by the strategy
        :type: List[SignalEvent]
        """
