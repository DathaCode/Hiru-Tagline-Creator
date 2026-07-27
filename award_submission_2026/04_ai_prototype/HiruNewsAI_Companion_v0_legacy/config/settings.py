"""
Settings loader — reads .env and provides typed configuration.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(_ENV_PATH, override=False)


class Settings:
    def __init__(self):
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.demo_mode: bool = os.getenv("DEMO_MODE", "false").lower() == "true"

        _raw_path = os.getenv("HANDOFF_OUTPUT_PATH", "").strip()
        if _raw_path:
            self.handoff_output_path = Path(_raw_path)
        else:
            self.handoff_output_path = Path(__file__).parent.parent / "sessions"

        # Auto-enable demo mode if no API key is present
        if not self.openai_api_key or self.openai_api_key.startswith("sk-your"):
            self.demo_mode = True

    @property
    def has_api_key(self) -> bool:
        return bool(self.openai_api_key) and not self.openai_api_key.startswith("sk-your")
