"""All of the exercises, version 2"""
import random

from midiutilities import MidiUtil
from guitarutilities import GuitarUtil
from player_new import Player_new


class Exercise:
    """Parent Class for Exercises"""

    def __init__(self, name, series_size, trials_size, sequence_size, keys, modes) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.player = Player_new()

        # The configuration data
        self.name = name
        self.series_size = series_size
        self.trials_size = trials_size
        self.sequence_size = sequence_size
        self.keys = keys
        self.modes = modes

    def __str__(self):
        return self.name

    def do_exercise(self):
        """In child classes, do the exercise in question"""
        print(f"{self.name} -- Exercise not defined.")

    def output_exercise_title(self):
        """Visual for exercise"""

        print('---------------------------------------------------------------------')
        print(f"Exercise: {self.name}")
        print('---------------------------------------------------------------------')

    def output_series_information(self, series, strings, key_center, grouping, position):
        """Visual for series"""

        print("*****")
        print(f"Series: {series + 1} of {self.series_size}")
        print(f"String: {strings}")
        print(f"Key: {key_center}")
        print(f"Note Grouping: {grouping}")
        print(f"Position: {position}")
        print("*****")


class OneString(Exercise):
    """Play single random notes on a single string"""

    def __init__(self) -> None:

        # Definitions
        name = "One String Exercise"
        series_size = 10
        trials_size = 10
        sequence_size = 1
        keys = ["E", "A"]
        modes = ["Ionian"]

        super().__init__(name, series_size, trials_size, sequence_size, keys, modes)

    def do_exercise(self):
        """Run the one string random note exercise"""

        # Let us know what the exercise is.
        super().output_exercise_title()

        # What are the midi note values for our low estring
        estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # 6 string open
        estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 12))  # 6 string 12th fret

        # Iterate across the series
        for series in range(0, self.series_size):

            # Pick the string for the exercise
            guitar_string = random.randrange(0, 6)


class Sequence_Subsets(Exercise):
    """Play sequences where each trial is from a definted random subset"""

    def __init__(self) -> None:

        # Definitions
        name = "Sequence Subsets Exercise"
        series_size = 10
        trials_size = 10
        sequence_size = 3
        keys = ["E", "A"]
        modes = ["Ionian"]

        super().__init__(name, series_size, trials_size, sequence_size, keys, modes)

        # Child definitions only
        self.progression = ["I7", "IV7", "V7"]

    def do_exercise(self):
        """Run the sequence subset note exercise"""

        # Let us know the exercise
        super().output_exercise_title()

        # Set the range of midi note values for the roots of the exercise
        lower_limit = self.m_u.index(
            self.g_u.get_full_note_name(6, 5))  # A on E string
        upper_limit = self.m_u.index(
            self.g_u.get_full_note_name(3, 9))  # E on G string

        # Loop through the series.
        for series in range(0, self.series_size):

            # Choose the key center and mode
            key_center = random.choice(self.keys)

            # Select a specific root within our range
            possible_roots = self.m_u.list_of_midi_notes(
                key_center, lower_limit, upper_limit)
            root = random.choice(possible_roots)

            # Build the note lists
            random_offset = random.randrange(6)
            low_note = root - random_offset     # Down as much as perfect 4th
            high_note = low_note + 12    # Up an octave
            note_lists = []
            for chord in self.progression:
                note_list = self.m_u.build_note_lists(
                    low_note, high_note, key_center, chord)
                note_lists.append(note_list)

            # Build the position string.
            root_name = self.m_u[root]
            fret_string_list = self.g_u.get_fret_string_from_name(
                root_name, 0, 12, 3, 6)
            # If there's more than one, just pick one randomly.
            fret_string = random.choice(fret_string_list)
            position_str = "Root on " + \
                fret_string[1] + " fret " + str(fret_string[0])

            # Build the grouping string
            group_string = ""
            first_time = True
            for chord in self.progression:
                if not first_time:
                    first_time = False
                    group_string += " "  # Don't add a space before the first chord
                group_string += chord

            # Let us know about the series
            super().output_series_information(
                series, "All Strings", key_center, group_string, position_str)
