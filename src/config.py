"""Configuration file loader for per-exercise and application settings"""

import json
import logging
import os

from src.midiutilities import MidiUtil


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

        m_u = MidiUtil()
        self.valid_key_centers = set(m_u.note_names)
        self.valid_intervalics = set(m_u.interval_pattern.keys())

    @staticmethod
    def _validate_list(raw_list, valid_set, setting_name, class_name):
        """Validate a list of values against a set of valid values.

        Returns the filtered list (only valid entries), or None if
        raw_list is not a list or all entries are invalid.
        """

        if not isinstance(raw_list, list):
            logging.warning(
                "Config '%s' for '%s' must be a list, got %s. Ignoring.",
                setting_name, class_name, type(raw_list).__name__
            )
            return None

        valid = []
        for item in raw_list:
            if item in valid_set:
                valid.append(item)
            else:
                logging.warning(
                    "Config '%s' for '%s': invalid value '%s'. Skipping.",
                    setting_name, class_name, item
                )

        if len(valid) == 0:
            logging.warning(
                "Config '%s' for '%s': no valid values remain. Using defaults.",
                setting_name, class_name
            )
            return None

        return valid

    def get_exercise_duration(self, class_name):
        """Return the exercise_duration override for the given class name, or None"""

        exercises = self.data.get("exercises", {})
        exercise_config = exercises.get(class_name, {})
        return exercise_config.get("exercise_duration", None)

    def get_mixer_duration(self, default=1200):
        """Return the mixer_duration setting, or the default"""

        return self.data.get("mixer_duration", default)

    def get_key_centers(self, class_name):
        """Return validated key_centers override for the given class name, or None"""

        exercises = self.data.get("exercises", {})
        exercise_config = exercises.get(class_name, {})
        raw = exercise_config.get("key_centers", None)
        if raw is None:
            return None
        return self._validate_list(raw, self.valid_key_centers, "key_centers", class_name)

    def get_intervalics(self, class_name):
        """Return validated intervalics override for the given class name, or None"""

        exercises = self.data.get("exercises", {})
        exercise_config = exercises.get(class_name, {})
        raw = exercise_config.get("intervalics", None)
        if raw is None:
            return None
        return self._validate_list(raw, self.valid_intervalics, "intervalics", class_name)
