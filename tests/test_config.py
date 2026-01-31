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
from src.exercise import OneString, OneOctaveEasy


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


class TestConfigKeyCenters(unittest.TestCase):
    """Tests for get_key_centers()"""

    def test_returns_valid_key_centers(self):
        """Returns the key_centers list when all values are valid"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": ["C", "G", "F"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_key_centers("OneOctaveEasy"), ["C", "G", "F"])
        finally:
            os.unlink(path)

    def test_returns_none_for_unlisted_exercise(self):
        """Returns None for an exercise not in the config"""
        config = Config("nonexistent.json")
        self.assertIsNone(config.get_key_centers("OneString"))

    def test_filters_invalid_key_centers(self):
        """Invalid key center values are filtered out with warnings"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": ["C", "X", "G"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING') as cm:
                result = config.get_key_centers("OneOctaveEasy")
            self.assertEqual(result, ["C", "G"])
            self.assertTrue(any("invalid value 'X'" in msg for msg in cm.output))
        finally:
            os.unlink(path)

    def test_all_invalid_returns_none(self):
        """When ALL key centers are invalid, returns None"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": ["X", "Y", "Z"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING'):
                result = config.get_key_centers("OneOctaveEasy")
            self.assertIsNone(result)
        finally:
            os.unlink(path)

    def test_non_list_type_returns_none(self):
        """When key_centers is not a list, returns None with warning"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": "C"}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING') as cm:
                result = config.get_key_centers("OneOctaveEasy")
            self.assertIsNone(result)
            self.assertTrue(any("must be a list" in msg for msg in cm.output))
        finally:
            os.unlink(path)

    def test_all_twelve_chromatic_notes_valid(self):
        """All 12 chromatic note names are accepted"""
        all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        data = {"exercises": {"OneString": {"key_centers": all_notes}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_key_centers("OneString"), all_notes)
        finally:
            os.unlink(path)


class TestConfigIntervalics(unittest.TestCase):
    """Tests for get_intervalics()"""

    def test_returns_valid_intervalics(self):
        """Returns the intervalics list when all values are valid"""
        data = {"exercises": {"OneOctaveEasy": {
            "intervalics": ["Major", "Minor", "Ionian"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_intervalics("OneOctaveEasy"),
                             ["Major", "Minor", "Ionian"])
        finally:
            os.unlink(path)

    def test_returns_none_for_unlisted_exercise(self):
        """Returns None for an exercise not in the config"""
        config = Config("nonexistent.json")
        self.assertIsNone(config.get_intervalics("OneString"))

    def test_filters_invalid_intervalics(self):
        """Invalid intervalic values are filtered out with warnings"""
        data = {"exercises": {"OneOctaveEasy": {
            "intervalics": ["Major", "FakeMode", "Dorian"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING') as cm:
                result = config.get_intervalics("OneOctaveEasy")
            self.assertEqual(result, ["Major", "Dorian"])
            self.assertTrue(any("invalid value 'FakeMode'" in msg for msg in cm.output))
        finally:
            os.unlink(path)

    def test_all_invalid_returns_none(self):
        """When ALL intervalics are invalid, returns None"""
        data = {"exercises": {"OneOctaveEasy": {
            "intervalics": ["FakeA", "FakeB"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING'):
                result = config.get_intervalics("OneOctaveEasy")
            self.assertIsNone(result)
        finally:
            os.unlink(path)

    def test_non_list_type_returns_none(self):
        """When intervalics is a string instead of list, returns None"""
        data = {"exercises": {"OneOctaveEasy": {"intervalics": "Ionian"}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING'):
                result = config.get_intervalics("OneOctaveEasy")
            self.assertIsNone(result)
        finally:
            os.unlink(path)


class TestApplyConfigKeyCentersIntervalics(unittest.TestCase):
    """Tests for Exercise.apply_config() with key_centers and intervalics"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_key_centers_override_replaces_defaults(self):
        """apply_config replaces key_centers with config values"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": ["C", "G"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            ex.apply_config(config)
            self.assertEqual(ex.key_centers, ["C", "G"])
        finally:
            os.unlink(path)

    def test_intervalics_override_replaces_defaults(self):
        """apply_config replaces intervalics with config values"""
        data = {"exercises": {"OneOctaveEasy": {
            "intervalics": ["Ionian", "Dorian"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            ex.apply_config(config)
            self.assertEqual(ex.intervalics, ["Ionian", "Dorian"])
        finally:
            os.unlink(path)

    def test_no_override_preserves_defaults(self):
        """apply_config leaves key_centers and intervalics unchanged when not in config"""
        config = Config("nonexistent.json")
        ex = OneOctaveEasy(self.player, self.scoreboard)
        original_kc = ex.key_centers.copy()
        original_intv = ex.intervalics.copy()
        ex.apply_config(config)
        self.assertEqual(ex.key_centers, original_kc)
        self.assertEqual(ex.intervalics, original_intv)

    def test_all_invalid_key_centers_preserves_defaults(self):
        """When all config key_centers are invalid, hardcoded defaults are kept"""
        data = {"exercises": {"OneOctaveEasy": {"key_centers": ["X", "Y"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            original_kc = ex.key_centers.copy()
            with self.assertLogs(level='WARNING'):
                ex.apply_config(config)
            self.assertEqual(ex.key_centers, original_kc)
        finally:
            os.unlink(path)

    def test_all_invalid_intervalics_preserves_defaults(self):
        """When all config intervalics are invalid, hardcoded defaults are kept"""
        data = {"exercises": {"OneOctaveEasy": {"intervalics": ["Fake"]}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            original_intv = ex.intervalics.copy()
            with self.assertLogs(level='WARNING'):
                ex.apply_config(config)
            self.assertEqual(ex.intervalics, original_intv)
        finally:
            os.unlink(path)

    def test_combined_all_three_overrides(self):
        """Config can override duration, key_centers, and intervalics simultaneously"""
        data = {"exercises": {"OneOctaveEasy": {
            "exercise_duration": 999,
            "key_centers": ["A", "B"],
            "intervalics": ["Chromatic"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            ex.apply_config(config)
            self.assertEqual(ex.exercise_duration, 999)
            self.assertEqual(ex.key_centers, ["A", "B"])
            self.assertEqual(ex.intervalics, ["Chromatic"])
        finally:
            os.unlink(path)

    def test_partial_invalid_key_centers_keeps_valid_ones(self):
        """Partially invalid key_centers list keeps only valid entries"""
        data = {"exercises": {"OneOctaveEasy": {
            "key_centers": ["C", "InvalidNote", "E"]
        }}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            ex = OneOctaveEasy(self.player, self.scoreboard)
            with self.assertLogs(level='WARNING'):
                ex.apply_config(config)
            self.assertEqual(ex.key_centers, ["C", "E"])
        finally:
            os.unlink(path)


class TestConfigGuitarType(unittest.TestCase):
    """Tests for Config.get_guitar_type()"""

    def test_returns_22_when_absent(self):
        """Returns default 22 when guitar_type is not in config"""
        config = Config("nonexistent.json")
        self.assertEqual(config.get_guitar_type(), 22)

    def test_maps_guitar20(self):
        """Guitar20 maps to 20"""
        data = {"guitar_type": "Guitar20"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_guitar_type(), 20)
        finally:
            os.unlink(path)

    def test_maps_guitar22(self):
        """Guitar22 maps to 22"""
        data = {"guitar_type": "Guitar22"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_guitar_type(), 22)
        finally:
            os.unlink(path)

    def test_maps_guitar24(self):
        """Guitar24 maps to 24"""
        data = {"guitar_type": "Guitar24"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            self.assertEqual(config.get_guitar_type(), 24)
        finally:
            os.unlink(path)

    def test_invalid_value_logs_warning_returns_22(self):
        """Invalid guitar_type logs warning and returns default 22"""
        data = {"guitar_type": "Guitar23"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            json.dump(data, f)
            path = f.name
        try:
            config = Config(path)
            with self.assertLogs(level='WARNING') as cm:
                result = config.get_guitar_type()
            self.assertEqual(result, 22)
            self.assertTrue(any("invalid value 'Guitar23'" in msg for msg in cm.output))
        finally:
            os.unlink(path)
