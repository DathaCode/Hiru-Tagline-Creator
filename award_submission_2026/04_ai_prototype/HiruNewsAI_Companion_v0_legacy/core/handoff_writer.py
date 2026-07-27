"""
Writes ai_handoff.json compatible with HiruTaglineCreator draft.json format.
"""
import json
import datetime
from pathlib import Path
from core.session_model import Session


def write_handoff(session: Session, base_path: str) -> Path:
    """
    Writes {base_path}/{session_name}_{date}/ai_handoff.json.
    Returns the path of the written file.
    """
    folder_name = f"{session.session_name or 'SESSION'}_{session.date_str}"
    out_dir = Path(base_path) / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "ai_handoff.json"

    # Build tag_lines_raw — newline-separated
    approved = [s for s in session.suggestions if s.selected]
    topic = approved[0].topic_bed if approved else ""
    tag_lines = "\n".join(
        ln for s in approved for ln in s.tag_lines
    )
    white = approved[0].white_bed if approved else ""

    payload = {
        "session_name": session.session_name,
        "template_type": "MAIN_TAG",
        "content": {
            "topic_bed_raw": topic,
            "tag_lines_raw": tag_lines,
            "white_bed_raw": white,
        },
        "adjustments": {"h_scale": 100, "letter_spacing": 0},
        "ai_metadata": {
            "generated_by": "HiruNews AI Streamline v0.1 (Prototype)",
            "source_file": session.source_path,
            "transcription_model": "whisper-1",
            "generation_model": "gpt-4o-mini",
            "generated_at": session.created_at,
            "approved_by": f"{session.editor_name} — {session.editor_role}".strip(" —"),
            "approved_at": session.approved_at or datetime.datetime.now().isoformat(),
            "approval_checklist": session.approval_checklist,
            "editor_notes": session.editor_notes,
        },
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return out_file
