"""Class for tracking performance"""


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

    def __str__(self):
        """An output to screen method"""

        return str(self.persistant_scores)


# Some testing code
sc = Scoreboard()
sc.append_score('M3', 1)
sc.append_score('M2', 2)
sc.append_score('M1', 3)
sc.append_score('M6', 4)
sc.append_score('M7', 1)
sc.append_score('M1', 2)
sc.append_score('M2', 3)
sc.append_score('M2', 3)
sc.append_score('M2', 1)
sc.append_score('M6', 2)
sc.assemble_scores()
print(sc)
