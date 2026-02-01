"""ChordTones exercise"""

from src.exercises.oneposition import OnePositionBase
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class ChordTones(OnePositionBase):
    """Play random notes, with each trial choosing from chord tones"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Chord Tones Exercise"
        mixable = True
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 5
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C', 'A', 'E', 'B', 'G']
        intervalics = ["ii7", "V7", "IMaj7"]
        trial_varied_intervalics = True
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,    # mid interval pause
            PauseDuration.MEDIUM,            # trial repeat & duration
            True                             # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        position = self.g_u.get_fret_from_full_note_name(low_note_true_name, 6)

        # Build the intervalic string
        intervalic_string = self.build_intervalic_string(intervalic_list)

        # Build the string
        definition = "Position: " + str(position) + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Progression: " + intervalic_string

        return definition
