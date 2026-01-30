"""Unit Tests for Exercise classes"""
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock scamp and keyboard before any src imports that depend on them
sys.modules.setdefault('scamp', MagicMock())
sys.modules.setdefault('keyboard', MagicMock())

from src.exercise import (
    OneString, OneOctaveEasy, OneOctaveMedium, OneOctaveHard,
    OnePositionEasy, OnePositionMedium, OnePositionHard,
    ChordTones, AudiationEasy, AudiationHard,
    JustTheIntervals, SingTheIntervalsEasy, SingTheIntervalsMedium,
    SingTheIntervalsHard,
)
from src.exercisepackage import ExerciseType
from src.scoreboard import Scoreboard
from tests.helpers import make_mock_player, validate_trial_sets


class TestExerciseBase(unittest.TestCase):
    """Tests for Exercise base-class behavior via OneString"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def setUp(self):
        self.one_string = OneString(self.player, self.scoreboard)

    def test_str(self):
        """__str__ returns the exercise name"""
        self.assertEqual(str(self.one_string), "One String Exercise")

    def test_is_mixable_true(self):
        """OneString is mixable"""
        self.assertTrue(self.one_string.is_mixable())

    def test_is_mixable_false(self):
        """OneOctaveHard is NOT mixable"""
        ex = OneOctaveHard(self.player, self.scoreboard)
        self.assertFalse(ex.is_mixable())

    def test_get_key_intervalic_single(self):
        """When trial_varied_intervalics is False, returns a single-element list"""
        key_center, intervalic_list = self.one_string.get_key_intervalic()
        self.assertIn(key_center, self.one_string.key_centers)
        self.assertEqual(len(intervalic_list), 1)
        self.assertIn(intervalic_list[0], self.one_string.intervalics)

    def test_get_key_intervalic_varied(self):
        """When trial_varied_intervalics is True, returns full intervalics list"""
        ct = ChordTones(self.player, self.scoreboard)
        key_center, intervalic_list = ct.get_key_intervalic()
        self.assertIn(key_center, ct.key_centers)
        self.assertEqual(intervalic_list, ct.intervalics)

    def test_build_intervalic_string_single(self):
        """Single intervalic gives no comma"""
        result = self.one_string.build_intervalic_string(["Ionian"])
        self.assertEqual(result, "Ionian")

    def test_build_intervalic_string_multiple(self):
        """Multiple intervalics separated by commas"""
        result = self.one_string.build_intervalic_string(["ii7", "V7", "IMaj7"])
        self.assertEqual(result, "ii7, V7, IMaj7")


class TestBuildTrialSet(unittest.TestCase):
    """Tests for build_trial_set()"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def setUp(self):
        self.one_string = OneString(self.player, self.scoreboard)
        self.chord_tones = ChordTones(self.player, self.scoreboard)

    def test_trial_set_count_matches_single_list(self):
        """Trial set count equals trials_count with single legal notes list"""
        legal_notes_list1 = [[22, 24, 26, 28, 30]]
        trial_set = self.one_string.build_trial_set(legal_notes_list1)
        self.assertEqual(len(trial_set), self.one_string.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list1, trial_set))

    def test_trial_set_count_matches_multi_list(self):
        """Trial set count equals trials_count with multiple legal notes lists"""
        # Note: lists must be close enough for max_interval / remember_note constraints
        legal_notes_list2 = [[40, 42, 44, 46, 48], [44, 46, 48, 50, 52]]
        trial_set = self.one_string.build_trial_set(legal_notes_list2)
        self.assertEqual(len(trial_set), self.one_string.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list2, trial_set))

    def test_validation_mismatch(self):
        """Validation fails when checked against wrong legal notes"""
        legal_notes_list1 = [[22, 24, 26, 28, 30]]
        legal_notes_list_wrong = [[60, 62, 64, 68, 70]]

        trial_set = self.one_string.build_trial_set(legal_notes_list1)
        self.assertFalse(validate_trial_sets(legal_notes_list_wrong, trial_set))

    def test_chord_tones_trial_set_single_list(self):
        """Chord tones build correct trial sets from a single list"""
        legal_notes_list1 = [[40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60]]
        trial_set = self.chord_tones.build_trial_set(legal_notes_list1)
        self.assertEqual(len(trial_set), self.chord_tones.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list1, trial_set))

    def test_chord_tones_trial_set_multi_list(self):
        """Chord tones build correct trial sets cycling through lists"""
        legal_notes_list2 = [
            [40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60],
            [43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63]
        ]
        trial_set = self.chord_tones.build_trial_set(legal_notes_list2)
        self.assertEqual(len(trial_set), self.chord_tones.trials_count)
        self.assertTrue(validate_trial_sets(legal_notes_list2, trial_set))

    def test_trial_size(self):
        """Each trial has the configured number of notes"""
        legal = [[40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60]]
        trial_set = self.chord_tones.build_trial_set(legal)
        for trial in trial_set:
            self.assertEqual(len(trial), self.chord_tones.trial_size)

    def test_max_interval_constraint(self):
        """Adjacent notes within a trial don't exceed max_interval"""
        legal = [[40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62]]
        trial_set = self.chord_tones.build_trial_set(legal)
        for trial in trial_set:
            for i in range(1, len(trial)):
                self.assertLessEqual(
                    abs(trial[i] - trial[i-1]),
                    self.chord_tones.max_interval)


