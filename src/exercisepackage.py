"""A claset of classes for everything needed to execute an exercise"""

from enum import Enum


class ExerciseType(Enum):
    """Enumerated types for exercise types"""

    SERIES = 1
    SERIES_HOLD_ON_ONE = 2
    INTERVAL = 3

    @classmethod
    def validate(cls, test_value):
        """Is this value one of the enumerated options"""

        if not test_value in cls:
            raise IndexError


class PauseDuration(float, Enum):
    """Enumerated types for pause duration"""

    NOT_APPLICABLE = -1
    NONE = 0
    BLIP = .5
    SHORT = 1
    SMEDIUM = 2.5
    MEDIUM = 3
    LMEDIUM = 4
    LONG = 5
    VLONG = 8

    @classmethod
    def validate(cls, test_value):
        """Is this value one of the enumerated options"""

        if not test_value in cls:
            raise IndexError


class ExercisePackage:
    """Container for exercise content needed by the player"""

    def __init__(self,
                 exercise_type: ExerciseType,
                 post_trial_pause: PauseDuration,
                 interval_pause: PauseDuration,
                 trial_repeat_pause: PauseDuration,
                 mid_trial_prompt_enabled: bool,
                 scoring_enabled: bool = False) -> None:

        # Exercise Type
        ExerciseType.validate(exercise_type)
        self.exercise_type = exercise_type

        # Delay between the end of one trial and the start of the next
        PauseDuration.validate(post_trial_pause)
        if post_trial_pause == PauseDuration.NOT_APPLICABLE:
            raise ValueError
        self.post_trial_pause = post_trial_pause

        # Delay between the base note and test interval
        PauseDuration.validate(interval_pause)
        if (exercise_type == ExerciseType.INTERVAL
                and interval_pause == PauseDuration.NOT_APPLICABLE):
            raise ValueError
        elif (exercise_type == ExerciseType.SERIES
                and interval_pause != PauseDuration.NOT_APPLICABLE):
            raise ValueError
        self.interval_pause = interval_pause

        # Are we doing a repeat of the trial and what's the delay
        PauseDuration.validate(trial_repeat_pause)
        if (exercise_type == ExerciseType.INTERVAL
                and trial_repeat_pause == PauseDuration.NOT_APPLICABLE):
            raise ValueError
        self.trial_repeat_pause = trial_repeat_pause

        # Are we prompting in the middle of the trial
        self.mid_trial_prompt_enabled = mid_trial_prompt_enabled

        # Are we keeping score
        self.scoring_enabled = scoring_enabled

        # The name of the test this package is representing
        self.trial_test_name = ""

        # The sets
        self.trial_sets = []
        self.trial_set_definitions = []
        self.trial_set_label = []

        # For iteration
        self.index = 0

    def reset(self):
        """Clear everything so we can build a new package"""

        # clear the name
        self.trial_test_name = ""

        # clear the lists
        self.trial_sets.clear()
        self.trial_set_definitions.clear()
        self.trial_set_label.clear()

    def __iter__(self):

        return self

    def __next__(self):

        if self.index >= len(self.trial_sets):
            raise StopIteration

        current_index = self.index
        self.index += 1
        return self.trial_sets[current_index], \
            self.trial_set_definitions[current_index], \
            self.trial_set_label[current_index]

    def __len__(self):
        """Size of this iterator"""

        # Any of the lists should have the right answer
        return len(self.trial_sets)

    def set_test_name(self, name: str):
        """Set the name of the test we're the package for"""

        self.trial_test_name = name

    def get_test_name(self):
        """Get the test name"""

        return self.trial_test_name

    def append_trial_set(self, trial_set, trial_definition, trial_label):
        """Incoming set"""

        self.trial_sets.append(trial_set)
        self.trial_set_definitions.append(trial_definition)
        self.trial_set_label.append(trial_label)

    def get_exercise_type(self):
        """Get the exercise type"""

        return self.exercise_type

    def get_post_trial_pause(self):
        """Get for post_trial pause"""

        return self.post_trial_pause

    def get_interval_pause(self):
        """Get for interval_pause pause"""

        return self.interval_pause

    def get_trial_repeat_pause(self):
        """Get for interval_pause pause"""

        return self.trial_repeat_pause

    def get_trial_repeat_enabled(self):
        """Get for trial repeat functionality"""

        return self.trial_repeat_pause != PauseDuration.NOT_APPLICABLE

    def get_mid_trial_prompt_enabled(self):
        """Get for mid trial prompt functionality"""

        return self.mid_trial_prompt_enabled

    def get_scoring_enabled(self):
        """Get for scoring functionality"""

        return self.scoring_enabled
