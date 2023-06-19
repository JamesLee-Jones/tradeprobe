import os.path
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Set, Generator, Any, Iterable

import pandas as pd
from pandas import Series

from tradeprobe.events import OLHCVIMarketEvent, MarketEvent, EventQueue


class DataHandler(object):
    """
    An abstract base class for data handlers.
    """

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.event_queue: EventQueue = EventQueue()

    @abstractmethod
    def get_bars(self) -> None:
        """Get the next available bar from the data source."""
        raise NotImplementedError("Implement get_next_bar().")

    @abstractmethod
    def get_symbol_list(self) -> Set[str]:
        """Get the list of available symbols."""
        raise NotImplementedError("Implement get_next_bar().")

    @abstractmethod
    def get_current_tick(self) -> datetime:
        """Get the frequency of the data."""
        raise NotImplementedError("Implement get_data_frequency().")


class CSVDataHandler(DataHandler):
    """

    """

    def __init__(self, csv_dir: str, symbol_list: Set[str]):
        super().__init__()

        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        # Dictionary mapping symbol to data
        self.symbol_data: dict[str, Iterable[tuple[datetime, Series]]] = {}

        self.current_tick: datetime = datetime.now()
        self._open_and_convert_csv_files()

    def _open_and_convert_csv_files(self):
        """

        :return:
        """
        # Initialize combined index and symbol data dictionary
        comb_index = None
        symbol_data = {}
        set_datetime = False

        # Loop through each symbol
        for symbol in self.symbol_list:
            # Construct file path for the symbol's CSV file
            file_path = os.path.join(self.csv_dir, f"{symbol}.csv")

            # Read CSV file into a DataFrame
            df = pd.read_csv(file_path, header=0, index_col=0, parse_dates=True,
                             names=['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])

            # Combine index values from different symbols into the combined index
            if comb_index is None:
                comb_index = df.index
            else:
                comb_index = comb_index.union(df.index)

            # Sort DataFrame based on the index
            df.sort_index(inplace=True)

            # Reindex DataFrame to align with the combined index and forward-fill missing values
            df = df.reindex(index=comb_index, method='pad')

            # Set the current tick without advancing the iterator
            if not set_datetime:
                self.current_tick = df.index.min()
                set_datetime = True

            # Calculate returns and drop rows with missing values
            df["returns"] = df["adj_close"].pct_change().dropna()

            # Store the DataFrame as an iterator in the symbol data dictionary
            symbol_data[symbol] = df.iterrows()

        # Update the symbol data dictionary of the backtesting framework
        self.symbol_data = symbol_data

    def _get_next_bar(self, symbol) -> Generator[MarketEvent, Any, None]:
        """
        Return the latest bar of the data feed as a MarketEvent.
        :return:
        """
        for i in self.symbol_data[symbol]:
            # TODO: Do this in a nicer way
            self.current_tick = i[0]
            yield OLHCVIMarketEvent(timestamp=self.current_tick,
                                    symbol=symbol,
                                    open=i[1][0],
                                    high=i[1][1],
                                    low=i[1][2],
                                    close=i[1][3],
                                    volume=i[1][5])

    def get_bars(self) -> None:
        """Get the next available bar from the data source."""
        for symbol in self.symbol_list:
            try:
                event = next(self._get_next_bar(symbol))
            except StopIteration:
                # Stop using this datasource as it is empty
                pass
            else:
                if event is not None:
                    self.event_queue.put_event(event)

    def get_symbol_list(self) -> Set[str]:
        """Get the list of available symbols."""
        return self.symbol_list

    def get_current_tick(self) -> datetime:
        """Get the frequency of the data."""
        return self.current_tick


class MultiSourceDataHandler(DataHandler):
    def __init__(self, data_handlers: List[DataHandler]):
        super().__init__()
        self.data_handlers: List[DataHandler] = data_handlers

    def get_bars(self):
        for data_handler in self.data_handlers:
            if data_handler.get_current_tick() == self.get_current_tick():
                data_handler.get_bars()

    def get_symbol_list(self):
        """Get the list of available symbols."""
        raise NotImplementedError("Implement get_symbol_list().")

    def get_current_tick(self):
        """Get the frequency of the data."""
        raise NotImplementedError("Implement get_data_frequency().")
