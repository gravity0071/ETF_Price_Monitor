# app/main.py
from fastapi import FastAPI, UploadFile, File
from pathlib import Path

from app.services.price_store import PriceStore

app = FastAPI()

price_store = None

@app.on_event("startup")
def startup_event():
    global price_store
    data_path = Path(__file__).resolve().parent / "static" / "prices.csv"
    price_store = PriceStore(data_path, refresh_interval=20)
    price_store.start()
    print("PriceStore initialized.")

@app.get("/symbols")
def symbols():
    return {"symbols": price_store.get_all_symbols(), "last_update": price_store.last_update}

@app.get("/prices/{symbol}")
def prices(symbol: str):
    p = price_store.get_symbol(symbol)
    if p is None:
        return {"error": "Data not ready or symbol not found"}
    return {"symbol": p.symbol, "data": p.prices[:20]}
