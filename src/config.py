"""Configuration file loader for per-exercise and application settings"""

import json
import logging
import os


class Config:
    """Loads optional config.json and provides setting accessors"""

    def __init__(self, file_path="config.json"):
        self.data = {}

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logging.warning("Failed to load config file '%s': %s", file_path, e)

    def get_exercise_duration(self, class_name):
        """Return the exercise_duration override for the given class name, or None"""

        exercises = self.data.get("exercises", {})
        exercise_config = exercises.get(class_name, {})
        return exercise_config.get("exercise_duration", None)

    def get_mixer_duration(self, default=1200):
        """Return the mixer_duration setting, or the default"""

        return self.data.get("mixer_duration", default)
