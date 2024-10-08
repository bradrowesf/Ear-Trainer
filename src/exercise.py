"""All of the exercises, version 2"""

from abc import ABC, abstractmethod
import itertools
import random

from src.midiutilities import MidiUtil
from src.guitarutilities import GuitarUtil
from src.player import Player


class PlayerConfig():
    """Data class to hold player configuration settings"""

    def __init__(self, post_trial_pause, trial_repeat_pause, mid_trial_pause, enable_trial_repeat,
                 enable_mid_trial_pause, enable_interval_singing) -> None:

        # Some important details w/rt these settings.

        # post_trial_pause
        #   - Time between end of last trial and beginning of new trial.
        #   - When pause_key_press is TRUE, the impact is lessened.
        # trial_repeat_pause
        #   - The duration between the trial and its validation repetition.
        #   - This only matters when enable_trial_repeat is TRUE.
        #       - IOW if enable_trial_repeat is FALSE, this is ignored.
        # enable_mid_trial_pause (boolean)
        #   - This means that after the trial is played, nothing happens until user action.
        #   - Usually a key press or a set of options.
        #   - This somewhat overrides everything.
        # enable_trial_repeat (boolean)
        #   - Controls whether a validation repeat occurs.
        #       - trial_repeat_pause controls the delay between the initial and validation playback.

        self.post_trial_pause = post_trial_pause
        self.trial_repeat_pause = trial_repeat_pause
        self.mid_trial_pause = mid_trial_pause
        self.enable_trial_repeat = enable_trial_repeat
        self.enable_mid_trial_pause = enable_mid_trial_pause
        self.enable_interval_singing = enable_interval_singing


class Exercise(ABC):
    """Parent Class for Exercises"""

    def __init__(self, player: Player, name, mixable: bool, exercise_duration, trials_sets_count,
                 trials_count, trial_size, max_interval, trial_range, key_centers,
                 intervalics, trial_varied_intervalics, player_config: PlayerConfig) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.player = player

        # The configuration data
        self.name = name

        # Should this exercise be included when we do the exercise mixer.
        self.mixable = mixable

        # Values for
        #   - Exercise duration (in seconds)
        #   - size of each trial, trials in a trial set, and trial sets.

        self.exercise_duration = exercise_duration

        # Maz number of different sets/definitions
        self.trials_sets_count = trials_sets_count
        # Number of trials under single definition
        self.trials_count = trials_count
        self.trial_size = trial_size                # Number of notes per trial

        # Need something here to determine what the legal notes for the exercise will be.
        # Trial set range, key/mode, chord tones, etc.
        self.key_centers = key_centers
        self.intervalics = intervalics
        self.trial_varied_intervalics = trial_varied_intervalics

        # A place for the last note of the previous trial.  Set to -1 in most cases.
        self.remember_note_of_previous_trial_set = False

        # Need something here to determine note limitations within a single trial.
        self.max_interval = max_interval
        self.trial_range = trial_range

        # Player config
        self.player_config = player_config

        # Some settings for interval singing exercises
        self.practice_intervals = ['m3', '-m3']
        self.practice_interval_current = ''

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

    def get_remember_note_of_previous_trial_set(self):
        """Has the last note of the previous set been saved?"""

        return self.remember_note_of_previous_trial_set

    def configure_player(self):
        """Configure the player based on child exercise requirements"""

        self.player.set_post_trial_pause(self.player_config.post_trial_pause)
        self.player.set_trial_repeat_pause(
            self.player_config.trial_repeat_pause)
        self.player.set_mid_trial_pause(self.player_config.mid_trial_pause)
        self.player.set_enable_trial_repeat(
            self.player_config.enable_trial_repeat)
        self.player.set_enable_mid_trial_pause(
            self.player_config.enable_mid_trial_pause)
        self.player.set_enable_interval_singing(
            self.player_config.enable_interval_singing)

    @abstractmethod
    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range -- abstract method"""

    @abstractmethod
    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Define Trial Definition -- abstract method"""

    def build_trial_set(self, legal_notes_list):
        """Build out the individual trials for the set"""

        # Our return list
        trial_set = []

        # Our cycling iterator for legal notes.
        legal_notes_cycle = itertools.cycle(legal_notes_list)
        legal_notes = next(legal_notes_cycle)

        # Someplace to hold the note from a previous trial, if we're doing that.
        last_note_previous_trial = -1
        first_trial = True

        # Iterate through all the trials we are building
        for _ in range(self.trials_count):

            # Temp list for the trial
            trial = []

            # Some placeholders to help us test note selection legality
            note = -1
            last_note = last_note_previous_trial
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
                        if self.get_remember_note_of_previous_trial_set():
                            if not (first_trial) and abs(note-last_note) > self.max_interval:
                                # The interval between this note and
                                # the last note of the previous trial is too large
                                continue
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

            # No longer the first trial
            first_trial = False

            # Change the legal notes for the next trial
            legal_notes = next(legal_notes_cycle)

            # Should we remember the last note of this trial_set for the next one.
            if self.get_remember_note_of_previous_trial_set():
                last_note_previous_trial = last_note

        return trial_set

    def do_exercise(self):
        """Run the  exercise"""

        # Configure the player
        self.configure_player()

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
            legal_notes_lists = self.m_u.build_note_list(
                low_note, high_note, intervalic_list, key_center)

            # Build the trial set and definition, based on the above.
            trial_set = self.build_trial_set(legal_notes_lists)
            trial_definition = self.build_trial_definition(
                low_note, key_center, intervalic_list)

            # Add it to the player trial sets and definitions
            trial_sets.append(trial_set)
            trial_definitions.append(trial_definition)

        # Let's Play
        self.player.set_trial_lists(trial_sets, trial_definitions)
        self.player.play(self.exercise_duration)

    def do_singleton(self, duration):
        """Do a single trial set of the exercise"""

        # Save old values
        old_exercise_duration = self.exercise_duration
        old_trials_sets_count = self.trials_sets_count

        # Set singleton values
        self.exercise_duration = duration
        self.trials_sets_count = 1

        # Run the singleton
        self.do_exercise()

        # Reset
        self.exercise_duration = old_exercise_duration
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

    def build_intervalic_string(self, intervalic_list):
        """Utility method to build a string from the intervalic list"""

        intervalic_string = ""
        for intervalic in intervalic_list:
            if len(intervalic_string) > 0:
                intervalic_string += ", "  # seperate by commas
            intervalic_string += intervalic

        return intervalic_string

    def is_mixable(self):
        """Return mix exercise eligibility"""

        return self.mixable


