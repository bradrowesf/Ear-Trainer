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
    MAX_ELAPSED_TIME = 20
    HOLD_ON_ONE_MULTIPLIER = 4


class Player:
    """The thing that plays the notes"""

    def __init__(self):

        # Create and configure the session and part.
        self.session = Session(tempo=120)
        self.part = self.session.new_part("Clarinet")

        # Playback settings
        self.volume = 1
        self.duration = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        """Cleanup the session"""
        if hasattr(self, 'session') and self.session is not None:
            self.session.kill()
            self.session = None

    def _do_key_pause(self, message, options):
        """Whenever we need to pause and wait for keyboard input"""

        # Message and wait for the keyboard
        pressed_key = key_press_message(message, options)

        # Wait so the first note isn't clipped
        wait(PlayerConst.NO_CLIP_PAUSE)

        return pressed_key

    def _get_remaining_time(self, start_time: float, duration: float) -> float:
        """Calculate remaining time in the exercise"""
        return duration - (time.time() - start_time)

    def _format_time_string(self, seconds: float) -> str:
        """Format seconds into MM:SS string"""
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"

    def _play_notes_sequence(self, trial: list[int]):
        """Play all notes in a trial sequentially"""
        for note in trial:
            self.part.play_note(note, self.volume, self.duration)

    def _prompt_to_start(self, trial_number: int, total_trials: int,
                         time_string: str, trial_definition: str) -> bool:
        """Display trial info and prompt user to start or exit"""
        print(f"Trial #{trial_number} of {total_trials} [{time_string}]")
        print(trial_definition)
        return self._do_key_pause("Press SPACE to start or 'x' to exit...",
                                  ["space", "x"]) != "x"

    def _handle_series_interactive_options(self, trial: list[int]) -> bool:
        """Handle repeat/reverse/exit options for SERIES exercises"""
        while True:
            response = self._do_key_pause(
                "Press 'r' for repeat, 'v' for reverse, "
                "'x' for exit, or 'space' to continue.",
                ["r", "v", "x", "space"])
            if response == "r":
                self._play_notes_sequence(trial)
                continue
            elif response == "v":
                reverse_trial = reversed(trial)
                self._play_notes_sequence(reverse_trial)
                continue
            elif response == "x":
                return False
            else:
                return True

    def _handle_scoring_display(self, elapsed_times: list[float]):
        """Display average time to user"""
        average_times = sum(elapsed_times) / len(elapsed_times)
        print(f" ** Adjusted Average Time: {average_times:.2f} seconds **")
        self._do_key_pause("Press SPACE to continue...", ["space"])

    def _play_interval_trial(self, trial: list[int], package: ExercisePackage) -> float:
        """Execute interval exercise with timing"""
        # Trial sets should only be size 2
        assert len(trial) == 2

        note1 = trial[0]
        note2 = trial[1]

        # Play the first note and wait
        self.part.play_note(note1, self.volume, self.duration)
        wait(package.get_interval_pause())

        response_time_seconds = time.time()
        if package.get_mid_trial_prompt_enabled():
            any_key_press("Press space when ready...")
            response_time_seconds = time.time() - response_time_seconds
            print(
                f"        Time to answer: {response_time_seconds:.2f} seconds.")

            # Maximum adjusted time is 20 seconds
            response_time_seconds = min(
                response_time_seconds, PlayerConst.MAX_ELAPSED_TIME)

            wait(PlayerConst.NO_CLIP_PAUSE)

        # Play the answer and briefly wait
        self.part.play_note(note2, self.volume, self.duration)
        if package.get_trial_repeat_enabled():
            wait(package.get_trial_repeat_pause())

        # And repeat
        self.part.play_note(note1, self.volume, self.duration)
        self.part.play_note(note2, self.volume, self.duration)

        # Did you get it right?
        if package.get_mid_trial_prompt_enabled():
            if self._do_key_pause("Press SPACE if correct or 'x' if wrong...",
                                  ["space", "x"]) == "x":
                response_time_seconds = 20

        # Pause before the next trial
        wait(package.get_post_trial_pause())

        return response_time_seconds

    def _play_series_trial(self, trial: list[int],
                           package: ExercisePackage, trial_index: int) -> bool:
        """Execute series/series-hold-on-one exercise"""
        # Play through all the notes in the trial
        self._play_notes_sequence(trial)

        # If option selected, wait for a key press before deciding what to do
        if package.get_mid_trial_prompt_enabled():
            if not self._handle_series_interactive_options(trial):
                return False

        # If the option to repeat trials is selected, repeat it
        if package.get_trial_repeat_enabled():
            wait(package.get_trial_repeat_pause())
            self._play_notes_sequence(trial)

        # Pause before the next trial
        pause_time = package.get_post_trial_pause()

        # Increase the pause time for first trial in the HOLD_ON_ONE exercises
        if trial_index == 0 and package.get_exercise_type() == ExerciseType.SERIES_HOLD_ON_ONE:
            pause_time = PlayerConst.HOLD_ON_ONE_MULTIPLIER * pause_time

        wait(pause_time)
        return True

    def _execute_trial(self, trial: list[int], trial_index: int, package: ExercisePackage) -> float:
        """Route to appropriate trial executor based on exercise type"""
        exercise_type = package.get_exercise_type()

        if exercise_type == ExerciseType.INTERVAL:
            return self._play_interval_trial(trial, package)
        elif exercise_type in (ExerciseType.SERIES, ExerciseType.SERIES_HOLD_ON_ONE):
            if self._play_series_trial(trial, package, trial_index):
                return 0.0
            else:
                # User chose to exit
                return -1.0
        else:
            # An undefined type of exercise was requested
            raise IndexError

    def _execute_trial_set(self, trial_set: list[list[int]], trial_definition: str,
                           trial_set_index: int, package: ExercisePackage, remaining_time: float) \
            -> tuple[bool, list[float]]:
        """Execute one complete trial set"""
        # Prompt user to start
        one_based_index = trial_set_index + 1
        time_string = self._format_time_string(remaining_time)
        if not self._prompt_to_start(one_based_index, len(package),
                                     time_string, trial_definition):
            return (False, [])

        # Iterate through the trials
        elapsed_times = []
        for trial_index, trial in enumerate(trial_set):
            one_based_index = trial_index + 1
            print(f"---- {one_based_index}/{len(trial_set)}")

            # Execute the trial
            elapsed_time = self._execute_trial(trial, trial_index, package)
            if elapsed_time < 0:
                return (False, [])  # User chose to exit
            if elapsed_time > 0:
                elapsed_times.append(elapsed_time)

        return (True, elapsed_times)

    def play(self, package: ExercisePackage, scoreboard: Scoreboard, duration):
        """Play the notes defined in the trial_sets list"""

        start_time = time.time()
        test_name = package.get_test_name()

        # Iterate through the trial sets
        for trial_set_index, (trial_set, trial_definition, trial_label) in enumerate(package):

            remaining_time = self._get_remaining_time(start_time, duration)
            if remaining_time < 0:
                break  # Time's up

            # Execute the trial set
            should_continue, elapsed_times = self._execute_trial_set(
                trial_set, trial_definition, trial_set_index, package, remaining_time)

            if not should_continue:
                return

            # Handle scoring
            if package.get_scoring_enabled() and elapsed_times:
                self._handle_scoring_display(elapsed_times)
                average_times = sum(elapsed_times) / len(elapsed_times)
                scoreboard.append_score(test_name, trial_label, average_times)
