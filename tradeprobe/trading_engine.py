from tradeprobe.events import EventQueue, Event
from tradeprobe.observer import Observer


class TradingEngine(Observer):
    """The main object used to run a backtest."""

    def __init__(self, start_datetime, end_datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.current_datetime = self.start_datetime

        self.event_queue: EventQueue = EventQueue()

        self.event_queue.register_observer(self, Event)

    def handle_event(self, event):
        self.current_datetime = event.timestamp

    def run(self):
        """The main loop for handling events."""
        while self.current_datetime < self.end_datetime:
            self.event_queue.process_events()
