"""Player Class, v2"""

import time

from enum import Enum
from scamp import Session
from scamp import wait

from src.keypresshelper import key_press_message, any_key_press
from src.exercisepackage import ExercisePackage, ExerciseType
from src.scoreboard import Scoreboard


class PlayerConst(float, Enum):
    """Namespace for constants"""

    NO_CLIP_PAUSE = 2


class Player:
    """The thing that plays the notes"""

    def __init__(self):

        # Create and configure the session and part.
        self.session = Session(tempo=120)
        self.part = self.session.new_part("Clarinet")

        # Playback settings
        self.volume = 1
        self.duration = 1

        # Scoreboard
        self.s_b = Scoreboard()

    def __del__(self):
        self.session.kill()     # Cleanup the session

    def do_key_pause(self, message, options):
        """Whenever we need to pause and wait for keyboard input"""

        # Message and wait for the keyboard
        pressed_key = key_press_message(message, options)

        # Wait so the first note isn't clipped
        wait(PlayerConst.NO_CLIP_PAUSE)

        return pressed_key

    def play(self, package: ExercisePackage, duration):
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
            wait(package.get_interval_pause())

            if package.get_mid_trial_prompt_enabled():
                any_key_press("Press space when ready...")
                wait(PlayerConst.NO_CLIP_PAUSE)

            # Play the answer and briefly wait.
            self.part.play_note(note2, self.volume, self.duration)
            if package.get_trial_repeat_enabled():
                wait(package.get_trial_repeat_pause())

            # And repeat
            self.part.play_note(note1, self.volume, self.duration)
            self.part.play_note(note2, self.volume, self.duration)
            # Pause before the next trial
            wait(package.get_post_trial_pause())

        start_time = time.time()

        # Iterate through the trial sets.
        trial_set_index = 0
        for trial_set_index, (trial_set, trial_definition, trial_label) in enumerate(package):

            remain_time = duration - (time.time() - start_time)
            if remain_time < 0:
                break      # Time's up

            # Output the info about the trial set

            # Format the time string
            minutes, seconds = divmod(remain_time, 60)
            remain_time_string = f"{int(minutes):02d}:{int(seconds):02d}"

            # Inform user
            human_index = trial_set_index + 1
            print(
                f"Trial #{human_index} of {len(package)} [{remain_time_string}]")
            print(trial_definition)

            # Let the user get ready.
            if self.do_key_pause("Press SPACE to start or 'x' to exit...", ["space", "x"]) == "x":
                return

            # Iterate through the trials.
            for trial_index, trial in enumerate(trial_set):
                # trial_index += 1
                human_index = trial_index + 1
                print(f"---- {human_index}/{len(trial_set)}")

                # What type of exercise?
                if package.get_exercise_type() == ExerciseType.INTERVAL:
                    play_interval_trial(trial)
                    continue

                elif package.get_exercise_type() == ExerciseType.SERIES:

                    # Play through all the notes in the trial.
                    play_full_trial(trial)

                    # If option selected, wait for a key press before deciding what to do.
                    if package.get_mid_trial_prompt_enabled():
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
                    if package.get_trial_repeat_enabled():
                        wait(package.get_trial_repeat_pause())
                        play_full_trial(trial)

                    # Pause before the next trial
                    wait(package.get_post_trial_pause())

                else:
                    # An undefined type of exercise was requested
                    raise IndexError

            # Score it here
            if True:
                score = self.do_key_pause(
                    "Score (1-4):", ["1", "2", "3", "4"])
                self.s_b.append_score(trial_label, score)

        self.s_b.assemble_scores()
        print(self.s_b)
        self.do_key_pause("Press Space", ["space"])
