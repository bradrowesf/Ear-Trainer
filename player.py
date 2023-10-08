"""Player Class, v2"""

import keyboard
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

    def do_key_pause(self, message):
        """Whenever we need to pause and wait for keyboard input"""

        # Message and wait for the keyboard
        print(message)
        pressed_key = keyboard.read_key(True)

        # Wait so the first note isn't clipped
        wait(self.no_clip_pause)

        return pressed_key

    def play(self):
        """Play the notes defined in the trial_sets list"""

        # Helper Inner Functions
        def play_trial(trial):
            for note in trial:
                self.part.play_note(note, self.volume, self.duration)

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
                play_trial(trial)

                # If option selected, wait for a key press before deciding what to do.
                if self.press_key_pause:
                    moving_on = False
                    while not moving_on:
                        response = self.do_key_pause(
                            "Press 'r' for repeat, 'x' for exit, or anything else to continue.")
                        if response == "r":
                            play_trial(trial)
                            continue
                        elif response == "x":
                            return
                        else:
                            moving_on = True

                # If the option to repeat trials is selected, repeat it.
                if self.trial_repeat:
                    wait(self.mid_trial_pause)
                    for note in trial:
                        self.part.play_note(note, self.volume, self.duration)

                wait(self.post_trial_pause)    # Pause before the next trial
