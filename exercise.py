"""All of the exercises"""
import random

from midiutilities import MidiUtil
from guitarutilities import GuitarUtil


class Exercise:
    """Parent Class for all the Exercises"""

    def __init__(self, player, name, count, p_duration,
                 m_duration, modes, l_modes, keys, l_keys) -> None:

        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()

        self.player = player
        self.name = name
        self.count = count
        self.practice_duration = p_duration
        self.maintenance_duration = m_duration
        self.modes = modes
        self.learning_modes = l_modes
        self.keys = keys
        self.learning_keys = l_keys

    def __str__(self):
        return self.name

    def key_string(self, key, mode):
        """Format so the key center includes exercise mode"""

        key_string = key + " " + mode
        return key_string

    def do_exercise(self):
        """In child classes, do the exercise in question"""
        print(f"{self.name} -- Exercise not defined.")

    def get_key_duration_mode(self, series):
        """Common method for establishing the key and duration of the test"""

        # Pick a random key center -- SANS-octave name
        # Set practice duration based on whether we're learning or maintaining the key in question.
        # Pick a random mode

        key_center = ""
        duration = 0
        mode = ""
        # If there are no learning keys, just do maintenance
        if len(self.learning_keys) == 0 or (series % 2) == 0:
            key_center = random.choice(self.keys)
            mode = random.choice(self.modes)
            duration = self.maintenance_duration
        else:
            key_center = random.choice(self.learning_keys)
            mode = random.choice(self.learning_modes)
            duration = self.practice_duration

        return key_center, duration, mode

    def play_to_identify(self, notes):
        """Play a series of notes that typically identifies the string or the key of the exercise"""

        # notes should be a list of notes
        self.player.set_notes(notes)
        self.player.set_duration(2)
        self.player.play_notes()

    def identify_key_center(self, key_center, mode):
        """Play an arpeggio built off the passed midi note value"""

        key_id_note = self.g_u.get_lowest_full_note_on_string(
            key_center, 6)  # Note string w/ octave
        key_id_value = self.m_u.index(key_id_note)  # Midi note value

        # Get the correct arpeggio type.
        arpeggio = self.m_u.get_chord_for_mode(mode)

        # Get the notes of a major arpegio
        notes = self.m_u.build_from_intervals(key_id_value, arpeggio)

        # Play them
        self.play_to_identify(notes)

    def output_exercise_title(self):
        """Visual for exercise"""

        print('---------------------------------------------------------------------')
        print(f"Exercise: {self.name}")
        print('---------------------------------------------------------------------')

    def output_series_information(self, series, strings, key, mode, position):
        """Visual for series"""

        print("*****")
        print(f"Series: {series + 1} of {self.count}")
        print(f"String: {strings}")
        print(f"Key: {self.key_string(key,mode)}")
        print(f"Position: {position}")
        print("*****")


class OneStringParent(Exercise):
    """Parent for play single random notes on a single string"""

    def do_exercise(self):
        """Run the one string random note exercise"""

        # Let us know what the exercise is.
        super().output_exercise_title()

        # What are the midi note values for our low estring
        estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # 6 string open
        estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 12))  # 6 string 12th fret

        for series in range(0, self.count):

            # Pick the string
            guitar_string = random.randrange(0, 6)

            # Pick the key and duration
            key_center, duration, mode = super().get_key_duration_mode(series)

            # Let us know about the series
            super().output_series_information(series, self.g_u.get_string_from_reverse_number(
                guitar_string), key_center, mode, "Full String")

            # Determine the midi note values for the low and high notes.
            b_e_string_corrector = 0
            if guitar_string > 3:   # did we pick the b or e string?
                b_e_string_corrector = 1
            low_note = estring_low_note + \
                (guitar_string * 5) - b_e_string_corrector
            high_note = estring_high_note + \
                (guitar_string * 5) - b_e_string_corrector

            # Audibly identify the string
            super().play_to_identify([low_note, high_note])

            # Audibly identify the key center
            super().identify_key_center(key_center, mode)

            # Play the test notes
            test_notes = self.m_u.build_note_list(
                low_note, high_note, mode, key_center)
            self.player.set_notes(test_notes)
            self.player.set_duration(duration)
            self.player.random_play()


