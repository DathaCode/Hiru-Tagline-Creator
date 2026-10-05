import os
import json

class ConfigManager:
    """
    Manages loading and saving of application settings.
    """
    def __init__(self, config_file="config/settings.json", default_config="config/default_settings.json"):
        self.config_file = config_file
        self.default_config = default_config
        self.settings = self._load()

    def _load(self):
        # 1. Load defaults
        settings = {}
        if os.path.exists(self.default_config):
            try:
                with open(self.default_config, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            except Exception as e:
                print(f"Error loading default settings: {e}")

        # 2. Load user settings and update defaults
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                    self._deep_update(settings, user_settings)
            except Exception as e:
                print(f"Error loading user settings: {e}")
        else:
            # If no user settings exist, save the default ones to create the file
            self.settings = settings
            self.save()

        return settings

    def _deep_update(self, d, u):
        """Recursively update dictionary."""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v

    def save(self):
        """Save current settings to config_file."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, section, key=None, default=None):
        """Get a specific setting."""
        if section not in self.settings:
            return default
        
        if key is None:
            return self.settings.get(section, default)
            
        return self.settings.get(section, {}).get(key, default)
