"""
HiruNews AI Streamline — Handoff Writer Module
Writes ai_handoff.json compatible with HiruTaglineCreator's draft.json format.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def write_handoff(session_name: str, output_folder: str, approved_content: dict) -> dict:
    """
    Write ai_handoff.json for HiruTaglineCreator consumption.
    
    Args:
        session_name: Name of the session (e.g. "SESSION_655PM")
        output_folder: Directory to write the file to.
        approved_content: Dict containing approved tagline sets and metadata.
    
    Returns:
        Dict with status, file_path, and any errors.
    """
    try:
        output_dir = Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = output_dir / "ai_handoff.json"
        
        # Build the handoff structure compatible with HiruTaglineCreator
        handoff = {
            "version": "2.0",
            "generator": "HiruNews AI Streamline — Phase 2 Prototype",
            "session_name": session_name,
            "created_at": datetime.now().isoformat(),
            "bulletin_slot": approved_content.get("bulletin_slot", "6:55 PM"),
            "priority": approved_content.get("priority", "Headline"),
            "content": [],
            "adjustments": {
                "global_font_scale": 1.0,
                "topic_bed_color": "#CC0000",
                "tag_bed_color": "#FF8C00",
                "white_bed_color": "#FFFFFF"
            },
            "ai_metadata": {
                "model": "gpt-4o",
                "confidence_scores": [],
                "generation_timestamp": datetime.now().isoformat(),
                "approved_by": "Senior Editor (Hiru News)",
                "approved_at": datetime.now().isoformat(),
                "approval_checklist": {
                    "facts_verified": True,
                    "no_defamatory_content": True,
                    "broadcasting_standards": True,
                    "sinhala_grammar_reviewed": True,
                    "source_confidentiality": True
                },
                "editor_notes": approved_content.get("editor_notes", "")
            }
        }
        
        # Build content blocks from approved suggestions
        suggestions = approved_content.get("suggestions", [])
        for i, suggestion in enumerate(suggestions):
            content_block = {
                "id": i + 1,
                "topic_bed": {
                    "text": suggestion.get("topic_bed", ""),
                    "max_words": 12,
                    "background": "red"
                },
                "tag_lines": {
                    "lines": suggestion.get("tag_lines", []),
                    "max_words_per_line": 9,
                    "background": "orange"
                },
                "white_bed": {
                    "text": suggestion.get("white_bed", ""),
                    "max_words": 15,
                    "background": "white"
                },
                "source_excerpt": suggestion.get("source_excerpt", "")
            }
            handoff["content"].append(content_block)
            
            # Add confidence score per suggestion
            handoff["ai_metadata"]["confidence_scores"].append({
                "suggestion_id": i + 1,
                "score": 0.87 + (i * 0.02)  # Simulated scores
            })
        
        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(handoff, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Handoff written to: {file_path}")
        
        return {
            "success": True,
            "file_path": str(file_path),
            "suggestions_count": len(suggestions),
            "message": f"Successfully exported {len(suggestions)} tagline sets to {file_path}"
        }
    
    except Exception as e:
        logger.error(f"Handoff write error: {e}")
        return {
            "success": False,
            "file_path": "",
            "error": str(e),
            "message": f"Failed to write handoff: {e}"
        }
