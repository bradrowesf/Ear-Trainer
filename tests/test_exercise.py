"""Unit Tests for Exercise classes"""
import unittest

from exercise import OneString, ChordTones
from player import Player

# Some Utility Functions


def validate_trial_sets(legal_notes_lists, trial_set):
    """Ensures that the trial sets are pulling from the correct list"""

    for idx, trial in enumerate(trial_set):
        legal_notes_index = idx % len(legal_notes_lists)
        for note in trial:
            if note not in legal_notes_lists[legal_notes_index]:
                return False

    return True


class TestExercise(unittest.TestCase):
    """Testing Class"""

    @classmethod
    def setUpClass(cls):
        """Setup for all the tests"""
        cls.player = Player()

    def setUp(self):
        """Setup"""

        self.one_string = OneString(TestExercise.player)
        self.chord_tones = ChordTones(TestExercise.player)

    def test_build_trial_set(self):
        """Build Trial Set under many circumstances"""

        legal_notes_list1 = [[22, 24, 26, 28, 30]]
        legal_notes_list2 = [[22, 24, 26, 28, 30], [60, 62, 64, 68, 70]]

        # Test whether the count is correct and the selections match the right list.
        trial_set = self.one_string.build_trial_set(legal_notes_list1)
        self.assertEqual(len(trial_set), self.one_string.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list1, trial_set))
        self.assertFalse(validate_trial_sets(legal_notes_list2, trial_set))

        trial_set = self.one_string.build_trial_set(legal_notes_list2)
        self.assertEqual(len(trial_set), self.one_string.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list2, trial_set))
        self.assertFalse(validate_trial_sets(legal_notes_list1, trial_set))

        # Chord Tones test
        trial_set = self.chord_tones.build_trial_set(legal_notes_list1)
        self.assertEqual(len(trial_set), self.chord_tones.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list1, trial_set))
        self.assertFalse(validate_trial_sets(legal_notes_list2, trial_set))

        trial_set = self.chord_tones.build_trial_set(legal_notes_list2)
        self.assertEqual(len(trial_set), self.chord_tones.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list2, trial_set))
        self.assertFalse(validate_trial_sets(legal_notes_list1, trial_set))

    def test_one_string_methods(self):
        """Test method"""

        key_center, intervalic_list = self.one_string.get_key_intervalic()
        low_note, high_note = self.one_string.get_trial_set_range(
            key_center, intervalic_list)

        # We're on one string, so this should always be 22.
        self.assertEqual(high_note-low_note, 22)
