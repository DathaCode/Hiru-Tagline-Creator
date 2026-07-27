"""
HiruNews AI Streamline — Mock Data Module
Provides realistic Sinhala sample data for demo/prototype mode.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import random
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# SAMPLE TRANSCRIPTS  (3 scenarios)
# ─────────────────────────────────────────────────────────────

TRANSCRIPTS = {
    "weather_disaster": [
        {
            "speaker": "Anchor",
            "timestamp": "00:00:03",
            "text": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි. කාලගුණ විද්‍යා දෙපාර්තමේන්තුව එම තොරතුර තහවුරු කළා."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:00:28",
            "text": "ඇදහැලෙන අධික වර්ෂාව නිසා අම්පාර හිමිදුරාව මාර්ගය ජලයෙන් යටවෙයි. අම්පාරේ කුඹුරු රැසක් ජලයෙන් යටව පවතිනවා."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:00:52",
            "text": "අධික වැසි සමඟ ප්‍රධාන ජලාශ්‍ර 73න් 25ක් වාන් දමමින් පවතිනවා. බෝවතැන්න ජලාශයේ වාන් දොරටු හයක් විවෘත කෙරුණා."
        },
        {
            "speaker": "Anchor",
            "timestamp": "00:01:18",
            "text": "දැඩි වර්ෂාවේ බලපෑමත් සමග ගංගා කිහිපයක ජල මට්ටම් තවදුරටත් ඉහළට. මහවැලි ගඟ ආශ්‍රිත පහත් බිම් ප්‍රදේශවලට ඉදිරි පැය 48 තුළ ගංවතුර තත්ත්වයක් ඇතිවීමේ අවධානමක්."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:01:48",
            "text": "කඩුගන්නාව ප්‍රදේශයේ තවදුරටත් නායයෑමේ අවදානම පවතී. හපුතලේ මාර්ග කිහිපයකට පස් කඳු කඩා වැටී ගමනාගමනයට බාධා. දුම්රිය ධාවනය නානුඔයට සීමා කෙරේ."
        },
        {
            "speaker": "Anchor",
            "timestamp": "00:02:15",
            "text": "දිට්වා සුළිකුණාටුවේදී ත්‍රිවිධ හමුදාව කටයුතු කළ විදිය අපි දැන් බලමු. මාතර දිස්ත්‍රික්කයේ ගංවතුරින් පවුල් 850කට අධික සංඛ්‍යාවක් අවතැන් වී ඇත. ආපදා සහන මධ්‍යස්ථාන 12ක් විවෘත කර ඇත."
        }
    ],

    "flood_update": [
        {
            "speaker": "Anchor",
            "timestamp": "00:00:02",
            "text": "අයහපත් වූ කාලගුණය හේතුවෙන් දිවයිනේ බොහෝ ප්‍රදේශවලට ඇදහැලෙන වැසි වාර්තා වෙනවා."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:00:22",
            "text": "අඹන පාලම අසලින් මාර්ගය ජලයෙන් යටවූ අයුරු. මධ්‍යම කඳුකරයේ දිය ඇලි සක්‍රීය වී ඇති ආකාරය."
        },
        {
            "speaker": "Official",
            "timestamp": "00:00:45",
            "text": "සෝමාවතී ප්‍රදේශයද ජලයෙන් යටවීමේ අවදානමක් පවතී. ජනතාව අවදානයෙන් සිටිය යුතුයි."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:01:10",
            "text": "මහවැලි ගඟ ආශ්‍රිත පහත් බිම් ප්‍රදේශවලට ඉදිරි පැය 48 තුළ ගංවතුර තත්ත්වයක් ඇතිවීමේ අවධානමක්."
        },
        {
            "speaker": "Anchor",
            "timestamp": "00:01:38",
            "text": "කඩුගන්නාව ප්‍රදේශයේ තවදුරටත් නායයෑමේ අවදානම පවතී. හපුතලේ මාර්ග කිහිපයකට පස් කඳු කඩා වැටී ගමනාගමනයට බාධා."
        },
        {
            "speaker": "Official",
            "timestamp": "00:02:05",
            "text": "අධික වැසි සමඟ ප්‍රධාන ජලාශ්‍ර 73න් 25ක් වාන් දමමින් පවතිනවා. බෝවතැන්න ජලාශයේ වාන් දොරටු හයක් විවෘත කෙරුණා."
        }
    ],

    "rescue_operations": [
        {
            "speaker": "Anchor",
            "timestamp": "00:00:04",
            "text": "දිට්වා සුළිකුණාටුවේදී ත්‍රිවිධ හමුදාව කටයුතු කළ විදිය අපි දැන් බලමු."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:00:25",
            "text": "මාතර දිස්ත්‍රික්කයේ ගංවතුරින් පවුල් 850කට අධික සංඛ්‍යාවක් අවතැන් වී ඇත. ආපදා සහන මධ්‍යස්ථාන 12ක් විවෘත කර ඇත."
        },
        {
            "speaker": "Official",
            "timestamp": "00:00:50",
            "text": "ඇදහැලෙන අධික වර්ෂාව නිසා අම්පාර හිමිදුරාව මාර්ගය ජලයෙන් යටවෙයි. අම්පාරේ කුඹුරු රැසක් ජලයෙන් යටව පවතිනවා."
        },
        {
            "speaker": "Reporter",
            "timestamp": "00:01:15",
            "text": "දුම්රිය ධාවනය නානුඔයට සීමා කෙරේ. මධ්‍යම කඳුකරයේ දිය ඇලි සක්‍රීය වී ඇති ආකාරය."
        },
        {
            "speaker": "Anchor",
            "timestamp": "00:01:42",
            "text": "දැඩි වර්ෂාවේ බලපෑමත් සමග ගංගා කිහිපයක ජල මට්ටම් තවදුරටත් ඉහළට."
        },
        {
            "speaker": "Official",
            "timestamp": "00:02:08",
            "text": "සෝමාවතී ප්‍රදේශයද ජලයෙන් යටවීමේ අවදානමක් පවතී. කඩුගන්නාව ප්‍රදේශයේ තවදුරටත් නායයෑමේ අවදානම පවතී."
        }
    ]
}


# ─────────────────────────────────────────────────────────────
# SAMPLE TAGLINE SUGGESTIONS  (5 sets)
# ─────────────────────────────────────────────────────────────

TAGLINE_SUGGESTIONS = [
    {
        "id": 1,
        "topic_bed": "අයහපත් වූ කාලගුණය",
        "tag_lines": [
            "ඇදහැලෙන අධික වර්ෂාව නිසා අම්පාර හිමිදුරාව මාර්ගය ජලයෙන් යටවෙයි",
            "අම්පාරේ කුඹුරු රැසක් ජලයෙන් යටව පවතිනවා",
            "අධික වැසි සමඟ ප්‍රධාන ජලාශ්‍ර 73න් 25ක් වාන් දමමින් පවතිනවා",
        ],
        "white_bed": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි-කාලගුණ විද්‍යා දෙපාර්තමේන්තුව",
        "source_excerpt": "ඇදහැලෙන අධික වර්ෂාව නිසා අම්පාර හිමිදුරාව මාර්ගය ජලයෙන් යටවෙයි..."
    },
    {
        "id": 2,
        "topic_bed": "අයහපත් වූ කාලගුණය",
        "tag_lines": [
            "බෝවතැන්න ජලාශයේ වාන් දොරටු හයක් විවෘත කෙරුණා",
            "අඹන පාලම අසලින් මාර්ගය ජලයෙන්  යටවූ අයුරු",
            "මධ්‍යම කඳුකරයේ දිය ඇලි සක්‍රීය වී ඇති ආකාරය",
        ],
        "white_bed": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි-කාලගුණ විද්‍යා දෙපාර්තමේන්තුව",
        "source_excerpt": "බෝවතැන්න ජලාශයේ වාන් දොරටු හයක් විවෘත කෙරුණා..."
    },
    {
        "id": 3,
        "topic_bed": "අයහපත් වූ කාලගුණය",
        "tag_lines": [
            "දැඩි වර්ෂාවේ බලපෑමත් සමග ගංගා කිහිපයක ජල මට්ටම් තවදුරටත් ඉහළට",
            "මහවැලි ගඟ ආශ්‍රිත පහත් බිම් ප්‍රදේශවලට ඉදිරි පැය 48 තුළ ගංවතුර තත්ත්වයක් ඇතිවීමේ අවධානමක්",
            "සෝමාවතී ප්‍රදේශයද ජලයෙන් යටවීමේ අවදානමක් පවතී",
        ],
        "white_bed": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි-කාලගුණ විද්‍යා දෙපාර්තමේන්තුව",
        "source_excerpt": "දැඩි වර්ෂාවේ බලපෑමත් සමග ගංගා කිහිපයක ජල මට්ටම් තවදුරටත් ඉහළට..."
    },
    {
        "id": 4,
        "topic_bed": "අයහපත් වූ කාලගුණය",
        "tag_lines": [
            "කඩුගන්නාව ප්‍රදේශයේ තවදුරටත් නායයෑමේ අවදානම පවතීී",
            "හපුතලේ මාර්ග කිහිපයකට පස් කඳු කඩා වැටී ගමනාගමනයට බාධා",
            "දුම්රිය ධාවනය නානුඔයට සීමා කෙරේ",
        ],
        "white_bed": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි-කාලගුණ විද්‍යා දෙපාර්තමේන්තුව",
        "source_excerpt": "කඩුගන්නාව ප්‍රදේශයේ තවදුරටත් නායයෑමේ අවදානම පවතී..."
    },
    {
        "id": 5,
        "topic_bed": "අයහපත් වූ කාලගුණය",
        "tag_lines": [
            "දිට්වා සුළිකුණාටුවේදී ත්‍රිවිධ හමුදාව කටයුතු කළ විදිය අපි දැන් බලමු",
            "මාතර දිස්ත්‍රික්කයේ ගංවතුරින් පවුල් 850කට අධික සංඛ්‍යාවක් අවතැන් වී ඇත",
            "ආපදා සහන මධ්‍යස්ථාන 12ක් විවෘත කර ඇත",
        ],
        "white_bed": "නිරිතදිග බෙංගාල බොක්ක ප්‍රදේශයට පවතින අඩුපීඩන කලාපය පීඩන අවපාතයක් දක්වා තීව්‍ර විය හැකියි-කාලගුණ විද්‍යා දෙපාර්තමේන්තුව",
        "source_excerpt": "දිට්වා සුළිකුණාටුවේදී ත්‍රිවිධ හමුදාව කටයුතු කළ විදිය..."
    }
]


# ─────────────────────────────────────────────────────────────
# DASHBOARD SESSION DATA  (exactly 8 rows as specified)
# ─────────────────────────────────────────────────────────────

DASHBOARD_SESSIONS = [
    {"id": 1, "session": "WEATHER_ALERT",    "bulletin_slot": "6:55 PM",  "taglines": 14, "status": "Approved",          "timestamp": "2025-12-10 17:22"},
    {"id": 2, "session": "FLOOD_UPDATE",     "bulletin_slot": "9:55 PM",  "taglines": 12, "status": "Approved",          "timestamp": "2025-12-10 21:10"},
    {"id": 3, "session": "AMPARA_FLOOD",     "bulletin_slot": "11:55 AM", "taglines": 15, "status": "Pending Review",    "timestamp": "2025-12-10 10:44"},
    {"id": 4, "session": "DITWA_CYCLONE",    "bulletin_slot": "6:55 PM",  "taglines": 24, "status": "Approved",          "timestamp": "2025-12-09 17:31"},
    {"id": 5, "session": "RESERVOIR_SPILL",  "bulletin_slot": "9:55 PM",  "taglines": 19, "status": "Approved",          "timestamp": "2025-12-09 20:58"},
    {"id": 6, "session": "LANDSLIDE_WARN",   "bulletin_slot": "11:55 AM", "taglines": 10, "status": "Rejected",          "timestamp": "2025-12-08 11:12"},
    {"id": 7, "session": "MATARA_RESCUE",    "bulletin_slot": "6:55 PM",  "taglines": 17, "status": "Approved",          "timestamp": "2025-12-08 16:45"},
    {"id": 8, "session": "RAIL_DISRUPTION",  "bulletin_slot": "9:55 PM",  "taglines": 8,  "status": "Changes Requested", "timestamp": "2025-12-07 21:03"},
]


# ─────────────────────────────────────────────────────────────
# DASHBOARD STATS
# ─────────────────────────────────────────────────────────────

DASHBOARD_STATS = {
    "taglines_today": 42,
    "taglines_approved": 38,
    "pending_review": 4,
    "avg_time_per_tagline": 142,  # seconds
    "trends": {
        "taglines_today_pct": 12,
        "approved_pct": 8,
        "pending_pct": -3,
        "avg_time_pct": -5,
    }
}


# ─────────────────────────────────────────────────────────────
# CHART DATA  (last 7 days)
# ─────────────────────────────────────────────────────────────

CHART_DATA_7_DAYS = [
    {"day": "Dec 4",  "taglines": 28},
    {"day": "Dec 5",  "taglines": 35},
    {"day": "Dec 6",  "taglines": 22},
    {"day": "Dec 7",  "taglines": 40},
    {"day": "Dec 8",  "taglines": 31},
    {"day": "Dec 9",  "taglines": 45},
    {"day": "Dec 10", "taglines": 42},
]


# ─────────────────────────────────────────────────────────────
# SYSTEM HEALTH
# ─────────────────────────────────────────────────────────────

SYSTEM_HEALTH = [
    {"name": "OpenAI API",                "status": "Connected", "color": "green"},
    {"name": "Local Storage",             "status": "OK",        "color": "green"},
    {"name": "HiruTaglineCreator Bridge", "status": "Ready",     "color": "green"},
]


# ─────────────────────────────────────────────────────────────
# AI PERFORMANCE METRICS
# ─────────────────────────────────────────────────────────────

AI_PERFORMANCE = {
    "transcription_avg_time": "18.4s",
    "generation_avg_time": "12.1s",
    "success_rate": "96.8%",
    "transcription_pct": 92,
    "generation_pct": 88,
    "success_pct": 97,
}


def get_random_transcript():
    """Return a random transcript scenario."""
    key = random.choice(list(TRANSCRIPTS.keys()))
    return TRANSCRIPTS[key]


def get_tagline_suggestions():
    """Return the 5 sample tagline suggestion sets."""
    return TAGLINE_SUGGESTIONS


def get_dashboard_data():
    """Return complete dashboard data bundle."""
    return {
        "stats": DASHBOARD_STATS,
        "chart": CHART_DATA_7_DAYS,
        "sessions": DASHBOARD_SESSIONS,
        "health": SYSTEM_HEALTH,
        "performance": AI_PERFORMANCE,
    }
