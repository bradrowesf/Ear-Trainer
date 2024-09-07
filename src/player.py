"""Player Class, v2"""

import time

from scamp import Session
from scamp import wait

from src.keypresshelper import key_press_message, any_key_press


class Player:
    """The thing that plays the notes"""

    def __init__(self):

        # Create and configure the session and part.
        self.session = Session(tempo=120)
        self.part = self.session.new_part("Clarinet")

        # Set initial config values
        self.post_trial_pause = 2
        self.trial_repeat_pause = 2
        self.mid_trial_pause = 2
        self.press_key_pause = False
        self.no_clip_pause = 2  # This one is just to prevent weird errors from scamp
        self.volume = 1
        self.duration = 1
        self.trial_sets = []
        self.trial_definitions = []
        self.trial_repeat = False
        self.enable_interval_singing = False

    def __del__(self):
        self.session.kill()     # Cleanup the session

    def set_post_trial_pause(self, post_trial_pause):
        """Set Post Trial Set Pause"""

        self.post_trial_pause = post_trial_pause

    def set_trial_repeat_pause(self, trial_repeat_pause):
        """Set Mid Trial Set Pause"""

        self.trial_repeat_pause = trial_repeat_pause

    def set_trial_repeat(self, trial_repeat):
        """Set Trial Repeat"""

        self.trial_repeat = trial_repeat

    def set_enable_interval_singing(self, enable_interval_singing):
        """Set play style for interval singing"""

        self.enable_interval_singing = enable_interval_singing

    def set_press_key_pause(self, press_key_pause):
        """Set the flag for mid-trial key press to continue"""

        self.press_key_pause = press_key_pause

    def set_trial_lists(self, trial_sets, trial_definitions):
        """Feed the list of trial sets to the player"""

        self.trial_sets = trial_sets
        self.trial_definitions = trial_definitions

    # def pre_roll(self):
    #     """Pause before start of playing"""

    #     # Wait for the user to press a key to begin
    #     key_press_message("Press ENTER to begin trial set...", ["enter"])

    #     # Wait so the first note isn't clipped
    #     wait(self.no_clip_pause)

    def do_key_pause(self, message, options):
        """Whenever we need to pause and wait for keyboard input"""

        # Message and wait for the keyboard
        pressed_key = key_press_message(message, options)

        # Wait so the first note isn't clipped
        wait(self.no_clip_pause)

        return pressed_key

    def play(self, duration):
        """Play the notes defined in the trial_sets list"""

        # Helper Inner Functions
        def play_full_trial(trial):
            for note in trial:
                self.part.play_note(note, self.volume, self.duration)

        def play_interval_trial(trial):

            # Trial sets should only be size 2.
            assert len(trial) == 2

            note1 = trial[0]
            note2 = trial[1]

            # Play the first note and wait
            self.part.play_note(note1, self.volume, self.duration)
            wait(self.mid_trial_pause)

            if self.press_key_pause:
                any_key_press("Press key when ready...")

            # Play the answer and briefly wait.
            self.part.play_note(note2, self.volume, self.duration)
            wait(self.mid_trial_pause/2)  # shorter

            # And repeat
            self.part.play_note(trial, self.volume, self.duration)

        start_time = time.time()

        # Iterate through the trial sets.
        trial_set_index = 0
        for trial_set, trial_definition in zip(self.trial_sets, self.trial_definitions):

            remain_time = duration - (time.time() - start_time)
            if remain_time < 0:
                return      # Time's up

            # Output the info about the trial set
            trial_set_index += 1

            # Format the time string
            minutes, seconds = divmod(remain_time, 60)
            remain_time_string = f"{int(minutes):02d}:{int(seconds):02d}"

            # Inform user
            print(
                f"Trial #{trial_set_index} of {len(self.trial_sets)} [{remain_time_string}]")
            print(trial_definition)

            # Let the user get ready.
            if self.do_key_pause("Press SPACE to start or 'x' to exit...", ["space", "x"]) == "x":
                return

            # Iterate through the trials.
            trial_index = 0
            for trial in trial_set:
                trial_index += 1
                print(f"---- {trial_index}/{len(trial_set)}")

                # Are we interval singing?
                if self.enable_interval_singing:
                    play_interval_trial(trial)
                    continue

                # Play through all the notes in the trial.
                play_full_trial(trial)

                # If option selected, wait for a key press before deciding what to do.
                if self.press_key_pause:
                    while True:
                        response = self.do_key_pause(
                            "Press 'r' for repeat, 'v' for reverse, "
                            "'x' for exit, or 'space' to continue.",
                            ["r", "v", "x", "space"])
                        if response == "r":
                            play_full_trial(trial)
                            continue
                        elif response == "v":
                            reverse_trial = reversed(trial)
                            play_full_trial(reverse_trial)
                            continue
                        elif response == "x":
                            return
                        else:
                            break

                # If the option to repeat trials is selected, repeat it.
                if self.trial_repeat:
                    wait(self.trial_repeat_pause)
                    play_full_trial(trial)

                wait(self.post_trial_pause)    # Pause before the next trial
