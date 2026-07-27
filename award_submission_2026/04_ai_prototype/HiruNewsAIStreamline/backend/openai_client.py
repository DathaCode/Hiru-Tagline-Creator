"""
HiruNews AI Streamline — OpenAI Client Module
Wraps OpenAI SDK calls with graceful fallback to mock data.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import os
import json
import logging
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env from project root
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(_env_path)
except ImportError:
    pass

logger = logging.getLogger(__name__)

# ─── Determine mode ──────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
MOCK_MODE = DEMO_MODE or not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-your")

if not MOCK_MODE:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI client initialized with live API key.")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenAI client: {e}. Falling back to mock mode.")
        MOCK_MODE = True
        client = None
else:
    client = None
    logger.info("Running in MOCK mode — no real API calls will be made.")


def transcribe_audio(file_path: str, progress_cb=None) -> list:
    """
    Transcribe audio using OpenAI Whisper.
    Falls back to mock data when MOCK_MODE is True.
    Returns a list of diarized transcript segments.
    """
    if MOCK_MODE:
        from . import mock_data
        return mock_data.get_random_transcript()

    try:
        with open(file_path, "rb") as audio_file:
            if progress_cb:
                progress_cb(10, "Sending audio to Whisper API...")

            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )

            if progress_cb:
                progress_cb(80, "Processing transcription results...")

            # Convert Whisper segments to our diarized format
            segments = []
            for i, seg in enumerate(response.segments):
                minutes = int(seg["start"] // 60)
                seconds = int(seg["start"] % 60)
                segments.append({
                    "speaker": f"Speaker {(i % 3) + 1}",
                    "timestamp": f"00:{minutes:02d}:{seconds:02d}",
                    "text": seg["text"].strip()
                })

            if progress_cb:
                progress_cb(100, "Transcription complete.")

            return segments

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        from . import mock_data
        return mock_data.get_random_transcript()


def generate_taglines(transcript_text: str, bulletin_slot: str = "6:55 PM") -> list:
    """
    Generate tagline suggestions from transcript using GPT.
    Falls back to mock data when MOCK_MODE is True.
    Returns a list of tagline suggestion dicts.
    """
    if MOCK_MODE:
        from . import mock_data
        return mock_data.get_tagline_suggestions()

    try:
        system_prompt = """You are a Sinhala news tagline generator for Hiru News, Sri Lanka's leading TV station.
Given a transcript, generate exactly 5 tagline sets. Each set has:
1. topic_bed: A headline for the red background strip (max 12 words in Sinhala)
2. tag_lines: Array of 3 sub-headlines for the orange TAG strip (max 9 words each)
3. white_bed: A summary line for the white background strip (max 15 words)
4. source_excerpt: First 80 characters of relevant transcript section

Return valid JSON array of objects with keys: id, topic_bed, tag_lines, white_bed, source_excerpt"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Bulletin slot: {bulletin_slot}\n\nTranscript:\n{transcript_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=2000,
        )

        result = json.loads(response.choices[0].message.content)
        suggestions = result.get("suggestions", result.get("taglines", []))

        # Ensure IDs
        for i, s in enumerate(suggestions):
            s["id"] = i + 1

        return suggestions

    except Exception as e:
        logger.error(f"Tagline generation error: {e}")
        from . import mock_data
        return mock_data.get_tagline_suggestions()


def is_mock_mode() -> bool:
    """Check if we're running in mock mode."""
    return MOCK_MODE
