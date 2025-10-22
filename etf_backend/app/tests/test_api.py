import io
import os

from fastapi.testclient import TestClient
from app.main import app

BASE_DIR = os.path.dirname(__file__)
ETF_FILE = os.path.join(BASE_DIR, "data/ETF1.csv")

def load_csv(path):
    with open(path, "rb") as f:
        return io.BytesIO(f.read())

def test_upload_etf_and_response():
    with TestClient(app) as client:
        file_bytes = load_csv(ETF_FILE)
        resp = client.post("/upload", files={"file": ("ETF1.csv", file_bytes, "text/csv")})
        assert resp.status_code == 200
        data = resp.json()

        for key in ["session_id", "table", "chart", "top5"]:
            assert key in data

        table = data["table"]
        chart = data["chart"]
        top5 = data["top5"]

        # Top5 test
        assert len(top5) == 5, f"Top5 count mismatch: {len(top5)}"
        expected_symbols = {"U", "F", "W", "X", "Z"}
        top5_symbols = {item["symbol"] for item in top5}
        assert top5_symbols.issubset(expected_symbols), f"Unexpected Top5 symbols: {top5_symbols}"

        # table check
        row_R = next((r for r in table if r["symbol"] == "R"), None)
        assert row_R, "Symbol R not found in table"
        assert abs(row_R["weight"] - 0.017) < 1e-3, f"Unexpected weight for R: {row_R['weight']}"
        assert abs(row_R["latest_price"] - 28.894) < 1e-3, f"Unexpected price for R: {row_R['latest_price']}"
        print(f"Verified R weight={row_R['weight']}, price={row_R['latest_price']}")

        session_id = data["session_id"]
        chart_resp = client.get(
            "/chart",
            params={"session_id": session_id}
        )
        assert chart_resp.status_code == 200
        chart_data = chart_resp.json()

        assert "date" in chart_data and "etf_price" in chart_data
        assert len(chart_data["date"]) == len(chart_data["etf_price"])

        # validate the ETF in 2017-1-7
        target_date = "2017-04-10"
        assert target_date in chart_data["date"], f"{target_date} not found in chart"
        idx = chart_data["date"].index(target_date)
        value = float(chart_data["etf_price"][idx])
        assert abs(value - 54.008013) < 1e-3, f"ETF value mismatch: expected 54.008013, got {value:.6f}"
        print(f"ETF value on {target_date} verified as {value:.6f}")

        print("ETF Upload validated successfully.")

def test_chart_date_range():
    with TestClient(app) as client:
        file_bytes = load_csv(ETF_FILE)
        upload_resp = client.post("/upload", files={"file": ("ETF1.csv", file_bytes, "text/csv")})
        session_id = upload_resp.json()["session_id"]

        resp = client.get(
            "/chart",
            params={"session_id": session_id, "start": "2017-01-05", "end": "2017-02-01"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "date" in data and "etf_price" in data
        assert "2017-04-01" not in data["date"]

def test_invalid_session():
    with TestClient(app) as client:
        resp = client.get(
            "/chart",
            params={"session_id": "non-existent-session-id", "start": "2017-01-01", "end": "2017-02-01"}
        )
        assert resp.status_code == 200
        assert "error" in resp.json()