class TestOneString(unittest.TestCase):
    """Tests for OneString exercise"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def setUp(self):
        self.ex = OneString(self.player, self.scoreboard)

    def test_range_span(self):
        """Trial set range spans exactly 22 semitones (one string)"""
        key_center, intervalic_list = self.ex.get_key_intervalic()
        low, high = self.ex.get_trial_set_range(key_center, intervalic_list)
        self.assertEqual(high - low, 22)

    def test_exercise_type(self):
        """OneString uses SERIES type"""
        self.assertEqual(self.ex.e_p.get_exercise_type(), ExerciseType.SERIES)

    def test_remembers_previous_note(self):
        """OneString remembers notes across trial sets"""
        self.assertTrue(self.ex.get_remember_note_of_previous_trial_set())

    def test_name(self):
        """Exercise name is correct"""
        self.assertEqual(str(self.ex), "One String Exercise")


class TestOneOctaveVariants(unittest.TestCase):
    """Tests for OneOctave Easy/Medium/Hard"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_easy_range(self):
        """OneOctaveEasy has 12-semitone range"""
        ex = OneOctaveEasy(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 12)

    def test_medium_range(self):
        """OneOctaveMedium has 12-semitone range"""
        ex = OneOctaveMedium(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 12)

    def test_hard_range(self):
        """OneOctaveHard has 12-semitone range"""
        ex = OneOctaveHard(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 12)

    def test_easy_is_mixable(self):
        """OneOctaveEasy is mixable"""
        ex = OneOctaveEasy(self.player, self.scoreboard)
        self.assertTrue(ex.is_mixable())

    def test_medium_is_mixable(self):
        """OneOctaveMedium is mixable"""
        ex = OneOctaveMedium(self.player, self.scoreboard)
        self.assertTrue(ex.is_mixable())

    def test_hard_not_mixable(self):
        """OneOctaveHard is NOT mixable"""
        ex = OneOctaveHard(self.player, self.scoreboard)
        self.assertFalse(ex.is_mixable())


class TestOnePositionVariants(unittest.TestCase):
    """Tests for OnePosition Easy/Medium/Hard"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_easy_range(self):
        """OnePositionEasy has 27-semitone range"""
        ex = OnePositionEasy(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 27)

    def test_medium_range(self):
        """OnePositionMedium has 27-semitone range"""
        ex = OnePositionMedium(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 27)

    def test_hard_range(self):
        """OnePositionHard has 27-semitone range"""
        ex = OnePositionHard(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 27)

    def test_easy_is_mixable(self):
        """OnePositionEasy is mixable"""
        ex = OnePositionEasy(self.player, self.scoreboard)
        self.assertTrue(ex.is_mixable())

    def test_hard_not_mixable(self):
        """OnePositionHard is NOT mixable"""
        ex = OnePositionHard(self.player, self.scoreboard)
        self.assertFalse(ex.is_mixable())

    def test_definition_contains_position(self):
        """Build trial definition includes 'Position:'"""
        ex = OnePositionEasy(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        defn = ex.build_trial_definition(low, key, intv)
        self.assertIn("Position:", defn)


class TestChordTones(unittest.TestCase):
    """Tests for ChordTones exercise"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def setUp(self):
        self.ex = ChordTones(self.player, self.scoreboard)

    def test_varied_intervalics_flag(self):
        """ChordTones uses varied intervalics"""
        self.assertTrue(self.ex.trial_varied_intervalics)

    def test_intervalics_content(self):
        """ChordTones has ii7, V7, IMaj7"""
        self.assertEqual(self.ex.intervalics, ["ii7", "V7", "IMaj7"])

    def test_definition_contains_progression(self):
        """Definition string includes 'Progression:'"""
        key, intv = self.ex.get_key_intervalic()
        low, high = self.ex.get_trial_set_range(key, intv)
        defn = self.ex.build_trial_definition(low, key, intv)
        self.assertIn("Progression:", defn)

    def test_is_mixable(self):
        """ChordTones is mixable"""
        self.assertTrue(self.ex.is_mixable())


