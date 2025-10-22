class etf_top_holdings:
    def __init__(self, df):
        self.df = df

    def compute(self):
        latest_date = self.df["Date"].max()
        df_latest = self.df[self.df["Date"] == latest_date].copy()
        df_latest["holding_value"] = df_latest["weight"] * df_latest["price"]
        return df_latest.nlargest(5, "holding_value")[["symbol", "holding_value"]].to_dict(orient="records")
