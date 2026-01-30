"""Unit Tests for Application class"""
import unittest
from unittest.mock import MagicMock, patch

from src.application import Application


def make_mock_exercise(mixable=True, name="Exercise"):
    """Create a mock exercise object"""
    ex = MagicMock()
    ex.is_mixable.return_value = mixable
    ex.__str__ = MagicMock(return_value=name)
    return ex


class TestApplicationRegister(unittest.TestCase):
    """Tests for register_exercise()"""

    def test_register_adds_to_list(self):
        """Registered exercises appear in the exercises list"""
        app = Application()
        ex = make_mock_exercise()
        app.register_exercise(ex)
        self.assertIn(ex, app.exercises)
        self.assertEqual(len(app.exercises), 1)

    def test_register_updates_options(self):
        """Registering adds the index string to options"""
        app = Application()
        ex1 = make_mock_exercise()
        ex2 = make_mock_exercise()
        app.register_exercise(ex1)
        app.register_exercise(ex2)
        self.assertIn("0", app.options)
        self.assertIn("1", app.options)

    def test_register_multiple(self):
        """Multiple registrations grow the list"""
        app = Application()
        for _ in range(5):
            app.register_exercise(make_mock_exercise())
        self.assertEqual(len(app.exercises), 5)


class TestApplicationRunMixer(unittest.TestCase):
    """Tests for run_mixer()"""

    def test_no_mixable_raises(self):
        """RuntimeError when no mixable exercises exist"""
        app = Application()
        app.register_exercise(make_mock_exercise(mixable=False))
        with self.assertRaises(RuntimeError):
            app.run_mixer()

    @patch('src.application.time.time')
    @patch('src.application.random.choice')
    def test_calls_do_singleton(self, mock_choice, mock_time):
        """run_mixer calls do_singleton on a mixable exercise"""
        # Simulate: first time call returns start, second returns past duration
        mock_time.side_effect = [0.0, 1300.0]

        ex = make_mock_exercise(mixable=True)
        mock_choice.return_value = ex

        app = Application()
        app.register_exercise(ex)
        app.run_mixer()

        ex.do_singleton.assert_called_once()


class TestApplicationRunRandom(unittest.TestCase):
    """Tests for run_random()"""

    @patch('src.application.random.choice')
    def test_calls_do_exercise(self, mock_choice):
        """run_random calls do_exercise on a random exercise"""
        ex = make_mock_exercise()
        mock_choice.return_value = ex

        app = Application()
        app.register_exercise(ex)
        app.run_random()

        ex.do_exercise.assert_called_once()


class TestApplicationRunAllRandom(unittest.TestCase):
    """Tests for run_all_random()"""

    @patch('src.application.random.sample')
    def test_calls_do_exercise_on_all(self, mock_sample):
        """run_all_random calls do_exercise on every exercise"""
        exercises = [make_mock_exercise(name=f"Ex{i}") for i in range(3)]
        mock_sample.return_value = exercises

        app = Application()
        for ex in exercises:
            app.register_exercise(ex)

        app.run_all_random()

        for ex in exercises:
            ex.do_exercise.assert_called_once()
