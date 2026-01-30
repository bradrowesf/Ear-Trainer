"""Unit Tests for Player class"""
import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

# Mock scamp and keyboard before importing Player
sys.modules.setdefault('scamp', MagicMock())
sys.modules.setdefault('keyboard', MagicMock())

from src.player import Player, PlayerConst
from src.exercisepackage import ExerciseType, PauseDuration
from tests.helpers import make_series_package, make_interval_package


def make_player_with_mocks():
    """Create a Player with mocked scamp internals"""
    with patch('src.player.Session') as mock_session_cls:
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_part = MagicMock()
        mock_session.new_part.return_value = mock_part
        player = Player()
    return player


class TestPlayerFormatTimeString(unittest.TestCase):
    """Tests for _format_time_string()"""

    def setUp(self):
        self.player = make_player_with_mocks()

    def test_zero_seconds(self):
        """0 seconds formats as 00:00"""
        self.assertEqual(self.player._format_time_string(0), "00:00")

    def test_seconds_only(self):
        """45 seconds formats as 00:45"""
        self.assertEqual(self.player._format_time_string(45), "00:45")

    def test_minutes_and_seconds(self):
        """125 seconds formats as 02:05"""
        self.assertEqual(self.player._format_time_string(125), "02:05")

    def test_exact_minutes(self):
        """300 seconds formats as 05:00"""
        self.assertEqual(self.player._format_time_string(300), "05:00")

    def test_large_value(self):
        """3661 seconds formats as 61:01"""
        self.assertEqual(self.player._format_time_string(3661), "61:01")


class TestPlayerGetRemainingTime(unittest.TestCase):
    """Tests for _get_remaining_time()"""

    def setUp(self):
        self.player = make_player_with_mocks()

    @patch('src.player.time.time', return_value=110.0)
    def test_positive_remaining(self, mock_time):
        """Returns positive value when time remains"""
        result = self.player._get_remaining_time(100.0, 20.0)
        self.assertAlmostEqual(result, 10.0)

    @patch('src.player.time.time', return_value=130.0)
    def test_negative_remaining(self, mock_time):
        """Returns negative value when time is exceeded"""
        result = self.player._get_remaining_time(100.0, 20.0)
        self.assertAlmostEqual(result, -10.0)

    @patch('src.player.time.time', return_value=120.0)
    def test_zero_remaining(self, mock_time):
        """Returns zero when time is exactly used up"""
        result = self.player._get_remaining_time(100.0, 20.0)
        self.assertAlmostEqual(result, 0.0)


class TestPlayerExecuteTrial(unittest.TestCase):
    """Tests for _execute_trial() routing"""

    def setUp(self):
        self.player = make_player_with_mocks()

    @patch.object(Player, '_play_interval_trial', return_value=3.5)
    def test_routes_to_interval(self, mock_interval):
        """INTERVAL type routes to _play_interval_trial"""
        pkg = make_interval_package()
        trial = [60, 67]
        result = self.player._execute_trial(trial, 0, pkg)
        mock_interval.assert_called_once_with(trial, pkg)
        self.assertEqual(result, 3.5)

    @patch.object(Player, '_play_series_trial', return_value=True)
    def test_routes_to_series(self, mock_series):
        """SERIES type routes to _play_series_trial"""
        pkg = make_series_package()
        trial = [60, 62, 64]
        result = self.player._execute_trial(trial, 0, pkg)
        mock_series.assert_called_once_with(trial, pkg, 0)
        self.assertEqual(result, 0.0)

    @patch.object(Player, '_play_series_trial', return_value=True)
    def test_routes_to_series_hold_on_one(self, mock_series):
        """SERIES_HOLD_ON_ONE type routes to _play_series_trial"""
        pkg = make_series_package(exercise_type=ExerciseType.SERIES_HOLD_ON_ONE)
        trial = [60, 62]
        self.player._execute_trial(trial, 0, pkg)
        mock_series.assert_called_once_with(trial, pkg, 0)

    @patch.object(Player, '_play_series_trial', return_value=False)
    def test_series_exit_returns_negative(self, mock_series):
        """User exit from series trial returns -1.0"""
        pkg = make_series_package()
        trial = [60, 62, 64]
        result = self.player._execute_trial(trial, 0, pkg)
        self.assertEqual(result, -1.0)


class TestPlayerPlayIntervalTrial(unittest.TestCase):
    """Tests for _play_interval_trial()"""

    def setUp(self):
        self.player = make_player_with_mocks()

    @patch('src.player.wait')
    @patch('src.player.any_key_press')
    @patch('src.player.key_press_message', return_value='space')
    @patch('src.player.time.time')
    def test_returns_time_on_correct(self, mock_time, mock_kpm, mock_akp, mock_wait):
        """Returns elapsed time when user answers correctly"""
        # Simulate timing: first call is start, second is after key press
        mock_time.side_effect = [100.0, 103.5]

        pkg = make_interval_package(
            mid_trial_prompt_enabled=True,
            trial_repeat_pause=PauseDuration.MEDIUM,
        )
        trial = [60, 67]
        result = self.player._play_interval_trial(trial, pkg)
        self.assertAlmostEqual(result, 3.5)

    @patch('src.player.wait')
    @patch('src.player.any_key_press')
    @patch('src.player.key_press_message', return_value='x')
    @patch('src.player.time.time')
    def test_returns_max_on_wrong(self, mock_time, mock_kpm, mock_akp, mock_wait):
        """Returns 20 when user marks answer wrong"""
        mock_time.side_effect = [100.0, 102.0]

        pkg = make_interval_package(
            mid_trial_prompt_enabled=True,
            trial_repeat_pause=PauseDuration.MEDIUM,
        )
        trial = [60, 67]
        result = self.player._play_interval_trial(trial, pkg)
        self.assertEqual(result, 20)


class TestPlayerPlaySeriesTrial(unittest.TestCase):
    """Tests for _play_series_trial()"""

    def setUp(self):
        self.player = make_player_with_mocks()

    @patch('src.player.wait')
    def test_returns_true_on_continue(self, mock_wait):
        """Returns True when no prompt and no exit"""
        pkg = make_series_package(mid_trial_prompt_enabled=False,
                                  trial_repeat_pause=PauseDuration.NOT_APPLICABLE)
        trial = [60, 62, 64]
        result = self.player._play_series_trial(trial, pkg, 1)
        self.assertTrue(result)

    @patch('src.player.wait')
    @patch.object(Player, '_handle_series_interactive_options', return_value=False)
    def test_returns_false_on_exit(self, mock_handle, mock_wait):
        """Returns False when user chooses to exit"""
        pkg = make_series_package(mid_trial_prompt_enabled=True,
                                  trial_repeat_pause=PauseDuration.NOT_APPLICABLE)
        trial = [60, 62, 64]
        result = self.player._play_series_trial(trial, pkg, 1)
        self.assertFalse(result)

    @patch('src.player.wait')
    def test_hold_on_one_increases_pause(self, mock_wait):
        """First trial in SERIES_HOLD_ON_ONE gets multiplied pause"""
        pkg = make_series_package(
            exercise_type=ExerciseType.SERIES_HOLD_ON_ONE,
            mid_trial_prompt_enabled=False,
            trial_repeat_pause=PauseDuration.NOT_APPLICABLE
        )
        trial = [60, 62]
        self.player._play_series_trial(trial, pkg, 0)

        # The wait should have been called with the multiplied pause
        expected_pause = PlayerConst.HOLD_ON_ONE_MULTIPLIER * pkg.get_post_trial_pause()
        mock_wait.assert_called_with(expected_pause)
