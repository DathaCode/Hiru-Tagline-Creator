"""
Exports the approved session to ai_handoff.json for HiruTaglineCreator.
"""
import json
import datetime
from pathlib import Path
from core.models import Session


def export_handoff(session: Session, output_dir: Path) -> Path:
    """
    Write ai_handoff.json to output_dir.
    Returns the path of the written file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "ai_handoff.json"

    payload = {
        "schema_version": "1.0",
        "product": "HiruNews AI Streamline",
        "module": "Phase 2 AI Processing — Prototype",
        "session_id": session.session_id,
        "bulletin_slot": session.bulletin_slot,
        "priority": session.priority,
        "source_type": session.source_type,
        "approved": session.approved,
        "approved_by": session.approved_by,
        "approved_at": session.approved_at,
        "approval_notes": session.approval_notes,
        "exported_at": datetime.datetime.now().isoformat(),
        "tagline_sets": [
            {
                "id": ts.id,
                "topic_bed": ts.topic_bed,
                "tag_lines": ts.tag_lines,
                "white_bed": ts.white_bed,
                "source_text": ts.source_text,
            }
            for ts in session.tagline_sets
        ],
        "transcript_segments": [
            {
                "speaker": seg.speaker,
                "start_time": seg.start_time,
                "end_time": seg.end_time,
                "text": seg.text,
            }
            for seg in session.transcript
        ],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return out_path
