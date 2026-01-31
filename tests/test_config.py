"""Unit Tests for Config class"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock

from src.config import Config

# Mock scamp and keyboard before any src imports that depend on them
sys.modules.setdefault('scamp', MagicMock())
sys.modules.setdefault('keyboard', MagicMock())

from tests.helpers import make_mock_player
from src.scoreboard import Scoreboard
from src.exercise import OneString


class TestConfigLoad(unittest.TestCase):
    """Tests for loading the config file"""

    def test_missing_file_uses_empty_defaults(self):
        """Config with nonexistent file produces empty data"""
        config = Config("nonexistent_file.json")
        self.assertEqual(config.data, {})

    def test_valid_file_loads(self):
        """Config loads a valid JSON file correctly"""
        data = {
            "mixer_duration": 900,
            "exercises": {
                "OneString": {"exercise_duration": 120}
            }
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name

        try:
            config = Config(path)
            self.assertEqual(config.data, data)
        finally:
            os.unlink(path)

    def test_malformed_file_logs_warning(self):
        """Malformed JSON results in empty data and a warning"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            f.write("{bad json")
            path = f.name

        try:
            with self.assertLogs(level='WARNING') as cm:
                config = Config(path)
            self.assertEqual(config.data, {})
            self.assertTrue(any("Failed to load config" in msg for msg in cm.output))
        finally:
            os.unlink(path)


class TestConfigExerciseDuration(unittest.TestCase):
    """Tests for get_exercise_duration()"""

    def setUp(self):
        self.data = {
            "exercises": {
                "OneString": {"exercise_duration": 120},
                "OneOctaveEasy": {"exercise_duration": 600}
            }
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(self.data, f)
            self.path = f.name
        self.config = Config(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_returns_override_value(self):
        """Returns the configured duration for a listed exercise"""
        self.assertEqual(self.config.get_exercise_duration("OneString"), 120)

    def test_returns_none_for_unlisted(self):
        """Returns None for an exercise not in the config"""
        self.assertIsNone(self.config.get_exercise_duration("ChordTones"))

    def test_returns_none_when_no_exercises_key(self):
        """Returns None when config has no exercises section"""
        config = Config("nonexistent.json")
        self.assertIsNone(config.get_exercise_duration("OneString"))


class TestConfigMixerDuration(unittest.TestCase):
    """Tests for get_mixer_duration()"""

    def test_returns_configured_value(self):
        """Returns the mixer_duration from config"""
        data = {"mixer_duration": 900}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name

        try:
            config = Config(path)
            self.assertEqual(config.get_mixer_duration(), 900)
        finally:
            os.unlink(path)

    def test_returns_default_when_absent(self):
        """Returns the default when mixer_duration is not in config"""
        config = Config("nonexistent.json")
        self.assertEqual(config.get_mixer_duration(), 1200)

    def test_returns_custom_default(self):
        """Respects a custom default parameter"""
        config = Config("nonexistent.json")
        self.assertEqual(config.get_mixer_duration(default=600), 600)


class TestApplyConfig(unittest.TestCase):
    """Tests for Exercise.apply_config() integration"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_overrides_exercise_duration(self):
        """apply_config changes exercise_duration when config has a value"""
        data = {"exercises": {"OneString": {"exercise_duration": 999}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name

        try:
            config = Config(path)
            ex = OneString(self.player, self.scoreboard)
            original = ex.exercise_duration
            ex.apply_config(config)
            self.assertEqual(ex.exercise_duration, 999)
            self.assertNotEqual(ex.exercise_duration, original)
        finally:
            os.unlink(path)

    def test_no_override_keeps_default(self):
        """apply_config does not change duration when exercise is not in config"""
        config = Config("nonexistent.json")
        ex = OneString(self.player, self.scoreboard)
        original = ex.exercise_duration
        ex.apply_config(config)
        self.assertEqual(ex.exercise_duration, original)
