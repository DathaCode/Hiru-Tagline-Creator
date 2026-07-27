"""
Tagline generation service — GPT-4o-mini with structured JSON output.
Generates 5-10 Sinhala broadcast tagline suggestions.
"""
import json
import time
from typing import List, Callable
from core.session_model import TranscriptLine, TaglineSuggestion
from services.openai_client import get_client, DEMO_MODE

_MOCK_SUGGESTIONS = [
    {
        "topic_bed":    "දිත්වා සුළිසුළං අනතුරු ඇඟවීම",
        "tag_lines":    ["රජය ඉවත් කිරීමේ නියෝග නිකුත් කරයි", "දිස්ත්‍රික්ක 5ක ජනතාව ආරක්ෂිත ස්ථාන වෙත"],
        "white_bed":    "හිරු පුවත් — රාත්‍රී 6.55",
        "source_excerpt": "රජය විසින් දිස්ත්‍රික්ක 5ක ජනතාවට ඉවත් කිරීමේ නියෝග නිකුත් කර ඇති...",
    },
    {
        "topic_bed":    "හමුදා සහ පොලිස් ක්‍රියාත්මකයි",
        "tag_lines":    ["නාවික හමුදා මෙහෙයුම් ආරම්භ කෙරේ", "ආපදා මධ්‍යස්ථාන ජනතාවට විවෘතයි"],
        "white_bed":    "හිරු පුවත් — රාත්‍රී 6.55",
        "source_excerpt": "නාවික හමුදාව සහ ගුවන් හමුදාව මෙහෙයුම් ආරම්භ කර...",
    },
    {
        "topic_bed":    "ගංවතුර අනතුරු ඇඟවීම ක්‍රියාත්මකයි",
        "tag_lines":    ["ගාල්ල, මාතර, හම්බන්තොට දිස්ත්‍රික්ක", "රත්නපුර හා කළුතරද ඇතුළත් වෙයි"],
        "white_bed":    "හිරු පුවත් — රාත්‍රී 6.55",
        "source_excerpt": "ගාල්ල, මාතර, හම්බන්තොට, රත්නපුර...",
    },
    {
        "topic_bed":    "ජනාධිපති හදිසි රැස්වීමක් කැඳවයි",
        "tag_lines":    ["ත්‍රිවිධ හමුදා ක්ෂණික සහය ලබා දෙයි", "ආපදා ඇමති ජනාධිපති සමඟ සාකච්ඡාවේ"],
        "white_bed":    "හිරු පුවත් — රාත්‍රී 6.55",
        "source_excerpt": "ජනාධිපති කාර්යාලය සහ ආපදා කළමනාකරණ ඇමතිවරයා...",
    },
    {
        "topic_bed":    "හිරු නිවේදනය — ආරක්ෂාව",
        "tag_lines":    ["ජනතාව ආරක්ෂිත ස්ථාන කරා ගෙන යෑමට දිරිගන්වමු", "රජයේ උපදෙස් පිළිපදිනු"],
        "white_bed":    "හිරු පුවත් — රාත්‍රී 6.55",
        "source_excerpt": "ආපදා කළමනාකරණ මධ්‍යස්ථානය...",
    },
]


def generate(
    transcript_lines: List[TranscriptLine],
    bulletin_slot: str = "6:55 PM",
    progress_cb: Callable[[int, str], None] = None,
    word_limits: dict = None,
) -> List[TaglineSuggestion]:
    """
    Returns a list of TaglineSuggestion objects.
    """
    if word_limits is None:
        word_limits = {"topic_bed": 12, "tag_line": 9, "white_bed": 15}

    if DEMO_MODE:
        return _mock_generate(bulletin_slot, progress_cb, word_limits)
    return _live_generate(transcript_lines, bulletin_slot, progress_cb, word_limits)


def _mock_generate(bulletin_slot, progress_cb, word_limits) -> List[TaglineSuggestion]:
    steps = [
        (20, "Analysing transcript structure..."),
        (45, "Identifying key news points..."),
        (70, "Generating Sinhala taglines..."),
        (90, "Validating word counts..."),
    ]
    for pct, msg in steps:
        time.sleep(0.4)
        if progress_cb:
            progress_cb(pct, msg)

    results = []
    for i, d in enumerate(_MOCK_SUGGESTIONS, start=1):
        white = d["white_bed"].replace("6.55", bulletin_slot.replace(" PM", "").replace(" AM", ""))
        sug = TaglineSuggestion(
            id=i,
            topic_bed=d["topic_bed"],
            tag_lines=list(d["tag_lines"]),
            white_bed=white,
            source_excerpt=d["source_excerpt"],
        )
        sug.validate(word_limits)
        results.append(sug)

    if progress_cb:
        progress_cb(100, f"{len(results)} suggestions generated.")
    return results


def _live_generate(transcript_lines, bulletin_slot, progress_cb, word_limits) -> List[TaglineSuggestion]:
    client = get_client()
    if progress_cb:
        progress_cb(15, "Sending transcript to GPT-4o-mini...")

    full_text = "\n".join(
        f"{ln.speaker} {ln.timestamp_str}: {ln.text}"
        for ln in transcript_lines
    )
    prompt = (
        "You are an expert Sinhala broadcast journalist at Hiru News, Sri Lanka.\n\n"
        "Analyse the transcript below and produce 5 tagline sets in Sinhala Unicode.\n\n"
        f"TRANSCRIPT:\n{full_text}\n\n"
        "Return valid JSON matching this exact schema:\n"
        '{"suggestions": [{"topic_bed": "<Sinhala, max 8 words>", '
        '"tag_lines": ["<Sinhala, max 9 words>", "<Sinhala, max 9 words>"], '
        f'"white_bed": "හිරු පුවත් — {bulletin_slot}", '
        '"source_excerpt": "<key sentence>"}]}\n\n'
        "Rules: Sinhala Unicode only for topic/tag/white, factual, broadcast-style, JSON only."
    )

    if progress_cb:
        progress_cb(50, "Waiting for GPT-4o-mini response...")

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    if progress_cb:
        progress_cb(85, "Validating suggestions...")

    raw = json.loads(resp.choices[0].message.content)
    results = []
    for i, d in enumerate(raw.get("suggestions", []), start=1):
        sug = TaglineSuggestion(
            id=i,
            topic_bed=d.get("topic_bed", ""),
            tag_lines=d.get("tag_lines", []),
            white_bed=d.get("white_bed", f"හිරු පුවත් — {bulletin_slot}"),
            source_excerpt=d.get("source_excerpt", ""),
        )
        sug.validate(word_limits)
        results.append(sug)

    if progress_cb:
        progress_cb(100, f"{len(results)} suggestions generated.")
    return results
