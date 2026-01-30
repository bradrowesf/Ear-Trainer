"""Shared test helpers for the EarTrainer test suite"""

from unittest.mock import MagicMock

from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration


def make_mock_player():
    """Return a MagicMock that looks like Player without needing scamp"""
    from src.player import Player
    mock = MagicMock(spec=Player)
    return mock


def make_mock_scoreboard():
    """Return a MagicMock that looks like Scoreboard"""
    from src.scoreboard import Scoreboard
    mock = MagicMock(spec=Scoreboard)
    mock.get_test_prefix = MagicMock(side_effect=lambda name, el: f"{name}:{el}")
    mock.get_adjusted_element_score = MagicMock(return_value=20.0)
    return mock


def make_series_package(**overrides):
    """Factory for a valid SERIES ExercisePackage"""
    defaults = dict(
        exercise_type=ExerciseType.SERIES,
        post_trial_pause=PauseDuration.MEDIUM,
        interval_pause=PauseDuration.NOT_APPLICABLE,
        trial_repeat_pause=PauseDuration.NOT_APPLICABLE,
        mid_trial_prompt_enabled=False,
        scoring_enabled=False,
    )
    defaults.update(overrides)
    return ExercisePackage(**defaults)


def make_interval_package(**overrides):
    """Factory for a valid INTERVAL ExercisePackage"""
    defaults = dict(
        exercise_type=ExerciseType.INTERVAL,
        post_trial_pause=PauseDuration.MEDIUM,
        interval_pause=PauseDuration.NONE,
        trial_repeat_pause=PauseDuration.MEDIUM,
        mid_trial_prompt_enabled=True,
        scoring_enabled=True,
    )
    defaults.update(overrides)
    return ExercisePackage(**defaults)


def validate_trial_sets(legal_notes_lists, trial_set):
    """Ensures that the trial sets are pulling from the correct list"""

    for idx, trial in enumerate(trial_set):
        legal_notes_index = idx % len(legal_notes_lists)
        for note in trial:
            if note not in legal_notes_lists[legal_notes_index]:
                return False

    return True