class OneString(OneStringParent):
    """Play single random notes on a single string"""

    def __init__(self, player) -> None:

        # Definitions
        name = "One String Exercise"
        count = 10
        practice_duration = 6
        maintenance_duration = 4
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C"]
        learning_keys = ["D", "G", "B", "F#"]

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)


class HammerOneString(OneStringParent):
    """Play single random notes, but lots and fast"""

    def __init__(self, player) -> None:

        # Definitions
        name = "One String Hammer Exercise"
        count = 10
        practice_duration = 4
        maintenance_duration = 3
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C"]
        learning_keys = ["D", "G", "B", "F#"]

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)

    def do_exercise(self):
        """Run the exercise"""

        # Get the current player count, so we can reset it.
        pre_count = self.player.get_count()

        # Do the exercise
        self.player.set_count(50)
        super().do_exercise()

        # Reset
        self.player.set_count(pre_count)


class TwoString(Exercise):
    """Play single random notes across two adjacent strings"""

    def __init__(self, player) -> None:

        # Definitions
        name = "Two String Exercise"
        count = 10
        practice_duration = 8
        maintenance_duration = 6
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C"]
        learning_keys = ["D", "G", "B", "F#"]

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)

    def do_exercise(self):
        """Run the two string random note exercise"""

        super().output_exercise_title()

        # What are the midi note values for low e and a string
        estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # 6 string open
        astring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(5, 12))  # 5 string 12th fret

        for series in range(0, self.count):

            # Pick a random string pair -- by selecting the lower of the 2 strings.
            guitar_pair_lower = random.randrange(
                0, 5)    # 0 - Low E string; 5 - B string

            # Pick the key and duration
            key_center, duration, mode = super().get_key_duration_mode(series)

            # Get the names of the strings in question
            low_note_str = self.g_u.get_string_from_reverse_number(
                guitar_pair_lower)
            high_note_str = self.g_u.get_string_from_reverse_number(
                guitar_pair_lower + 1)

            # Format it for display
            guitar_string_text = low_note_str + " and " + high_note_str

            # Show it to the user
            super().output_series_information(
                series, guitar_string_text, key_center, mode, "Full String")

            # ID the midi note value for the low string
            low_note = estring_low_note + (guitar_pair_lower * 5)

            # ID the midi note value high string
            high_note = astring_high_note + (guitar_pair_lower * 5)

            # Adjust if we've chosen 3 & 2 or 2 & 1 (i.e that pesky major 3rd)
            if guitar_pair_lower == 3:
                high_note -= 1
            elif guitar_pair_lower == 4:
                high_note -= 1
                low_note -= 1

            # Audibly ID the strings
            # The midi note values for the strings in question
            id_notes = [low_note, high_note - 12]
            super().play_to_identify(id_notes)

            # Audibly ID the key center
            super().identify_key_center(key_center, mode)

            # Play the test notes
            test_notes = self.m_u.build_note_list(
                low_note, high_note, mode, key_center)
            self.player.set_notes(test_notes)
            self.player.set_duration(duration)
            self.player.random_play()


class OnePosition(Exercise):
    """Notes from a single fretboard position"""

    def __init__(self, player) -> None:

        # Definitions
        name = "One Position Exercise"
        count = 10
        practice_duration = 6
        maintenance_duration = 4
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C"]
        learning_keys = ["D", "G", "B", "F#"]

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)

    def do_exercise(self):
        """Run the one position random note exercise"""

        super().output_exercise_title()

        for series in range(0, self.count):

            # Choose the position
            position = random.randrange(0, 13)

            # Pick key and duration
            key_center, duration, mode = super().get_key_duration_mode(series)

            # Tell the user what's up
            super().output_series_information(
                series, "All Strings", key_center, mode, position)

            # Audibly ID the key center
            super().identify_key_center(key_center, mode)

            # Get the midi note values for the range of notes
            low_note = self.m_u.index(self.g_u.get_full_note_name(6, position))
            high_note = self.m_u.index(
                self.g_u.get_full_note_name(1, position + 4))

            # Get the notes in the range in the key
            test_notes = self.m_u.build_note_list(
                low_note, high_note, mode, key_center)

            # Play the test
            self.player.set_notes(test_notes)
            self.player.set_duration(duration)
            self.player.random_play(True)


