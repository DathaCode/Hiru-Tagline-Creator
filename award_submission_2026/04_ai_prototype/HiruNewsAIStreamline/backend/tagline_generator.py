"""
HiruNews AI Streamline — Tagline Generator Module
GPT-powered structured JSON generation for broadcast taglines.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import logging
from . import openai_client

logger = logging.getLogger(__name__)


def generate(transcript_segments: list, bulletin_slot: str = "6:55 PM", progress_cb=None) -> list:
    """
    Generate tagline suggestions from transcript segments.
    
    Args:
        transcript_segments: List of diarized transcript dicts.
        bulletin_slot: The bulletin time slot.
        progress_cb: Optional callback(pct, msg) for progress updates.
    
    Returns:
        List of tagline suggestion dicts.
    """
    logger.info("Starting tagline generation...")
    
    if progress_cb:
        progress_cb(10, "Preparing transcript for AI analysis...")
    
    # Combine segments into a single text block
    full_text = "\n".join(
        f"[{seg.get('speaker', 'Unknown')} @ {seg.get('timestamp', '')}] {seg.get('text', '')}"
        for seg in transcript_segments
    )
    
    if progress_cb:
        progress_cb(30, "Sending to GPT for tagline generation...")
    
    suggestions = openai_client.generate_taglines(full_text, bulletin_slot)
    
    if progress_cb:
        progress_cb(100, "Tagline generation complete.")
    
    logger.info(f"Generated {len(suggestions)} tagline suggestions.")
    return suggestions
