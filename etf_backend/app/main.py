from fastapi import FastAPI, Depends, Query
from pathlib import Path
from fastapi import UploadFile, File
import pandas as pd
from app.services.etf_calculator import etf_calculator
from app.services.price_store import PriceStore
from app.services.session_store import etf_session_store
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
price_store = None
session_store = None

def get_current_user(session_id: str = Query(...)):
    if session_id is None or session_id not in session_store.sessions:
        raise ValueError("not logged in")
    print(session_id)
    return session_id

@app.on_event("startup")
def startup_event():
    global price_store
    global session_store
    data_path = Path(__file__).resolve().parent / "static" / "prices.csv"
    session_store = etf_session_store()
    price_store = PriceStore(data_path, session_store, refresh_interval=60*60*24)
    price_store.start()
    print("PriceStore and SessionStore initialized.")

@app.on_event("shutdown")
def shutdown_event():
    price_store.stop()

@app.post("/upload")
def upload_etf(
    file: UploadFile = File(...),
    session_id: str = Query(None),
    days: int = Query(90),
):
    try:
        etf_df = pd.read_csv(file.file)

        calculator = etf_calculator(price_store)
        result = calculator.compute_all(etf_df, days=days)

        sid = session_store.create_or_update_session(result["merged_df"], session_id)
        # print({"session_id": sid, **{k: v for k, v in result.items() if k != "merged_df"}})
        return {"session_id": sid, **{k: v for k, v in result.items() if k != "merged_df"}}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Server error: {e}"})


@app.get("/chart")
def get_chart(session_id: str = Query(...), start: str = Query(None), end: str = Query(None), user_id = Depends(get_current_user)):
    print(f"from getChart func: user_id_seesion_id {user_id}")
    df = session_store.get_session(session_id)
    if df is None:
        return {"error": "Session not found"}
    calculator = etf_calculator(price_store)
    chart_data = calculator.compute_chart_with_date(df, start, end)
    # print(chart_data)
    return chart_data

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)