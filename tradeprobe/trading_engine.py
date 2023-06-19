import queue
from multiprocessing import Queue

from tradeprobe.broker import Broker
from tradeprobe.data_handler import DataHandler
from tradeprobe.events import Event, EventQueue
from tradeprobe.portfolio import Portfolio


class TradingEngine:
    """The main object used to run a backtest."""

    def __init__(self, start_datetime, end_datetime, portfolio: Portfolio, broker: Broker, data_handler: DataHandler):
        self.portfolio = portfolio
        self.broker = broker
        self.data_handler: DataHandler = data_handler

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.current_datetime = self.start_datetime

        self.event_queue: EventQueue = EventQueue()

    def run(self):
        """The main loop for handling events."""
        while self.current_datetime < self.end_datetime:
            self.current_datetime = self.data_handler.get_current_tick()

            while True:
                try:
                    match self.event_queue.get_event().__class__.__name__:
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
