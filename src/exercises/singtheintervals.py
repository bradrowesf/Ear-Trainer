"""SingTheIntervals exercises"""

import random

from src.exercises.exercise import Exercise
from src.player import Player
from src.exercisepackage import ExercisePackage, ExerciseType, PauseDuration
from src.scoreboard import Scoreboard


class SingTheIntervals(Exercise):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def apply_config(self, config):
        """Apply config and recompute trial_range for full neck span"""

        super().apply_config(config)
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

    def adjust_interval_frequency(self):
        """Use scoreboard to adjust the frequency of the intervals under examination"""

        # Clear the existing list
        self.practice_intervals.clear()

        score_frequencies = {}
        score_averages = {}
        for interval in self.candidate_intervals:
            prefix = self.sb.get_test_prefix(self.name, interval)
            average = self.sb.get_adjusted_element_score(prefix)
            score_averages[interval] = average
            score_frequencies[interval] = average ** 2  # Not linear

        scores_sum = sum(score_frequencies.values())
        for interval in self.candidate_intervals:

            # Get the frequency, but always at least 1
            interval_freq = round(100*score_frequencies[interval]/scores_sum)
            interval_freq = interval_freq + 1

            print(
                f"{interval:<10} : {score_averages[interval]:>6.3f} : {interval_freq}%")
            for _ in range(0, interval_freq):
                self.practice_intervals.append(interval)

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

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions
        name = "Singing the Easy Intervals"
        mixable = False
        exercise_duration = 600     # 5 minutes, in seconds
        trials_sets_count = 50
        trials_count = 6
        # Noted here for documentation purposes, but not functional in this exercise.
        # (It's hard coded elsewhere to be 2 notes: the start note and the note 1 interval away.)
        trial_size = 2
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.INTERVAL,
            PauseDuration.MEDIUM,
            PauseDuration.NONE,
            PauseDuration.MEDIUM,           # trial repeat & duration
            True,                           # mid trial prompt enabled
            True                            # keep score
        )

        # Pass these to the parent class
        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        # trial_range is the full neck span
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

        self.candidate_intervals = ['-M6', '-m7', '-m6']
        self.practice_intervals = []
        self.practice_interval_current = ''


class SingTheIntervalsMedium(SingTheIntervals):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions
        name = "Singing the Medium Intervals"
        mixable = False
        exercise_duration = 900     # seconds
        trials_sets_count = 50
        trials_count = 3
        # Noted here for documentation purposes, but not functional in this exercise.
        # (It's hard coded elsewhere to be 2 notes: the start note and the note 1 interval away.)
        trial_size = 2
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.INTERVAL,
            PauseDuration.MEDIUM,
            PauseDuration.NONE,
            PauseDuration.MEDIUM,           # trial repeat & duration
            True,                          # mid trial prompt enabled
            True                            # keep score
        )

        # Pass these to the parent class
        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        # trial_range is the full neck span
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

        self.candidate_intervals = [
            'm2', '-m2',
            'M2', '-M2',
            'm3', '-m3',
            'M3', '-M3',
            'P4', '-P4',
            'Aug4', '-Aug4',
            'P5', '-P5',
            'm6', '-m6',
            'M6', '-M6',
            'm7', '-m7',
            'M7', '-M7'
        ]
        self.practice_intervals = []
        self.practice_interval_current = ''


class SingTheIntervalsHard(SingTheIntervals):
    """Each set is practice for singling a specific interval above/below a random base note"""

    def __init__(self, player: Player, scoreboard: Scoreboard) -> None:

        # Definitions
        name = "Singing the Hard Intervals"
        mixable = False
        exercise_duration = 600     # 10 minutes, in seconds
        trials_sets_count = 20
        trials_count = 1
        # Noted here for documentation purposes, but not functional in this exercise.
        # (It's hard coded elsewhere to be 2 notes: the start note and the note 1 interval away.)
        trial_size = 2
        max_interval = 12   # 1 octave
        trial_range = 46    # Full Neck

        key_centers = ['C']
        intervalics = ['Chromatic']
        trial_varied_intervalics = False
        e_p = ExercisePackage(
            ExerciseType.INTERVAL,
            PauseDuration.MEDIUM,
            PauseDuration.NONE,
            PauseDuration.MEDIUM,           # trial repeat & duration
            True,                           # mid trial prompt enabled
            True                            # keep score
        )

        # Pass these to the parent class
        super().__init__(player, scoreboard, name, e_p, mixable, exercise_duration,
                         trials_sets_count, trials_count, trial_size,
                         max_interval, trial_range, key_centers,
                         intervalics, trial_varied_intervalics)

        # trial_range is the full neck span
        self.trial_range = self.high_estring_high_note - self.low_estring_low_note

        self.candidate_intervals = [
            'm2', '-m2',
            'M2', '-M2',
            'm3', '-m3',
            'M3', '-M3',
            'P4', '-P4',
            'Aug4', '-Aug4',
            'P5', '-P5',
            'm6', '-m6',
            'M6', '-M6',
            'm7', '-m7',
            'M7', '-M7'
        ]
        self.practice_intervals = []
        self.practice_interval_current = ''
