class etf_chart:
    def __init__(self, df):
        self.df = df

    def compute(self, start: str = None, end: str = None):
        df = self.df.copy()
        if start:
            df = df[df["Date"] >= start]
        if end:
            df = df[df["Date"] <= end]
        df["weighted_price"] = df["price"] * df["weight"]
        etf_series = df.groupby("Date")["weighted_price"].sum().reset_index()
        return {
            "date": etf_series["Date"].tolist(),
            "etf_price": etf_series["weighted_price"].tolist(),
        }