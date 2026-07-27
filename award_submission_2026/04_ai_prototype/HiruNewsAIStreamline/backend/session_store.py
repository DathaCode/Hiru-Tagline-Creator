"""
HiruNews AI Streamline — Session Store Module
Local JSON persistence for sessions and app state.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Default data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SESSIONS_DIR = DATA_DIR / "sessions"


def ensure_dirs():
    """Create data directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def save_session(session_name: str, session_data: dict) -> dict:
    """
    Save a session to disk as JSON.
    
    Args:
        session_name: Name of the session.
        session_data: Full session data dictionary.
    
    Returns:
        Dict with status and file path.
    """
    ensure_dirs()
    
    try:
        file_path = SESSIONS_DIR / f"{session_name}.json"
        session_data["saved_at"] = datetime.now().isoformat()
        session_data["session_name"] = session_name
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Session saved: {file_path}")
        return {"success": True, "file_path": str(file_path)}
    
    except Exception as e:
        logger.error(f"Session save error: {e}")
        return {"success": False, "error": str(e)}


def load_session(session_name: str) -> dict:
    """
    Load a session from disk.
    
    Args:
        session_name: Name of the session to load.
    
    Returns:
        Session data dictionary or empty dict if not found.
    """
    try:
        file_path = SESSIONS_DIR / f"{session_name}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Session load error: {e}")
        return {}


def list_sessions() -> list:
    """
    List all saved sessions.
    
    Returns:
        List of session summary dicts.
    """
    ensure_dirs()
    
    sessions = []
    for file_path in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sessions.append({
                    "session_name": data.get("session_name", file_path.stem),
                    "saved_at": data.get("saved_at", ""),
                    "bulletin_slot": data.get("bulletin_slot", ""),
                    "status": data.get("status", "Draft"),
                })
        except Exception:
            continue
    
    return sessions


def load_dashboard_json() -> dict:
    """Load dashboard.json or return empty dict."""
    try:
        dashboard_path = DATA_DIR / "dashboard.json"
        if dashboard_path.exists():
            with open(dashboard_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Dashboard load error: {e}")
        return {}
