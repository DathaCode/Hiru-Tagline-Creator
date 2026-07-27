"""
Approval state helpers and checklist labels.
"""
from typing import Dict

CHECKLIST_LABELS: Dict[str, str] = {
    "facts_verified":         "Facts verified against source material",
    "no_defamatory_content":  "No defamatory or legally sensitive content",
    "broadcasting_standards": "Complies with broadcasting standards",
    "sinhala_grammar_reviewed": "Sinhala grammar and script reviewed",
    "source_confidentiality": "Source confidentiality preserved",
}

STATUS_COLOURS: Dict[str, str] = {
    "Approved":           "#1a6b1a",
    "Rejected":           "#a70003",
    "Changes Requested":  "#cc6600",
    "Pending":            "#888888",
}


def status_colour(status: str) -> str:
    return STATUS_COLOURS.get(status, "#888888")
