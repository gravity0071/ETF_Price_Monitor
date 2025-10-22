import pandas as pd
from app.services.etf_chart import etf_chart
from app.services.etf_table import etf_table
from app.services.etf_top_holdings import etf_top_holdings
from typing import Dict
from app.services.price_store import PriceStore, Price

class etf_calculator:

    def __init__(self, price_store: PriceStore):
        if not price_store.ready:
            raise RuntimeError("PriceStore not ready")
        self.price_store = price_store

    def _merge_etf_with_prices(self, etf_df: pd.DataFrame) -> pd.DataFrame:
        frames = []
        for symbol, obj in self.price_store.data_map.items():
            if symbol not in etf_df["name"].values:
                continue
            tmp = pd.DataFrame(obj.prices, columns=["Date", "price"])
            tmp["symbol"] = symbol
            frames.append(tmp)

        if not frames:
            raise ValueError("No matching symbols between ETF and prices.csv")
        df_prices = pd.concat(frames)
        df = df_prices.merge(etf_df, left_on="symbol", right_on="name", how="inner")
        # print(df.sort_values("Date").reset_index(drop=True))
        return df.sort_values("Date").reset_index(drop=True)

    def compute_all(self, etf_df: pd.DataFrame):
        df = self._merge_etf_with_prices(etf_df)
        table = etf_table(df).compute()
        chart = etf_chart(df).compute()
        top5 = etf_top_holdings(df).compute()
        return {"merged_df": df, "table": table, "chart": chart, "top5": top5}

    def compute_chart_with_date(self, df: pd.DataFrame, start: str = None, end: str = None) -> Dict:
        return etf_chart(df).compute(start=start, end=end)