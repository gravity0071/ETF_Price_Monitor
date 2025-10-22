
class etf_table:
    def __init__(self, df):
        self.df = df

    def compute(self):
        latest_date = self.df["Date"].max()
        df_latest = self.df[self.df["Date"] == latest_date].copy()
        df_latest["latest_price"] = df_latest["price"]
        return df_latest[["symbol", "weight", "latest_price"]].to_dict(orient="records")