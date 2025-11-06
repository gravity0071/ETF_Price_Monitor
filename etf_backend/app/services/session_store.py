from uuid import uuid4
import pandas as pd
from typing import Dict, Optional


class etf_session_store:
    def __init__(self):
        self.sessions: Dict[str, pd.DataFrame] = {}

    def create_or_update_session(self, merged_df: pd.DataFrame, session_id: Optional[str] = None) -> str:
        # print(session_id)
        # print(self.sessions)
        if session_id and session_id in self.sessions:
            self.sessions[session_id] = merged_df
            print("[INFO] Updated existing ETF session: {}", session_id)
            return session_id
        new_id = str(uuid4())
        while new_id in self.sessions:
            new_id = str(uuid4())
        self.sessions[new_id] = merged_df
        print("[INFO] Created new ETF session: {}", new_id)
        return new_id

    def get_session(self, session_id: str) -> Optional[pd.DataFrame]:
        return self.sessions.get(session_id)

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"[INFO] Cleared ETF session: {session_id}")

    def clear_all(self):
        session_ids = list(self.sessions.keys())
        for session_id in session_ids:
            del self.sessions[session_id]
            print(f"[INFO] Cleared ETF session: {session_id}")
        print(f"[INFO] Cleared all ETF session.")
