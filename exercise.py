"""All of the exercises, version 2"""
import random

from midiutilities import MidiUtil
from guitarutilities import GuitarUtil
from player import Player


class Exercise:
    """Parent Class for Exercises"""

    def __init__(self, name, trial_sets_count, trials_count,
                 trial_size, key_centers, intervalics) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.player = Player()

        # The configuration data
        self.name = name

        # Values for the size of each trial, trials in a trial set, and trial sets.
        # Essentially this defines the length of the exercise
        self.trial_sets_count = trial_sets_count
        self.trials_count = trials_count
        self.trial_size = trial_size

        # Need something here to determine what the legal notes for the exercise will be.
        # Trial set range, key/mode, chord tones, etc.
        self.key_centers = key_centers
        self.intervalics = intervalics

        # Need something here to determine note limitations within a single trial.
        # Interval Limit, Trial Range, etc.

        # What are the midi note values for our low estring
        #  - turns out this is useful in most exercises
        self.estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # 6 string open
        self.estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 12))  # 6 string 12th fret

    def __str__(self):
        return self.name

    def do_exercise(self):
        """In child classes, do the exercise in question"""
        assert True, f"{self.name} -- Do Exercise not defined."

    def output_exercise_title(self):
        """Visual for exercise"""

        print('---------------------------------------------------------------------')
        print(f"Exercise: {self.name}")
        print('---------------------------------------------------------------------')

 #   def output_series_information(self, series, strings, key_center, grouping, position):
 #       """Visual for series"""

        # Need something here that defines what is happening in a single trial set.
 #       print("*****")
 #       print("*****")

    def get_key_intervalic(self):
        """Select the key center and intervalics for the legal note determinations"""

        # Basic version, just pick randomly and independently.
        key_center = random.choice(self.key_centers)
        intervalic = random.choice(self.intervalics)

        return key_center, intervalic


class OneString(Exercise):
    """Play single random notes on a single string"""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "One String Exercise"
        trials_sets_count = 10
        trials_count = 50
        trial_size = 1
        key_centers = ["C"]
        intervalics = ["Ionian"]

        super().__init__(name, trials_sets_count, trials_count,
                         trial_size, key_centers, intervalics)

    def get_trial_set_range(self):
        """Define the Trial Set Range"""

        # Pick the string for the trial set.
        #  - String numbering is backwards (low E string is 0, high e is 5)
        guitar_string = random.randrange(0, 6)

        # Determine the Trial Set Range.
        #  - the midi note values for the high and low notes on the chosen string.
        b_e_string_corrector = 0
        if guitar_string > 3:   # did we pick the b or e string?
            b_e_string_corrector = 1
        low_note = self.estring_low_note + \
            (guitar_string * 5) - b_e_string_corrector
        high_note = self.estring_high_note + \
            (guitar_string * 5) - b_e_string_corrector

        return low_note, high_note

    def build_trial_set(self, legal_notes):
        """Build out the individual trials for the set"""

        # Our return list
        trial_set = []

        # Iterate through all the trials we are building
        for _ in range(self.trials_count):

            # Temp list for the trial
            trial = []

            # Some placeholders to help us avoid note doubling within a trial
            note = -1
            last_note = -1

            # Iterate through all the notes in a single trial
            for _ in range(self.trial_size):

                # Keep picking as long as the note matches the last one
                while note == last_note:
                    note = random.choice(legal_notes)

                # Add it to the trial and continue.
                trial.append(note)
                last_note = note

            # Trial is complete so add it to the end.
            trial_set.append(trial)

        return trial_set

    def build_trial_definition(self, low_note, key_center, intervalic):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        fret_string_list = self.g_u.get_fret_string_from_name(
            low_note_true_name, 0, 1)
        fret_string = fret_string_list[0]  # Should only be 1
        string = fret_string[1]  # This should be the name.

        # Build the string
        definition = "String: " + string + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic

        return definition

    def do_exercise(self):
        """Run the one string random note exercise"""

        # Let us know what the exercise is.
        super().output_exercise_title()

        # Setup our player lists
        trial_sets = []
        trial_definitions = []

        # Iterate across the trial_sets
        for trial_set in range(0, self.trial_sets_count):

            # Get the trial set range.
            low_note, high_note = self.get_trial_set_range()

            # Determine the legal notes
            key_center, intervalic = self.get_key_intervalic()
            legal_notes = self.m_u.build_note_list(
                low_note, high_note, intervalic, key_center)

            # Build the trial set and definition, based on the above.
            trial_set = self.build_trial_set(legal_notes)
            trial_definition = self.build_trial_definition(
                low_note, key_center, intervalic)

            # Add it to the player trial sets and definitions
            trial_sets.append(trial_set)
            trial_definitions.append(trial_definition)

        # Let's Play
        self.player.set_trial_lists(trial_sets, trial_definitions)
        self.player.play()


