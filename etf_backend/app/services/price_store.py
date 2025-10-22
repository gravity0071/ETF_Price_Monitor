import pandas as pd
from pathlib import Path
from threading import Thread
import time

class Price:
    def __init__(self, symbol: str, price_list: list[tuple[str, float]]):
        self.symbol = symbol
        self.prices = price_list

class PriceStore:
    def __init__(self, csv_path: Path, refresh_interval: int = 30):
        self.csv_path = csv_path
        self.refresh_interval = refresh_interval
        self.data_map: dict[str, Price] = {}
        self.last_update = None
        self.ready = False
        self._stop = False

    def load(self):
        try:
            df = pd.read_csv(self.csv_path)
            if "DATE" not in df.columns:
                raise ValueError("Missing 'DATE' column in CSV")
            df = df.sort_values("DATE").reset_index(drop=True)

            new_map = {}
            for symbol in df.columns[1:]:
                price_list = list(zip(df["DATE"], df[symbol]))
                new_map[symbol] = Price(symbol, price_list)

            self.data_map = new_map
            self.last_update = time.strftime("%Y-%m-%d %H:%M:%S")
            self.ready = True
            print(f"[INFO] Reloaded {self.csv_path.name} ({len(new_map)} symbols) at {self.last_update}")
        except Exception as e:
            print(f"[ERROR] Failed to load {self.csv_path}: {e}")

    def _refresh_loop(self):
        while not self._stop:
            time.sleep(self.refresh_interval)
            self.load()

    def start(self):
        self.load()
        t = Thread(target=self._refresh_loop, daemon=True)
        t.start()
        print(f"[INFO] Background refresh thread started (interval={self.refresh_interval}s)")

    def stop(self):
        self._stop = True

    def get_symbol(self, symbol: str):
        if not self.ready:
            return None
        print("getting data: {}", symbol)
        return self.data_map.get(symbol)

    def get_all_symbols(self):
        if not self.ready:
            return []
        return list(self.data_map.keys())

    def get_latest_price(self, symbol: str):
        if not self.ready:
            return None
        print("getting latest price of {}", symbol)
        price_obj = self.data_map.get(symbol)
        date, price = price_obj.prices[-1]

        return {"symbol": symbol, "date": date, "price": price}