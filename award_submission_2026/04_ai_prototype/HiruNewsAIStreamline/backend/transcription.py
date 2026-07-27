"""
HiruNews AI Streamline — Transcription Module
Handles audio transcription via Whisper with mock fallback.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import logging
from . import openai_client

logger = logging.getLogger(__name__)


def transcribe(file_path: str, progress_cb=None) -> list:
    """
    Transcribe audio file and return diarized segments.
    
    Args:
        file_path: Path to the audio/video file.
        progress_cb: Optional callback(pct, msg) for progress updates.
    
    Returns:
        List of dicts with keys: speaker, timestamp, text
    """
    logger.info(f"Starting transcription for: {file_path}")
    
    if progress_cb:
        progress_cb(5, "Preparing audio for transcription...")
    
    segments = openai_client.transcribe_audio(file_path, progress_cb)
    
    logger.info(f"Transcription complete — {len(segments)} segments.")
    return segments
