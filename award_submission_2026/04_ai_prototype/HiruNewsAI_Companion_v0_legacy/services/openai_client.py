"""
OpenAI client singleton — loads key from .env, falls back to mock mode.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=False)

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
DEMO_MODE: bool = (
    not OPENAI_API_KEY
    or OPENAI_API_KEY.startswith("your_key")
    or os.getenv("DEMO_MODE", "false").lower() == "true"
)

_client = None


def get_client():
    global _client
    if DEMO_MODE:
        return None
    if _client is None:
        import openai
        _client = openai.OpenAI(api_key=OPENAI_API_KEY)
    return _client
