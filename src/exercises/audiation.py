"""Audiation exercises"""

import random

from src.exercises.oneposition import OnePositionBase
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class AudiationBase(OnePositionBase):
    """Straight up chromatics"""

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        # Range is 2 octaves + minor 3rd
        high_note_true_name = self.m_u[low_note + 27]

        # Build the string
        definition = "Chromatic between " + \
            low_note_true_name + " and " + high_note_true_name

        return definition

    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range"""

        # Notes from the first 12 frets.
        estring_fret_start = random.randrange(0, 9)
        low_note = self.low_estring_low_note + estring_fret_start
        # Range is 2 octaves + minor 3rd
        high_note = low_note + 27

        return low_note, high_note


class AudiationEasy(AudiationBase):
    """Chromatics only."""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Chromatic Audiation Exercise (Easy)"
        mixable = False
        exercise_duration = 300     # in seconds
        trials_sets_count = 10
        trials_count = 20
        trial_size = 3
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = True
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,    # mid interval pause
            PauseDuration.NOT_APPLICABLE,    # trial repeat & duration
            True                             # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)


class AudiationHard(AudiationBase):
    """Chromatics only."""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Chromatic Audiation Exercise (Hard)"
        mixable = False
        exercise_duration = 300     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 5
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = True
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.NOT_APPLICABLE,   # trial repeat & duration
            True                           # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)
