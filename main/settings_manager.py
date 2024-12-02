import json
import os
from typing import Dict, Any

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "selected_monitor": 0,
            "idle_timeout": 5,
            "timer_enabled": True
        }
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create with defaults if doesn't exist"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading settings file. Using defaults.")
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()

    def save_settings(self) -> None:
        """Save current settings to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key: str, default=None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and save to file"""
        self.settings[key] = value
        self.save_settings()