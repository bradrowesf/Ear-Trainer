"""OnePosition exercises"""

import random

from src.exercises.exercise import Exercise
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class OnePositionBase(Exercise):
    """A base class for single position exercises"""

    def get_trial_set_range(self, key_center, intervalic):
        """Determine the position we'll be playing in and the range of pitches available"""

        # Find the legal notes on the low estring for the key_center and intervalic
        #  - midi note values, natch
        #  - lowest note in the range cannot be above the 19th fret
        legal_low_notes_list = self.m_u.build_note_list(
            self.low_estring_low_note, self.low_estring_high_note - 3, intervalic, key_center)

        # First, we need a single list.
        legal_low_notes = []
        for notes in legal_low_notes_list:
            for note in notes:
                legal_low_notes.append(note)

        # Now remove the dupicates
        legal_low_notes_sans_dupes = list(set(legal_low_notes))

        # Pick one of them
        low_note = random.choice(legal_low_notes_sans_dupes)
        high_note = low_note + 27  # up 2 octaves and a minor 3rd

        return low_note, high_note


class OnePositionEMH(OnePositionBase):
    """Play random notes, but in a specific position"""

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
        definition += "Intervalic: " + intervalic_string

        return definition


class OnePositionEasy(OnePositionEMH):
    """Easy single position exercise"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Position Exercise (Simple)"
        mixable = True
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 3
        max_interval = 11  # 1 octave (-1)
        trial_range = 19   # 1 octave + perfect 5th

        key_centers = ['C', 'F', 'G', 'A', 'B', 'D']
        intervalics = ['Major', 'Minor', 'Major Seventh', 'Minor Seventh',
                       'Dominant Seventh', 'Major Pentatonic', 'Minor Pentatonic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,    # mid interval pause
            PauseDuration.MEDIUM,           # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)


class OnePositionMedium(OnePositionEMH):
    """Medium single position exercise"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Position Exercise (On-Level)"
        mixable = True
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 5
        max_interval = 11  # 1 octave (-1)
        trial_range = 19   # 1 octave + perfect 5th

        key_centers = ['C', 'F', 'G', 'A', 'B', 'D']
        intervalics = ['Ionian', 'Aeolian', 'Mixolydian', 'Dorian']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.MEDIUM,           # trial repeat & duration
            True                            # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)


class OnePositionHard(OnePositionEMH):
    """Hard single position exercise"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Position Exercise (Advanced)"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 5
        max_interval = 11  # 1 octave (-1)
        trial_range = 19   # 1 octave + perfect 5th

        key_centers = ['C', 'F', 'G', 'A', 'B', 'D']
        intervalics = ['Melodic Minor', 'Harmonic Minor',
                       'Super Locrian', 'Lydian Dominant']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.MEDIUM,           # trial repeat & duration
            True                            # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)
