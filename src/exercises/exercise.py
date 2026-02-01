"""Exercise base class (ABC)"""

from abc import ABC, abstractmethod
import itertools
import random

from src.midiutilities import MidiUtil
from src.guitarutilities import GuitarUtil
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard
from src.keypresshelper import any_key_press


class Exercise(ABC):
    """Parent Class for Exercises"""

    def __init__(self, player: Player, scoreboard: Scoreboard, name, e_p: ExercisePackage,
                 mixable: bool, exercise_duration, trials_sets_count, trials_count, trial_size,
                 max_interval, trial_range, key_centers, intervalics,
                 trial_varied_intervalics) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.e_p = e_p
        self.player = player
        self.sb = scoreboard

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

        # Some settings for interval singing exercises
        self.practice_intervals = []
        self.candidate_intervals = []
        self.practice_interval_current = ''

        # What are the midi note values for our low estring
        #  - turns out this is useful in most exercises
        self.low_estring_low_note = self.m_u.index(
            self.g_u.get_full_note_name(6, 0))    # low-e string open
        self.low_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, self.g_u.max_frets))
        self.high_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(1, self.g_u.max_frets))

    def __str__(self):
        return self.name

    def get_remember_note_of_previous_trial_set(self):
        """Has the last note of the previous set been saved?"""

        return self.remember_note_of_previous_trial_set

    @abstractmethod
    def get_trial_set_range(self, key_center, intervalic):
        """Define the Trial Set Range -- abstract method"""

    @abstractmethod
    def build_trial_definition(self, low_note, key_center, intervalic_list):
        """Define Trial Definition -- abstract method"""

    def adjust_interval_frequency(self):
        """Nothing for most exercises"""

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

        # Let us know what the exercise is.
        self.output_exercise_title()

        # Adjust frequency of intervals (if necessary for specific exercise)
        self.adjust_interval_frequency()

        # Iterate across the trial_sets
        self.e_p.reset()
        self.e_p.set_test_name(self.name)
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

            # Add it to the player trial sets, definitions, and label
            self.e_p.append_trial_set(
                trial_set, trial_definition, self.practice_interval_current)

        # Let's Play
        self.player.play(self.e_p, self.sb, self.exercise_duration)

        # If we're keeping score, let's save and print it out.
        if self.e_p.get_scoring_enabled():
            self.sb.save()
            self.sb.output_scores(self.name, self.candidate_intervals)
            any_key_press("Press Any Key")

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

    def _recompute_fret_limits(self):
        """Recompute derived MIDI note limits from current max_frets"""

        self.low_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(6, self.g_u.max_frets))
        self.high_estring_high_note = self.m_u.index(
            self.g_u.get_full_note_name(1, self.g_u.max_frets))

    def apply_config(self, config):
        """Apply configuration overrides from a Config object"""

        class_name = type(self).__name__

        duration = config.get_exercise_duration(class_name)
        if duration is not None:
            self.exercise_duration = duration

        key_centers = config.get_key_centers(class_name)
        if key_centers is not None:
            self.key_centers = key_centers

        intervalics = config.get_intervalics(class_name)
        if intervalics is not None:
            self.intervalics = intervalics

        guitar_type = config.get_guitar_type()
        if guitar_type != self.g_u.max_frets:
            self.g_u.max_frets = guitar_type
            self._recompute_fret_limits()

    def is_mixable(self):
        """Return mix exercise eligibility"""

        return self.mixable
