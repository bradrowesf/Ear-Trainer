"""Unit Tests for ExercisePackage, ExerciseType, and PauseDuration"""
import unittest

from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from tests.helpers import make_series_package, make_interval_package


class TestExerciseType(unittest.TestCase):
    """Tests for ExerciseType enum"""

    def test_validate_valid_types(self):
        """All enum members pass validation"""
        for member in ExerciseType:
            ExerciseType.validate(member)  # should not raise

    def test_validate_invalid_type_raises(self):
        """Non-member value raises IndexError or TypeError"""
        with self.assertRaises((IndexError, TypeError)):
            ExerciseType.validate("INVALID")

    def test_validate_invalid_int_raises(self):
        """Raw integer is not a member"""
        with self.assertRaises((IndexError, TypeError)):
            ExerciseType.validate(1)

    def test_enum_values(self):
        """Verify expected enum values"""
        self.assertEqual(ExerciseType.SERIES.value, 1)
        self.assertEqual(ExerciseType.SERIES_HOLD_ON_ONE.value, 2)
        self.assertEqual(ExerciseType.INTERVAL.value, 3)


class TestPauseDuration(unittest.TestCase):
    """Tests for PauseDuration enum"""

    def test_validate_valid_durations(self):
        """All enum members pass validation"""
        for member in PauseDuration:
            PauseDuration.validate(member)  # should not raise

    def test_validate_invalid_raises(self):
        """Non-member value raises IndexError or TypeError"""
        with self.assertRaises((IndexError, TypeError)):
            PauseDuration.validate(99.9)

    def test_float_values(self):
        """PauseDuration members are floats"""
        self.assertEqual(float(PauseDuration.NONE), 0.0)
        self.assertEqual(float(PauseDuration.BLIP), 0.5)
        self.assertEqual(float(PauseDuration.SHORT), 1.0)
        self.assertEqual(float(PauseDuration.MEDIUM), 3.0)
        self.assertEqual(float(PauseDuration.LONG), 5.0)
        self.assertEqual(float(PauseDuration.VLONG), 8.0)

    def test_is_float_subclass(self):
        """PauseDuration inherits from float"""
        self.assertIsInstance(PauseDuration.MEDIUM, float)


