"""All of the exercises, version 2"""

from abc import ABC, abstractmethod
import itertools
import random

from midiutilities import MidiUtil
from guitarutilities import GuitarUtil
from player import Player


class Exercise(ABC):
    """Parent Class for Exercises"""

    def __init__(self, name, trials_sets_count, trials_count,
                 trial_size, max_interval, trial_range, key_centers,
                 intervalics, trial_varied_intervalics) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.player = Player()

        # The configuration data
        self.name = name

        # Values for the size of each trial, trials in a trial set, and trial sets.
        # Essentially this defines the length of the exercise
        # Number of different sets/definitions
        self.trials_sets_count = trials_sets_count
        # Number of trials under single definition
        self.trials_count = trials_count
        self.trial_size = trial_size                # Number of notes per trial

        # Need something here to determine what the legal notes for the exercise will be.
        # Trial set range, key/mode, chord tones, etc.
        self.key_centers = key_centers
        self.intervalics = intervalics
        self.trial_varied_intervalics = trial_varied_intervalics

        # Need something here to determine note limitations within a single trial.
        self.max_interval = max_interval
        self.trial_range = trial_range

        # What are the midi note values for our low estring
        #  - turns out this is useful in most exercises
        self.low_estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # low-e string open
        self.low_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 22))   # low-e string 22nd fret
        self.high_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(1, 22))   # high-e string 22nd fret

    def __str__(self):
        return self.name

    def configure_player(self, post_trial_pause, mid_trial_pause, trial_repeat, press_key_pause):
        """Configure the player based on child exercise requirements"""

        self.player.set_post_trial_pause(post_trial_pause)
        self.player.set_mid_trial_pause(mid_trial_pause)
        self.player.set_trial_repeat(trial_repeat)
        self.player.set_press_key_pause(press_key_pause)

    @abstractmethod
    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range -- abstract method"""

    @abstractmethod
    def build_trial_definition(self, low_note, key_center, intervalic):
        """Define Trial Definition -- abstract method"""

    def build_trial_set(self, legal_notes_list):
        """Build out the individual trials for the set"""

        # Our return list
        trial_set = []

        # Our cycling iterator for legal notes.
        legal_notes_cycle = itertools.cycle(legal_notes_list)
        legal_notes = legal_notes_cycle[0]

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

            # Save the trial.
            trial_set.append(trial)

            # Change the legal notes for the next trial
            legal_notes = next(legal_notes_cycle)

        return trial_set

    def do_exercise(self):
        """Run the  exercise"""

        # Let us know what the exercise is.
        self.output_exercise_title()

        # Setup our player lists
        trial_sets = []
        trial_definitions = []

        # Iterate across the trial_sets
        for trial_set in range(0, self.trials_sets_count):

            # Get the key_center and intervalic list.
            #   - Needed to identify the range when positionally determined.
            key_center, intervalic_list = self.get_key_intervalic()

            # Get the trial set range
            low_note, high_note = self.get_trial_set_range(
                key_center, intervalic_list)

            # Now the legal notes in that trial set range.
            legal_notes = self.m_u.build_note_list(
                low_note, high_note, intervalic_list, key_center)

            # Build the trial set and definition, based on the above.
            trial_set = self.build_trial_set(legal_notes)
            trial_definition = self.build_trial_definition(
                low_note, key_center, intervalic_list)

            # Add it to the player trial sets and definitions
            trial_sets.append(trial_set)
            trial_definitions.append(trial_definition)

        # Let's Play
        self.player.set_trial_lists(trial_sets, trial_definitions)
        self.player.play()

    def do_singleton(self):
        """Do a single trial set of the exercise"""

        # Reset to do a single trial (and save the current value for later)
        old_trials_sets_count = self.trials_sets_count
        self.trials_sets_count = 1

        # Run the singleton
        self.do_exercise()

        # Reset
        self.trials_sets_count = old_trials_sets_count

    def output_exercise_title(self):
        """Visual for exercise"""

        print('---------------------------------------------------------------------')
        print(f"Exercise: {self.name}")
        print('---------------------------------------------------------------------')

    def get_key_intervalic(self):
        """Select the key center and intervalics for the legal note determinations"""

        # Pick the key center randomly.
        key_center = random.choice(self.key_centers)

        # Build the intervalic list as appropriate
        intervalic_list = []
        if self.trial_varied_intervalics:
            intervalic_list = self.intervalics  # We need them all to vary between trials
        else:
            intervalic_list.append(random.choice(self.intervalics))  # pick one

        return key_center, intervalic_list


class OneString(Exercise):
    """Play single random notes on a single string"""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "One String Exercise"
        trials_sets_count = 10
        trials_count = 50
        trial_size = 1
        max_interval = 22  # The whole string
        trial_range = 22   # The whole string
        key_centers = ["C", "F", "G"]
        intervalics = ["Ionian", "Major Pentatonic", "Minor Pentatonic"]
        trial_varied_intervalics = False

        # Pass these to the parent class
        super().__init__(name, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        self.configure_player(3, 2, False, False)

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


class OneOctave(Exercise):
    """Play random notes, within a single octave"""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "Single Octave Exercise"
        trials_sets_count = 20
        trials_count = 50
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ["C"]
        intervalics = ["Ionian"]
        trial_varied_intervalics = False

        super().__init__(name, trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        self.configure_player(1, 1, False, False)

    def get_trial_set_range(self, key_center, intervalic):
        """Chose a specific octave for testing"""

        # Find all the legal notes for the lowest note in our range
        #  - lowest note in the range can't be be within an octave of the highest note
        legal_low_notes = self.m_u.build_note_list(
            self.low_estring_low_note, self.high_estring_high_note - 12, intervalic, key_center)

        # Pick one of them
        low_note = random.choice(legal_low_notes)
        high_note = low_note + 12   # one octave higher

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic):
        """Build our definition string for the chosen trial set"""

        # What are all the possible places this low note could be.
        low_note_true_name = self.m_u[low_note]
        fret_string_list = self.g_u.get_fret_string_from_name(
            low_note_true_name, 0, 19, 3, 6)

        # Pick one of them
        fret_string = random.choice(fret_string_list)
        position = fret_string[0]   # This is the position of the exercise.

        # Build the string
        definition = "Position: " + str(position) + "\n"
        definition += "Low note: " + low_note_true_name + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic

        return definition


class OnePositionBase(Exercise):
    """A base class for single position exercises"""

    def get_trial_set_range(self, key_center, intervalic):
        """Determine the position we'll be playing in and the range of pitches available"""

        # Find the legal notes on the low estring for the key_center and intervalic
        #  - midi note values, natch
        #  - lowest note in the range cannot be above the 19th fret
        legal_low_notes = self.m_u.build_note_list(
            self.low_estring_low_note, self.low_estring_high_note - 3, intervalic, key_center)

        # Pick one of them
        low_note = random.choice(legal_low_notes)
        high_note = low_note + 27  # up 2 octaves and a minor 3rd

        return low_note, high_note

    def find_position(self, low_note):
        """Given """


