import pandas as pd
from app.services.etf_chart import etf_chart
from app.services.etf_table import etf_table
from app.services.etf_top_holdings import etf_top_holdings
from typing import Dict
from app.services.price_store import PriceStore
from datetime import timedelta


class etf_calculator:

    def __init__(self, price_store: PriceStore):
        if not price_store.ready:
            raise RuntimeError("PriceStore not ready")
        self.price_store = price_store

    def _merge_etf_with_prices(self, etf_df: pd.DataFrame) -> pd.DataFrame:
        etf_names = etf_df["name"].unique()
        data_map = self.price_store.data_map

        missing = [name for name in etf_names if name not in data_map]
        if missing:
            raise ValueError(f"Exists a name not matching backend price record: {missing}")
        frames = []
        for name in etf_names:
            obj = data_map[name]
            tmp = pd.DataFrame(obj.prices, columns=["Date", "price"])
            tmp["symbol"] = name
            frames.append(tmp)

        df_prices = pd.concat(frames)
        df = df_prices.merge(etf_df, left_on="symbol", right_on="name", how="inner")
        # print(df.sort_values("Date").reset_index(drop=True))
        return df.sort_values("Date").reset_index(drop=True)

    def compute_all(self, etf_df: pd.DataFrame, days: int = 90):
        df = self._merge_etf_with_prices(etf_df)
        table = etf_table(df).compute()
        top5 = etf_top_holdings(df).compute()

        end_date = pd.to_datetime(df["Date"].max()).date()
        start_date = end_date - timedelta(days=days - 1)

        chart = self.compute_chart_with_date(df, start=start_date.isoformat(), end=end_date.isoformat())

        return {"merged_df": df, "table": table, "chart": chart, "top5": top5}
    def compute_chart_with_date(self, df: pd.DataFrame, start: str = None, end: str = None) -> Dict:
        return etf_chart(df).compute(start=start, end=end)