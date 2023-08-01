"""Player Class, v2"""

import os
import random
from scamp import Session
from scamp import wait


class Player_new:
    """The thing that plays the notes"""

    def __init__(self):

        # Create and configure the session and part.
        self.session = Session(tempo=120)
        self.part = self.session.new_part("Clarinet")

        # Set initial config values
        self.reset_defaults()

    def reset_defaults(self):
        """Some standard configs"""

        self.standard_pause = 2
        self.longer_pause = 4
        self.standard_volume = 1
        self.note_duration = 1
        self.note_lists = []
        self.trials_size = 10
        self.sequence_size = 1

    def set_trials_size(self, trials_size):
        """Set trials size"""
        self.trials_size = trials_size

    def pre_roll(self):
        """Pause before start of playing"""

        # Wait for the user to press a key to begin
        input("Press ENTER to begin series...")

        # Wait so the first note isn't clipped
        wait(self.standard_pause)

    def random_play_sequence(self, pause=False):
        """Randomly play notes, each trial pulling from a randomly selected note list"""

        self.pre_roll()

        # Build out the lists for playback

        sequence_lists = []  # A list of midi note value lists
        for _ in range(self.trials_size):

            # Start with an empty sequence
            sequence = []

            # Choose the note list to draw from.
            note_list = random.choice(self.note_lists)

            # Populate the sequence
            for _ in range(self.sequence_size):

                # Choose a random note and add to the sequence/list
                note = random.choice(note_list)
                sequence.append(note)

            # Add the sequence/list to the list of lists
            sequence_lists.append(sequence)

        # Play the sequences
        sequence_count = 0
        for sequence in sequence_lists:
            sequence_count += 1
            print(f"Playing sequence {sequence_count} of {self.trials_size}")

            for note in sequence:
                self.part.play_note(note, 1, self.note_duration)

            if pause:
                os.system('pause')

            wait(self.longer_pause)  # Wait before playing the next sequence

        wait(self.standard_pause)
