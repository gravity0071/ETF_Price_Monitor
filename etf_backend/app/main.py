from fastapi import FastAPI, UploadFile, File, Query
from pathlib import Path
from fastapi import UploadFile, File
import pandas as pd
from app.services.etf_calculator import etf_calculator
from app.services.price_store import PriceStore
from app.services.session_store import etf_session_store

app = FastAPI()

price_store = None
session_store = etf_session_store()

@app.on_event("startup")
def startup_event():
    global price_store
    global session_store
    data_path = Path(__file__).resolve().parent / "static" / "prices.csv"
    price_store = PriceStore(data_path, refresh_interval=60 * 60)
    price_store.start()
    session_store = etf_session_store()
    print("PriceStore and SessionStore initialized.")

# @app.get("/symbols")
# def symbols():
#     return {"symbols": price_store.get_all_symbols(), "last_update": price_store.last_update}

# @app.get("/prices/{symbol}")
# def prices(symbol: str):
#     p = price_store.get_symbol(symbol)
#     if p is None:
#         return {"error": "Data not ready or symbol not found"}
#     return {"symbol": p.symbol, "data": p.prices[:20]}
#
# @app.get("/last/{symbol}")
# def last(symbol: str):
#     p = price_store.get_latest_price(symbol)
#     if p is None:
#         return {"error": "Data not ready or symbol not found"}
#     print(p)
#     return p


@app.post("/upload")
async def upload_etf(file: UploadFile = File(...), session_id: str = Query(None)):
    etf_df = pd.read_csv(file.file)
    # print(session_id)

    calculator = etf_calculator(price_store)
    result = calculator.compute_all(etf_df)

    sid = session_store.create_or_update_session(result["merged_df"], session_id)  #put the combined dataframe into session
    return {"session_id": sid, **{k: v for k, v in result.items() if k != "merged_df"}}


@app.get("/chart")
def get_chart(session_id: str = Query(...), start: str = Query(None), end: str = Query(None)):
    df = session_store.get_session(session_id)
    if df is None:
        return {"error": "Session not found"}
    calculator = etf_calculator(price_store)
    chart_data = calculator.compute_chart_with_date(df, start, end)
    return chart_data