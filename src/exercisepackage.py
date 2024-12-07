"""A class for everything needed to execute an exercise"""


class ExercisePackage:
    """Container for exercise content needed by the player"""

    def __init__(self) -> None:

        self.trial_sets = []
        self.trial_set_definitions = []
        self.trial_set_label = []

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

    def append_trial_set(self, trial_set, trial_definition, label):
        """Incoming set"""

        self.trial_sets.append(trial_set)
        self.trial_set_definitions.append(trial_definition)
        self.trial_set_label.append(label)
