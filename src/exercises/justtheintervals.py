"""JustTheIntervals exercise"""

from src.exercises.exercise import Exercise
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class JustTheIntervals(Exercise):
    """Play single notes, one after the other, an octave or less apart"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions
        name = "Full Neck Sub-Octave Intervals"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 20
        trials_count = 20
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES_HOLD_ON_ONE,
            PauseDuration.LONG,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.NOT_APPLICABLE,   # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        # Pass these to the parent class
        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        # trial_range is the full neck span
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

        # Remember across trial_sets
        self.remember_note_of_previous_trial_set = True

    def apply_config(self, config):
        """Apply config and recompute trial_range for full neck span"""

        super().apply_config(config)
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range"""

        # All the notes
        low_note = self.low_estring_low_note
        high_note = self.high_estring_high_note

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        return "All the notes"