class TestExercisePackage(unittest.TestCase):
    """Tests for ExercisePackage"""

    def test_valid_series_construction(self):
        """SERIES package constructs without error"""
        pkg = make_series_package()
        self.assertEqual(pkg.get_exercise_type(), ExerciseType.SERIES)

    def test_valid_interval_construction(self):
        """INTERVAL package constructs without error"""
        pkg = make_interval_package()
        self.assertEqual(pkg.get_exercise_type(), ExerciseType.INTERVAL)

    def test_invalid_exercise_type_raises(self):
        """Non-ExerciseType value raises IndexError or TypeError"""
        with self.assertRaises((IndexError, TypeError)):
            ExercisePackage("BAD", PauseDuration.MEDIUM,
                            PauseDuration.NOT_APPLICABLE,
                            PauseDuration.NOT_APPLICABLE, False)

    def test_post_trial_pause_not_applicable_raises(self):
        """NOT_APPLICABLE is not allowed for post_trial_pause"""
        with self.assertRaises(ValueError):
            ExercisePackage(ExerciseType.SERIES, PauseDuration.NOT_APPLICABLE,
                            PauseDuration.NOT_APPLICABLE,
                            PauseDuration.NOT_APPLICABLE, False)

    def test_interval_requires_interval_pause(self):
        """INTERVAL type with NOT_APPLICABLE interval_pause raises ValueError"""
        with self.assertRaises(ValueError):
            ExercisePackage(ExerciseType.INTERVAL, PauseDuration.MEDIUM,
                            PauseDuration.NOT_APPLICABLE,
                            PauseDuration.MEDIUM, True)

    def test_interval_requires_trial_repeat_pause(self):
        """INTERVAL type with NOT_APPLICABLE trial_repeat_pause raises ValueError"""
        with self.assertRaises(ValueError):
            ExercisePackage(ExerciseType.INTERVAL, PauseDuration.MEDIUM,
                            PauseDuration.NONE,
                            PauseDuration.NOT_APPLICABLE, True)

    def test_series_rejects_interval_pause(self):
        """SERIES type with a real interval_pause raises ValueError"""
        with self.assertRaises(ValueError):
            ExercisePackage(ExerciseType.SERIES, PauseDuration.MEDIUM,
                            PauseDuration.NONE,
                            PauseDuration.NOT_APPLICABLE, False)

    def test_getters_return_construction_values(self):
        """All getters return values provided at construction"""
        pkg = ExercisePackage(
            ExerciseType.INTERVAL,
            PauseDuration.LONG,
            PauseDuration.SHORT,
            PauseDuration.BLIP,
            True,
            True
        )
        self.assertEqual(pkg.get_exercise_type(), ExerciseType.INTERVAL)
        self.assertEqual(pkg.get_post_trial_pause(), PauseDuration.LONG)
        self.assertEqual(pkg.get_interval_pause(), PauseDuration.SHORT)
        self.assertEqual(pkg.get_trial_repeat_pause(), PauseDuration.BLIP)
        self.assertTrue(pkg.get_mid_trial_prompt_enabled())
        self.assertTrue(pkg.get_scoring_enabled())

    def test_trial_repeat_enabled_true(self):
        """Repeat is enabled when trial_repeat_pause is not NOT_APPLICABLE"""
        pkg = make_interval_package(trial_repeat_pause=PauseDuration.MEDIUM)
        self.assertTrue(pkg.get_trial_repeat_enabled())

    def test_trial_repeat_enabled_false(self):
        """Repeat is disabled when trial_repeat_pause is NOT_APPLICABLE"""
        pkg = make_series_package(trial_repeat_pause=PauseDuration.NOT_APPLICABLE)
        self.assertFalse(pkg.get_trial_repeat_enabled())

    def test_set_get_test_name(self):
        """set_test_name / get_test_name round-trips"""
        pkg = make_series_package()
        self.assertEqual(pkg.get_test_name(), "")
        pkg.set_test_name("My Test")
        self.assertEqual(pkg.get_test_name(), "My Test")

    def test_append_and_len(self):
        """append_trial_set grows the package length"""
        pkg = make_series_package()
        self.assertEqual(len(pkg), 0)
        pkg.append_trial_set([[60, 62]], "def1", "label1")
        self.assertEqual(len(pkg), 1)
        pkg.append_trial_set([[64, 65]], "def2", "label2")
        self.assertEqual(len(pkg), 2)

    def test_iterator_yields_in_order(self):
        """Iterating yields (trial_set, definition, label) tuples in order"""
        pkg = make_series_package()
        pkg.append_trial_set([[1]], "d1", "l1")
        pkg.append_trial_set([[2]], "d2", "l2")

        results = list(pkg)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ([[1]], "d1", "l1"))
        self.assertEqual(results[1], ([[2]], "d2", "l2"))

    def test_iterator_raises_stop_iteration(self):
        """StopIteration raised after exhausting items"""
        pkg = make_series_package()
        pkg.append_trial_set([[1]], "d", "l")

        it = iter(pkg)
        next(it)
        with self.assertRaises(StopIteration):
            next(it)

    def test_reset_clears_all_data(self):
        """reset() clears name, trial_sets, definitions, and labels"""
        pkg = make_series_package()
        pkg.set_test_name("TestName")
        pkg.append_trial_set([[1, 2]], "def", "label")

        pkg.reset()

        self.assertEqual(pkg.get_test_name(), "")
        self.assertEqual(len(pkg), 0)

    def test_scoring_disabled_by_default(self):
        """scoring_enabled defaults to False"""
        pkg = make_series_package()
        self.assertFalse(pkg.get_scoring_enabled())

    def test_scoring_enabled_when_set(self):
        """scoring_enabled is True when passed"""
        pkg = make_interval_package(scoring_enabled=True)
        self.assertTrue(pkg.get_scoring_enabled())
