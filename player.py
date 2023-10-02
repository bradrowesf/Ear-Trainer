"""Player Class, v2"""

import os
from scamp import Session
from scamp import wait


class Player:
    """The thing that plays the notes"""

    def __init__(self):

        # Create and configure the session and part.
        self.session = Session(tempo=120)
        self.part = self.session.new_part("Clarinet")

        # Set initial config values
        self.post_trial_pause = 2
        self.mid_trial_pause = 2
        self.press_key_pause = False
        self.no_clip_pause = 2  # This one is just to prevent weird errors from scamp
        self.volume = 1
        self.duration = 1
        self.trial_sets = []
        self.trial_definitions = []
        self.trial_repeat = False

    def set_post_trial_pause(self, post_trial_pause):
        """Set Post Trial Set Pause"""

        self.post_trial_pause = post_trial_pause

    def set_mid_trial_pause(self, mid_trial_pause):
        """Set Mid Trial Set Pause"""

        self.mid_trial_pause = mid_trial_pause

    def set_trial_repeat(self, trial_repeat):
        """Set Trial Repeat"""

        self.trial_repeat = trial_repeat

    def set_press_key_pause(self, press_key_pause):
        """Set the flag for mid-trial key press to continue"""

        self.press_key_pause = press_key_pause

    def set_trial_lists(self, trial_sets, trial_definitions):
        """Feed the list of trial sets to the player"""

        self.trial_sets = trial_sets
        self.trial_definitions = trial_definitions

    def pre_roll(self):
        """Pause before start of playing"""

        # Wait for the user to press a key to begin
        input("Press ENTER to begin trial set...")

        # Wait so the first note isn't clipped
        wait(self.no_clip_pause)

    def play(self):
        """Play the notes defined in the trial_sets list"""

        # Iterate through the trial sets.
        trial_set_index = 0
        for trial_set, trial_definition in zip(self.trial_sets, self.trial_definitions):

            # Output the info about the trial set
            trial_set_index += 1
            print(f"Trial #{trial_set_index} of {len(self.trial_sets)}")
            print(trial_definition)

            # Let the user get ready.
            self.pre_roll()

            # Iterate through the trials.
            trial_index = 0
            for trial in trial_set:
                trial_index += 1
                print(f"---- {trial_index}/{len(trial_set)}")

                # Play through all the notes in the trial.
                for note in trial:
                    self.part.play_note(note, self.volume, self.duration)

                # If option selected, wait for a key press before next trial.
                if self.press_key_pause:
                    os.system('pause')

                # If the option to repeat trials is selected, repeat it.
                if self.trial_repeat:
                    wait(self.mid_trial_pause)
                    for note in trial:
                        self.part.play_note(note, self.volume, self.duration)

                wait(self.post_trial_pause)    # Pause before the next trial
