import unittest
from datetime import time, datetime
from queue import Queue
from unittest.mock import patch, MagicMock

import pytest

from tradeprobe.events import EventQueue, Event


@pytest.fixture
def event_queue():
    return EventQueue()


class TestEventQueue(unittest.TestCase):
    # Most things don't need to be tested since it uses a standard
    # python queue.

    def test_singleton_instance(self):
        queue1 = EventQueue()
        queue2 = EventQueue()

        self.assertIs(queue1, queue2)
        self.assertIsInstance(queue1, Queue)
        self.assertIsInstance(queue2, Queue)

    def test_queue_operations(self):
        mock_event = MagicMock(spec=Event)
        event1: Event = mock_event()
        event2: Event = mock_event()

        with patch('tradeprobe.events.Event', return_value=mock_event):
            queue = EventQueue()

            queue.put(event1)
            queue.put(event2)

            self.assertEqual(queue.qsize(), 2)
            self.assertFalse(queue.empty())

            event1 = queue.get()
            event2 = queue.get()

            self.assertEqual(event1, event1)
            self.assertEqual(event2, event2)
            self.assertTrue(queue.empty())
