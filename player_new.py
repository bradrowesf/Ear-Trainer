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
        # Some standard configs
        self.standard_pause = 2
        self.standard_volume = 1

    def pre_roll(self):
        """Pause before start of playing"""

        # Wait for the user to press a key to begin
        input("Press ENTER to begin series...")

        # Wait so the first note isn't clipped
        wait(self.standard_pause)