class TestAudiationVariants(unittest.TestCase):
    """Tests for Audiation Easy/Hard"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_easy_range(self):
        """AudiationEasy has 27-semitone range"""
        ex = AudiationEasy(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 27)

    def test_hard_range(self):
        """AudiationHard has 27-semitone range"""
        ex = AudiationHard(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        self.assertEqual(high - low, 27)

    def test_definition_contains_chromatic(self):
        """Definition includes 'Chromatic between'"""
        ex = AudiationEasy(self.player, self.scoreboard)
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        defn = ex.build_trial_definition(low, key, intv)
        self.assertIn("Chromatic between", defn)

    def test_easy_not_mixable(self):
        """AudiationEasy is NOT mixable"""
        ex = AudiationEasy(self.player, self.scoreboard)
        self.assertFalse(ex.is_mixable())


class TestJustTheIntervals(unittest.TestCase):
    """Tests for JustTheIntervals exercise"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def setUp(self):
        self.ex = JustTheIntervals(self.player, self.scoreboard)

    def test_full_neck_range(self):
        """Range spans the entire guitar neck"""
        key, intv = self.ex.get_key_intervalic()
        low, high = self.ex.get_trial_set_range(key, intv)
        # Low E open to high E fret 22
        self.assertGreater(high - low, 40)

    def test_definition_text(self):
        """Definition is 'All the notes'"""
        key, intv = self.ex.get_key_intervalic()
        low, high = self.ex.get_trial_set_range(key, intv)
        defn = self.ex.build_trial_definition(low, key, intv)
        self.assertEqual(defn, "All the notes")

    def test_remembers_previous_note(self):
        """JustTheIntervals remembers notes across trial sets"""
        self.assertTrue(self.ex.get_remember_note_of_previous_trial_set())

    def test_exercise_type(self):
        """Uses SERIES_HOLD_ON_ONE type"""
        self.assertEqual(self.ex.e_p.get_exercise_type(),
                         ExerciseType.SERIES_HOLD_ON_ONE)


class TestSingTheIntervals(unittest.TestCase):
    """Tests for SingTheIntervals Easy/Medium/Hard"""

    @classmethod
    def setUpClass(cls):
        cls.player = make_mock_player()
        cls.scoreboard = Scoreboard()

    def test_easy_trial_size(self):
        """SingTheIntervalsEasy has trial_size == 2"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        self.assertEqual(ex.trial_size, 2)

    def test_medium_trial_size(self):
        """SingTheIntervalsMedium has trial_size == 2"""
        ex = SingTheIntervalsMedium(self.player, self.scoreboard)
        self.assertEqual(ex.trial_size, 2)

    def test_hard_trial_size(self):
        """SingTheIntervalsHard has trial_size == 2"""
        ex = SingTheIntervalsHard(self.player, self.scoreboard)
        self.assertEqual(ex.trial_size, 2)

    def test_easy_candidate_intervals(self):
        """SingTheIntervalsEasy has 3 candidate intervals"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        self.assertEqual(ex.candidate_intervals, ['-M6', '-m7', '-m6'])

    def test_medium_candidate_intervals(self):
        """SingTheIntervalsMedium has all 22 intervals"""
        ex = SingTheIntervalsMedium(self.player, self.scoreboard)
        self.assertEqual(len(ex.candidate_intervals), 22)

    def test_hard_candidate_intervals(self):
        """SingTheIntervalsHard has all 22 intervals"""
        ex = SingTheIntervalsHard(self.player, self.scoreboard)
        self.assertEqual(len(ex.candidate_intervals), 22)

    def test_exercise_type_is_interval(self):
        """SingTheIntervals uses INTERVAL type"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        self.assertEqual(ex.e_p.get_exercise_type(), ExerciseType.INTERVAL)

    def test_scoring_enabled(self):
        """SingTheIntervals has scoring enabled"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        self.assertTrue(ex.e_p.get_scoring_enabled())

    @patch('builtins.print')
    def test_adjust_interval_frequency_weighting(self, mock_print):
        """adjust_interval_frequency populates practice_intervals"""
        sb = Scoreboard()
        ex = SingTheIntervalsEasy(make_mock_player(), sb)
        # Give all candidates the same score so weighting is equal
        for interval in ex.candidate_intervals:
            for _ in range(5):
                prefix = sb.get_test_prefix(ex.name, interval)
                sb.append_score(ex.name, interval, 5.0)

        ex.adjust_interval_frequency()

        self.assertGreater(len(ex.practice_intervals), 0)
        # All candidate intervals should appear
        for interval in ex.candidate_intervals:
            self.assertIn(interval, ex.practice_intervals)

    def test_not_mixable(self):
        """SingTheIntervals exercises are not mixable"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        self.assertFalse(ex.is_mixable())

    def test_build_trial_definition(self):
        """Definition starts with 'Sing a'"""
        ex = SingTheIntervalsEasy(self.player, self.scoreboard)
        ex.practice_interval_current = '-M6'
        key, intv = ex.get_key_intervalic()
        low, high = ex.get_trial_set_range(key, intv)
        defn = ex.build_trial_definition(low, key, intv)
        self.assertTrue(defn.startswith("Sing a"))
