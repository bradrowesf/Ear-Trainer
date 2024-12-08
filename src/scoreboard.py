"""Class for tracking performance"""

import json


class Scoreboard:
    """Primary class for tracking performance of an exercise"""

    def __init__(self) -> None:

        # List for raw score results
        self.active_scores = []

        # Dictionary for aggregation
        self.persistant_scores = {}

        # flag for unaggregated scores
        self.new_scores = False

    def append_score(self, test_element, trial_score):
        """Populate the dictionary with the trial types being scored"""

        score_tuple = (test_element, trial_score)
        self.active_scores.append(score_tuple)
        self.new_scores = True

    def assemble_scores(self):
        """Tally up all the new scores"""

        if self.new_scores is False:
            return      # Don't do anything

        for score in self.active_scores:
            test_element = score[0]
            trial_score = score[1]

            # Have we scored this element yet?
            if test_element in self.persistant_scores:

                # Get the existing score tuple
                score_tuple = self.persistant_scores[test_element]
                current_score = score_tuple[0]
                current_trial_count = score_tuple[1]

                # Rebuild it with the new score
                score_sum = current_score * current_trial_count
                score_sum += trial_score
                current_trial_count += 1
                current_score = score_sum / current_trial_count

                # Shove it back in the Dictionary
                self.persistant_scores[test_element] = (
                    current_score, current_trial_count)

            else:

                # Add a new test element
                self.persistant_scores[test_element] = (trial_score, 1)

        # clear the active scores and flag
        self.active_scores.clear()
        self.new_scores = False

    def open(self):
        """Read the scores from a saved file"""

        # Clear the deck
        self.active_scores.clear()
        self.persistant_scores.clear()

        try:
            with open('scores.json', 'r', encoding="utf-8") as score_file:
                self.persistant_scores = json.load(score_file)
        except FileNotFoundError:
            return

    def save(self):
        """Write the persistant scores to a file"""

        # Process any unassembled scores
        if self.new_scores:
            self.assemble_scores()

        with open('scores.json', 'w', encoding="utf-8") as score_file:
            score_file.write(json.dumps(self.persistant_scores))

    def __str__(self):
        """An output to screen method"""

        return str(self.persistant_scores)