class OnePosition(Exercise):
    """Play single random notes, but in a specific position."""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "Single Position Exercise"
        trials_sets_count = 10
        trials_count = 50
        trial_size = 3
        key_centers = ["C"]
        intervalics = ["Ionian"]

        super().__init__(name, trials_sets_count, trials_count,
                         trial_size, key_centers, intervalics)

        # Some child definitions
        self.max_interval = 12  # 1 octave
        self.trial_range = 19   # 1 octave + perfect 5th

    def get_trial_set_range(self, key_center, intervalic):
        """Determine the position we'll be playing in and the range of pitches available"""

        # Find the legal notes on the low estring for the key_center and intervalic
        #  - midi note values, natch
        legal_low_notes = self.m_u.build_note_list(
            self.estring_low_note, self.estring_high_note, intervalic, key_center)

        # Pick one of them
        low_note = random.choice(legal_low_notes)
        high_note = low_note + 27  # up 2 octaves and a minor 3rd

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        fret_string_list = self.g_u.get_fret_string_from_name(
            low_note_true_name, 0, 22, 6, 6)
        fret_string = fret_string_list[0]  # Should only be 1
        position = fret_string[0]  # This should be the position.

        # Build the string
        definition = "Position: " + str(position) + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic

        return definition

    def build_trial_set(self, legal_notes):
        """Build out the individual trials for the set"""

        # Our return list
        trial_set = []

        # Iterate through all the trials we are building
        for _ in range(self.trials_count):

            # Temp list for the trial
            trial = []

            # Some placeholders to help us test note selection legality
            note = -1
            last_note = -1
            high_note = -1
            low_note = 1000
            first_note_in_set = True

            for _ in range(self.trial_size):

                legit_note = False
                while not legit_note:

                    # Pick a note
                    note = random.choice(legal_notes)

                    # Was it legit?
                    if first_note_in_set:
                        first_note_in_set = False
                        legit_note = True
                    elif abs(note-last_note) > self.max_interval:
                        # The interval between notes is too large
                        continue
                    elif abs(note-high_note) > self.trial_range:
                        # Too far below highest note
                        continue
                    elif abs(note-low_note) > self.trial_range:
                        # Too far below lowest note
                        continue
                    else:
                        legit_note = True

                # Add it to the trial
                trial.append(note)

                # Remember this note
                last_note = note

                # Is this the highest note in the set?
                if note > high_note:
                    high_note = note

                # Is this the lowest note in the set?
                if note < low_note:
                    low_note = note

            trial_set.append(trial)

        return trial_set

    def do_exercise(self):
        """Run the one position exercise"""

        # Let us know what the exercise is.
        super().output_exercise_title()

        # Setup our player lists
        trial_sets = []
        trial_definitions = []

        # Iterate across the trial_sets
        for trial_set in range(0, self.trial_sets_count):

            # Get the key_center and intervalic.
            #   - Needed to identify the range when positionally determined.
            key_center, intervalic = self.get_key_intervalic()

            # Get the trial set range
            low_note, high_note = self.get_trial_set_range(
                key_center, intervalic)

            # Now the legal notes in that trial set range.
            legal_notes = self.m_u.build_note_list(
                low_note, high_note, intervalic, key_center)

            # Build the trial set and definition, based on the above.
            trial_set = self.build_trial_set(legal_notes)
            trial_definition = self.build_trial_definition(
                low_note, key_center, intervalic)

            # Add it to the player trial sets and definitions
            trial_sets.append(trial_set)
            trial_definitions.append(trial_definition)

        # Let's Play
        self.player.set_trial_lists(trial_sets, trial_definitions)
        self.player.play()
