import os
import json
from datetime import datetime

class SessionManager:
    """
    Handles session creation, auto-saving, and file organization.
    """
    def __init__(self, settings):
        self.settings = settings
        self.base_dir = self.settings.get("session", "default_save_location", "C:/HiruTaglines/")
        self.current_session_path = None
        self.unsaved_changes = False

    def create_session(self, session_name):
        """Create new session folder."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{session_name}_{date_str}"
        self.current_session_path = os.path.join(self.base_dir, folder_name)
        
        os.makedirs(self.current_session_path, exist_ok=True)
        self.unsaved_changes = True
        
        # Create initial draft
        self.save_draft({
            "session_name": session_name,
            "template_type": "MAIN_TAG",
            "created": datetime.now().isoformat(),
            "content": {},
            "adjustments": {}
        })
        
        return self.current_session_path

    def get_session_path(self):
        """Return current session folder path."""
        return self.current_session_path

    def save_draft(self, draft_data):
        """Auto-save current work to session folder."""
        if not self.current_session_path:
            return False
            
        draft_data["last_modified"] = datetime.now().isoformat()
        draft_path = os.path.join(self.current_session_path, "draft.json")
        
        try:
            with open(draft_path, "w", encoding="utf-8") as f:
                json.dump(draft_data, f, indent=4, ensure_ascii=False)
            self.unsaved_changes = False
            return True
        except Exception as e:
            print(f"Failed to save draft: {e}")
            return False

    def load_draft(self):
        """Load draft from session folder."""
        if not self.current_session_path:
            return None
            
        draft_path = os.path.join(self.current_session_path, "draft.json")
        if os.path.exists(draft_path):
            try:
                with open(draft_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load draft: {e}")
        return None

    def list_sessions(self):
        """Return list of existing sessions."""
        if not os.path.exists(self.base_dir):
            return []
            
        sessions = []
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "draft.json")):
                sessions.append(item)
        return sorted(sessions, reverse=True)

    def generate_filename(self, bed_type, text, date=None):
        """Create filename based on convention."""
        if date is None:
            date_format = self.settings.get("session", "date_format", "%Y-%m-%d")
            # standardizing the python strftime format if "YYYY-MM-DD" is given
            if date_format == "YYYY-MM-DD":
                date_format = "%Y-%m-%d"
            date = datetime.now().strftime(date_format)
            
        if bed_type == "TOPIC_BED":
            return f"TopicBed_{date}.png"
            
        # Clean text for other beds to get first 3 words
        safe_text = "".join([c for c in text if c.isalnum() or c.isspace()]).strip()
        words = safe_text.split()
        prefix = "_".join(words[:3]) if words else "Untitled"
        
        if bed_type == "TAG_BED":
            return f"{prefix}_TAG_{date}.png"
        elif bed_type == "WHITE_BED":
            return f"{prefix}_WhiteBed_{date}.png"
            
        return f"{prefix}_{bed_type}_{date}.png"

    def check_unsaved_changes(self):
        """Prompt user to save before closing."""
        return self.unsaved_changes
        
    def has_draft(self):
        """Check if any drafts exist across sessions."""
        return len(self.list_sessions()) > 0

    def load_draft_into_ui(self, app):
        """Will be implemented to load draft content into UI elements."""
        print("Loading draft into UI (not fully implemented yet)")
