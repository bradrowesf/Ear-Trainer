"""Player Class"""

import os
import random
from scamp import Session
from scamp import wait
# from scamp import MetricPhaseTarget


class Player:
    """Play the music"""

    def __init__(self, player_tempo=120, duration=1, count=10):
        self.session = Session(tempo=player_tempo)
        self.part = self.session.new_part("Clarinet")
        self.note_set = []      # For notes played one at a time.
        # self.note_lists = []    # For lines.
        self.duration = duration
        self.count = count

        self.standard_pause = 2
        self.standard_volume = 1

    def pre_roll(self):
        """Pause before start of playing"""

        # Wait for the user to press a key to begin
        input("Press ENTER to begin series...")

        # Wait so the first note isn't clipped
        wait(self.standard_pause)

#    def play(self, notes):
#        """Wrap and fork play calls"""

#        def play_note():
#            for note in notes:
#                self.part.play_note(note, self.standard_volume, self.duration)

#        wait(1)

#        self.session.fork(play_note)  # schedule_at=MetricPhaseTarget(0))

    def play_notes(self):
        """Play notes in note set in order"""
        for note in self.note_set:
            self.part.play_note(note, 1, self.duration)

        # self.play(self.note_set)

        wait(self.standard_pause)

    def random_play(self, pause=False):
        """Play notes in note set randomly"""

        self.pre_roll()

        # Build the note list.
        note = -1
        last_note = -1
        note_list = []
        for _ in range(self.count):
            note = random.choice(self.note_set)

            # keep picking notes until it isn't the same one.
            while note == last_note:
                note = random.choice(self.note_set)

            note_list.append(note)
            last_note = note

        # Play the notes
        notecount = 0
        for note in note_list:
            notecount += 1
            print(f"Playing note {notecount} of {self.count}")
            self.part.play_note(note, 1, self.duration)
            # self.play([note])
            if pause:
                os.system('pause')
                wait(.5)

        wait(self.standard_pause)

    def random_play_sequence(self, count, pause=False):
        """Randomly play the from the note_set in groups of count."""

        self.pre_roll()

        # Build out the lists of notes to play.
        sequence_lists = []  # A list of midi note value lists
        for _ in range(self.count):

            # Start with an empty sequence
            sequence = []
            for _ in range(count):

                # Choose a random note and add to the sequence/list
                note = random.choice(self.note_set)
                sequence.append(note)

            # Add the sequence/list to the list of lists
            sequence_lists.append(sequence)

        # Play the sequences
        sequence_count = 0
        for sequence in sequence_lists:
            sequence_count += 1
            print(f"Playing sequence {sequence_count} of {self.count}")

            for note in sequence:
                self.part.play_note(note, 1, self.duration)

            if pause:
                os.system('pause')

            wait(self.standard_pause)  # Wait before playing the next sequence

        wait(self.standard_pause)

    def simon_play(self, count, pause=False):
        """Play random notes, but simon style"""

        self.pre_roll()

        # Build the simon list
        simon_list = []
        for _ in range(count):

            # Choose a random note and add to the list
            note = random.choice(self.note_set)
            simon_list.append(note)

        # Play the notes, simon style
        for series_length in range(count):

            # Simonize it
            for idx in range(series_length + 1):
                note_to_play = simon_list[idx]
                self.part.play_note(
                    note_to_play, self.standard_volume, self.duration)

            if pause:
                os.system('pause')
                wait(1)

        wait(self.standard_pause)

    def set_duration(self, duration):
        """Set note durations for playback."""

        self.duration = duration

    def set_notes(self, notes):
        """Pass in a list of notes to play"""

        self.note_set = notes


def set_count(self, count):
    """Pass in the number of notes to play in any random series"""

    self.count = count
