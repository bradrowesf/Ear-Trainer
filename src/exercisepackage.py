"""A claset of classes for everything needed to execute an exercise"""

from enum import Enum


class ExerciseType(Enum):
    """Enumerated types for exercise types"""

    SERIES = 1
    INTERVAL = 2


class PauseDuration(Enum):
    """Enumerated types for pause duration"""

    SHORT = 1
    MEDIUM = 2
    LONG = 4


class ExercisePackage:
    """Container for exercise content needed by the player"""

    def __init__(self, exercise_type: ExerciseType, post_trial_pause: PauseDuration) -> None:

        # Exercise Type
        if exercise_type not in list(ExerciseType):
            raise IndexError
        self.exercise_type = exercise_type

        # Delay between the end of one trial and the start of the next
        if post_trial_pause not in list(PauseDuration):
            raise IndexError
        self.post_trial_pause = post_trial_pause

        # The sets
        self.trial_sets = []
        self.trial_set_definitions = []
        self.trial_set_label = []

        # For iteration
        self.index = 0

    def reset(self):
        """Clear everything so we can build a new package"""

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
