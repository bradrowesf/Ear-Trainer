"""OneOctave exercises"""

import random

from src.exercises.exercise import Exercise
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class OneOctaveBase(Exercise):
    """Base class for one octave exercises."""

    def get_trial_set_range(self, key_center, intervalic):
        """Chose a specific octave for testing"""

        # Find all the legal notes for the lowest note in our range
        #  - lowest note in the range can't be be within an octave of the highest note
        # legal_low_notes = self.m_u.build_note_list(
        #    self.low_estring_low_note, self.high_estring_high_note - 12, intervalic, key_center)

        # Get all the notes
        legal_low_notes = self.m_u.list_of_midi_notes(key_center)

        # Prune for legal notes
        def predicate(
            x): return self.low_estring_low_note <= x <= self.high_estring_high_note - 12
        legal_low_notes = [x for x in legal_low_notes if predicate(x)]

        # Pick one of them
        #   Legal_low_notes is now a list of lists, but there should only be
        #   one list in this exercise.
        # low_note = random.choice(legal_low_notes[0])
        low_note = random.choice(legal_low_notes)
        high_note = low_note + 12   # one octave higher

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build our definition string for the chosen trial set"""

        # What are all the possible places this low note could be.
        low_note_true_name = self.m_u[low_note]
        fret_string_list = self.g_u.get_fret_string_from_name(
            low_note_true_name, 0, 19, 3, 6)

        # Pick one of them
        fret_string = random.choice(fret_string_list)
        position = fret_string[0]   # This is the position of the exercise.

        # Build the intervalic string
        intervalic_string = self.build_intervalic_string(intervalic_list)

        # Build the return string
        definition = "Position: " + str(position) + "\n"
        definition += "Low note: " + low_note_true_name + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic_string

        return definition


class OneOctaveEasy(OneOctaveBase):
    """Play random notes, within a single octave"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Octave Exercise (Simple)"
        mixable = True
        exercise_duration = 300     # 5 minutes, in seconds
        trials_sets_count = 20
        trials_count = 50
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C', 'G', 'F', 'A', 'B', 'D', 'E']
        intervalics = ['Major', 'Minor', 'Major Seventh', 'Dominant Seventh',
                       'Minor Seventh', 'Major Pentatonic', 'Minor Pentatonic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.SHORT,            # post trial pause
            PauseDuration.NOT_APPLICABLE,   # interval pause
            PauseDuration.NOT_APPLICABLE,   # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)


class OneOctaveMedium(OneOctaveBase):
    """Play random notes, within a single octave"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Octave Exercise (On-Level)"
        mixable = True
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 20
        trials_count = 50
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C', 'G', 'F', 'A', 'B', 'D', 'E']
        intervalics = ['Ionian', 'Aeolian', 'Dorian',
                       'Mixolydian', 'Lydian', 'Phrygian', 'Locrian']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.SHORT,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.NOT_APPLICABLE,   # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)


class OneOctaveHard(OneOctaveBase):
    """Play random notes, within a single octave"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions (from parent)
        name = "Single Octave Exercise (Advanced)"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 20
        trials_count = 50
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C', 'G', 'F', 'A', 'B', 'D', 'E']
        intervalics = ['Super Locrian', 'Lydian Dominant',
                       'Harmonic Minor', 'Melodic Minor']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.SERIES,
            PauseDuration.MEDIUM,
            PauseDuration.NOT_APPLICABLE,   # mid interval pause
            PauseDuration.NOT_APPLICABLE,    # trial repeat & duration
            False                           # mid trial prompt enabled
        )

        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)