class Sequence(Exercise):
    """Notes from a single fretboard position"""

    def __init__(self, player) -> None:

        # Definitions
        name = "Sequence Exercise"
        count = 10
        practice_duration = 4
        maintenance_duration = 2
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C"]
        learning_keys = ["D", "G", "B", "F#"]

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)

        # Defined in the child only
        self.sequence_size = 2

    def do_exercise(self):
        """Run the sequence note exercise"""

        # Let us know the exercise
        super().output_exercise_title()

        # Set the range of midi note values for the roots of the exercise
        lower_limit = self.m_u.index(
            self.g_u.get_full_note_name(6, 5))  # A on E string
        upper_limit = self.m_u.index(
            self.g_u.get_full_note_name(3, 9))  # E on G string

        # Loop
        for series in range(0, self.count):

            # Pick the key and duration
            key_center, duration, mode = super().get_key_duration_mode(series)

            # Now select the root in question
            possible_roots = self.m_u.list_of_midi_notes(
                key_center, lower_limit, upper_limit)
            root = random.choice(possible_roots)

            # Build the position string.
            root_name = self.m_u[root]
            fret_string_list = self.g_u.get_fret_string_from_name(
                root_name, 0, 12, 3, 6)
            # If there's more than one, just pick one randomly.
            fret_string = random.choice(fret_string_list)
            position_str = "Root on " + \
                fret_string[1] + " fret " + str(fret_string[0])

            # Let us know about the series
            super().output_series_information(
                series, "All Strings", key_center, mode, position_str)

            # Build our test note range
            low_note = root - 5     # Down a perfect 4th
            high_note = root + 16    # Up a major 10th
            test_notes = self.m_u.build_note_list(
                low_note, high_note, mode, key_center)

            # Play the test notes
            self.player.set_notes(test_notes)
            self.player.set_duration(duration)
            self.player.random_play_sequence(
                self.sequence_size, True)   # Pause between sequences


class Simon(Exercise):
    """Notes from a single fretboard position"""

    def __init__(self, player) -> None:

        # Definitions
        name = "Simon Exercise"
        count = 10
        practice_duration = 6
        maintenance_duration = 2
        modes = ["Ionian", "Aeolian"]
        learning_modes = ["Mixolydian", "Dorian"]
        keys = ["E", "A", "C", "D", "G", "B", "F#", "C#"]
        learning_keys = []

        super().__init__(player, name, count, practice_duration,
                         maintenance_duration, modes, learning_modes, keys, learning_keys)

        self.simon_max_size = 8

    def do_exercise(self):
        """Run the Simon exercise"""

        # Let us know the exercise
        super().output_exercise_title()

        # Set the range of midi note values for the roots of the exercise
        lower_limit = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))  # Low E on Low E string
        upper_limit = self.m_u.index(
            self.g_u.get_full_note_name(3, 9))  # E on G string

        # Loop through each trial
        for series in range(self.count):

            # Get the key and note duration
            key_center, duration, mode = super().get_key_duration_mode(series)

            # Let's figure out the root we'll be using
            possible_roots = self.m_u.list_of_midi_notes(
                key_center, lower_limit, upper_limit)
            root = random.choice(possible_roots)

            # Build the position string.
            root_name = self.m_u[root]
            fret_string_list = self.g_u.get_fret_string_from_name(
                root_name, 0, 12, 3, 6)
            # If there's more than one, just pick one randomly.
            fret_string = random.choice(fret_string_list)
            position_str = "Root on " + \
                fret_string[1] + " fret " + str(fret_string[0])

            # Let us know about the series
            super().output_series_information(
                series, "All Strings", key_center, mode, position_str)

            # Build our test note range
            high_note = root + 12    # Up an octave
            test_notes = self.m_u.build_note_list(
                root, high_note, mode, key_center)

            # Play a simon
            self.player.set_notes(test_notes)
            self.player.set_duration(duration)
            self.player.simon_play(
                self.simon_max_size, True)   # Pause between sequences