class OneString(Exercise):
    """Play single random notes on a single string"""

    def __init__(self, player: Player) -> None:

        # Definitions (from parent)
        name = "One String Exercise"
        mixable = True
        exercise_duration = 300     # 5 Minutes
        trials_sets_count = 10
        trials_count = 50
        trial_size = 1
        max_interval = 22  # The whole string
        trial_range = 22   # The whole string
        key_centers = ['C', 'F', 'G', 'A', 'E', 'B']
        intervalics = ['Ionian', "Major Pentatonic", "Minor Pentatonic", 'Major', 'Minor',
                       'Major Seventh', 'Dominant Seventh', 'Minor Seventh', 'Dorian', 'Lydian',
                       'Mixolydian', 'Super Locrian']
        trial_varied_intervalics = False
        player_config = PlayerConfig(2, 2, 2, False, False, False)

        # Pass these to the parent class
        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)

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


class OneOctaveBase(Exercise):
    """Base class for one octave exercises."""

    def get_trial_set_range(self, key_center, intervalic):
        """Chose a specific octave for testing"""

        # Find all the legal notes for the lowest note in our range
        #  - lowest note in the range can't be be within an octave of the highest note
        legal_low_notes = self.m_u.build_note_list(
            self.low_estring_low_note, self.high_estring_high_note - 12, intervalic, key_center)

        # Pick one of them
        #   Legal_low_notes is now a list of lists, but there should only be
        #   one list in this exercise.
        low_note = random.choice(legal_low_notes[0])
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

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(1, 1, 2, False, False, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class OneOctaveMedium(OneOctaveBase):
    """Play random notes, within a single octave"""

    def __init__(self, player: Player) -> None:

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
        intervalics = ['Ionian', 'Aeolian', 'Dorian', 'Mixolydian']
        trial_varied_intervalics = False
        player_config = PlayerConfig(2, 1, 2, False, False, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class OneOctaveHard(OneOctaveBase):
    """Play random notes, within a single octave"""

    def __init__(self, player: Player) -> None:

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
        intervalics = ['Super Locrian', 'Lydian Dominant']
        trial_varied_intervalics = False
        player_config = PlayerConfig(4, 1, 2, False, False, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


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

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(2, 4, 2, True, False, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class OnePositionMedium(OnePositionEMH):
    """Medium single position exercise"""

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(2, 2, 2, True, True, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class OnePositionHard(OnePositionEMH):
    """Hard single position exercise"""

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(2, 2, 2, True, True, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class ChordTones(OnePositionBase):
    """Play random notes, with each trial choosing from chord tones"""

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(2, 2, 2, True, True, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)

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
        low_note = self.low_estring_low_note
        high_note = self.m_u.index(self.g_u.get_full_note_name(1, 12))

        return low_note, high_note


class AudiationEasy(AudiationBase):
    """Chromatics only."""

    def __init__(self, player: Player) -> None:

        # Definitions (from parent)
        name = "Chromatic Audiation Exercise (Easy)"
        mixable = False
        exercise_duration = 300     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 10
        trial_size = 4
        max_interval = 12   # 1 octave
        trial_range = 12    # 1 octave

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = True
        player_config = PlayerConfig(2, 2, 2, False, True, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class AudiationHard(AudiationBase):
    """Chromatics only."""

    def __init__(self, player: Player) -> None:

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
        player_config = PlayerConfig(2, 2, 2, False, True, False)

        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)


class JustTheIntervals(Exercise):
    """Play single notes, one after the other, an octave or less apart"""

    def __init__(self, player: Player) -> None:

        # Definitions
        name = "Full Neck Sub-Octave Intervals"
        mixable = False
        exercise_duration = 300     # 10 minutes, in seconds
        trials_sets_count = 1
        trials_count = 100
        trial_size = 1
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        player_config = PlayerConfig(4, 2, 2, False, False, False)

        # Pass these to the parent class
        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)

        # Remember across trial_sets
        self.remember_note_of_previous_trial_set = True

    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range"""

        # All the notes
        low_note = self.low_estring_low_note
        high_note = self.high_estring_high_note

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        return "All the notes"


class SingTheIntervals(Exercise):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range"""

        # Notes from the first 12 frets.
        low_note = self.low_estring_low_note
        high_note = self.m_u.index(self.g_u.get_full_note_name(1, 12))

        return low_note, high_note

    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Build the definition string for the trial set"""

        definition = "Sing a " + self.practice_interval_current

        return definition

    def build_trial_set(self, legal_notes_list):

        # Our return list
        trial_set = []

        # Our list of legal starting notes
        legal_notes = []

        # Choose the interval
        current_interval = self.practice_interval_current
        while self.practice_interval_current == current_interval:  # no dupes
            current_interval = random.choice(self.practice_intervals)

        self.practice_interval_current = current_interval
        interval = self.m_u.get_semitone_count_for_interval(current_interval)

        # Purge the list of available starting notes so that we stay on the fretboard
        if interval > 0:
            top_note = max(legal_notes_list[0]) - interval
            legal_notes = [k for k in legal_notes_list[0] if k <= top_note]
        else:
            bottom_note = min(legal_notes_list[0]) - interval
            legal_notes = [k for k in legal_notes_list[0] if k >= bottom_note]

        # Remember the last note so we don't dupe.
        last_note = -1

        # Iterate through the trials we are building
        for _ in range(self.trials_count):

            # Temp list for the trial
            trial = []

            # Pick the note and the interval
            note = last_note
            # no dupes/octaves
            while note == last_note or abs(note-last_note) % 12 == 0:
                note = random.choice(legal_notes)

            last_note = note    # Never forget
            note2 = note + interval
            trial.append(note)

            # Add the interval we are singing (hard coded for now).
            trial.append(note2)

            # Trial is finished. Append to the set.
            trial_set.append(trial)

        return trial_set


class SingTheIntervalsEasy(SingTheIntervals):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def __init__(self, player: Player) -> None:

        # Definitions
        name = "Singing the Easy Intervals"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 5
        # Noted here for documentation purposes, but not functional in this exercise.
        trial_size = 2
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        player_config = PlayerConfig(2, 1, 4, False, False, True)

        # Pass these to the parent class
        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)

        self.practice_intervals = ['m2', '-m2',
                                   'M2', '-M2',
                                   'M3', '-M3',
                                   'm3', '-m3',
                                   'P4', '-P4',
                                   'P5', '-P5'
                                   ]
        self.practice_interval_current = ''


class SingTheIntervalsHard(SingTheIntervals):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def __init__(self, player: Player) -> None:

        # Definitions
        name = "Singing the Hard Intervals"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 10
        trials_count = 5
        # Noted here for documentation purposes, but not functional in this exercise.
        trial_size = 2
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        player_config = PlayerConfig(2, 1, 1, False, True, True)

        # Pass these to the parent class
        super().__init__(player, name, mixable, exercise_duration, trials_sets_count, trials_count,
                         trial_size, max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics, player_config)

        self.practice_intervals = [
            'M6', '-M6',
            'm6', '-m6',
            'm7', '-m7']
        self.practice_interval_current = ''
