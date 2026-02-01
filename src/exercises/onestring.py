"""OneString exercise"""

import random

from src.exercises.exercise import Exercise
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class OneString(Exercise):
    """Play single random notes on a single string"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "One String Exercise"
        mixable = True
        exercise_duration = 300     # 5 Minutes
        trials_sets_count = 10
        trials_count = 50
        trial_size = 1
        max_interval = 12  # One octave
        trial_range = 22   # The whole string
        # key_centers = ['C', 'F', 'G', 'A', 'E', 'B']
        # intervalics = ['Ionian', "Major Pentatonic", "Minor Pentatonic", 'Major', 'Minor',
        #               'Major Seventh', 'Dominant Seventh', 'Minor Seventh', 'Dorian', 'Lydian',
        #               'Mixolydian', 'Super Locrian']
        key_centers = ['C']
        intervalics = ['Chromatic']

        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.LONG,           # post trial pause
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.NOT_APPLICABLE,   # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        # Pass these to the parent class
        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size, max_interval, trial_range,
                         key_centers, intervalics, trial_varied_intervalics)

        # trial_range should match the guitar's fret count
        self.trial_range = self.g_u.max_frets

        # Remember across trial_sets
        self.remember_note_of_previous_trial_set = True

    def apply_config(self, config):
        """Apply config and update trial_range to match guitar fret count"""

        super().apply_config(config)
        self.trial_range = self.g_u.max_frets

    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range"""

        # Pick the string for the trial set.
        #  - String numbering is backwards (low E string is 0, high e is 5)
        guitar_string = random.randrange(0, 6)

        # Determine the Trial Set Range.
        #  - the midi note values for the high and low notes on the chosen string.
        b_e_string_corrector = 0
        if guitar_string > 3:   # did we pick the b or e string?
            b_e_string_corrector = 1
        low_note = self.low_estring_low_note + \
            (guitar_string * 5) - b_e_string_corrector
        high_note = self.low_estring_high_note + \
            (guitar_string * 5) - b_e_string_corrector

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        fret_string_list = self.g_u.get_fret_string_from_name(
            low_note_true_name, 0, 1)
        fret_string = fret_string_list[0]  # Should only be 1
        string = fret_string[1]  # This should be the name.

        # Build the intervalic string
        intervalic_string = self.build_intervalic_string(intervalic_list)

        # Build the string
        definition = "String: " + string + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic_string

        return definition
