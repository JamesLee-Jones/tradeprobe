from datetime import datetime

import pytest

from tradeprobe.data_handler import CSVDataHandler
from tradeprobe.events import OLHCVIMarketEvent


@pytest.fixture
def csv_data_handler():
    return CSVDataHandler("./tests/data_handler", {'AAPL', 'META'})


class TestCSVDataHandler:
    def test_get_symbol_list(self, csv_data_handler):
        assert csv_data_handler.get_symbol_list() == {'AAPL', 'META'}

    def test_get_current_tick(self, csv_data_handler):
        assert csv_data_handler.get_current_tick() == datetime(2022, 6, 15)

    def test_get_bar(self, csv_data_handler):
        events = csv_data_handler.get_bars()
        assert OLHCVIMarketEvent(timestamp=datetime(2022, 6, 15),
                                 symbol='META',
                                 open=167.199997,
                                 high=172.160004,
                                 low=163.979996,
                                 close=169.350006,
                                 volume=30008300) in events
        assert OLHCVIMarketEvent(timestamp=datetime(2022, 6, 15),
                                 symbol='AAPL',
                                 open=134.289993,
                                 high=137.339996,
                                 low=132.160004,
                                 close=135.429993,
                                 volume=91533000) in events
        events = csv_data_handler.get_bars()
        assert OLHCVIMarketEvent(timestamp=datetime(2022, 6, 16),
                                 symbol='META',
                                 open=163.720001,
                                 high=165.080002,
                                 low=159.610001,
                                 close=160.869995,
                                 volume=26944100) in events
        assert OLHCVIMarketEvent(timestamp=datetime(2022, 6, 16),
                                 symbol='AAPL',
                                 open=132.080002,
                                 high=132.389999,
                                 low=129.039993,
                                 close=130.059998,
                                 volume=108123900) in events