class OnePosition(OnePositionBase):
    """Play random notes, but in a specific position"""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "Single Position Exercise"
        trials_sets_count = 10
        trials_count = 10
        trial_size = 3
        max_interval = 12  # 1 octave
        trial_range = 19   # 1 octave + perfect 5th

        key_centers = ["C", "F", "G"]
        intervalics = ["Ionian", "Major Pentatonic", "Minor Pentatonic"]
        trial_varied_intervalics = False

        super().__init__(name, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        self.configure_player(2, 1, True, True)

    # def get_trial_set_range(self, key_center, intervalic):
    #     """Determine the position we'll be playing in and the range of pitches available"""

    #     # Find the legal notes on the low estring for the key_center and intervalic
    #     #  - midi note values, natch
    #     #  - lowest note in the range cannot be above the 19th fret
    #     legal_low_notes = self.m_u.build_note_list(
    #         self.low_estring_low_note, self.low_estring_high_note - 3, intervalic, key_center)

    #     # Pick one of them
    #     low_note = random.choice(legal_low_notes)
    #     high_note = low_note + 27  # up 2 octaves and a minor 3rd

    #     return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        position = self.g_u.get_fret_from_full_note_name(low_note_true_name, 6)
        # fret_string_list = self.g_u.get_fret_string_from_name(
        #     low_note_true_name, 0, 22, 6, 6)
        # fret_string = fret_string_list[0]  # Should only be 1
        # position = fret_string[0]  # This should be the position.

        # Build the string
        definition = "Position: " + str(position) + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Intervalic: " + intervalic

        return definition


class ChordTones(OnePositionBase):
    """Play random notes, with each trial choosing from chord tones"""

    def __init__(self) -> None:

        # Definitions (from parent)
        name = "Chord Tones Exercise"
        trials_sets_count = 10
        trials_count = 10
        trial_size = 3
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ["C"]
        intervalics = ["I7", "IV7", "V7"]
        trial_varied_intervalics = True

        super().__init__(name, trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        self.configure_player(2, 1, True, True)

    def build_trial_definition(self, low_note, key_center, intervalic):
        """Build the definition string for the trial set"""

        # What string are we on? Well, what is the low note name?
        low_note_true_name = self.m_u[low_note]
        position = self.g_u.get_fret_from_full_note_name(low_note_true_name, 6)

        # Build the string
        definition = "Position: " + str(position) + "\n"
        definition += "Key: " + key_center + "\n"
        definition += "Progression: " + intervalic

        return definition
