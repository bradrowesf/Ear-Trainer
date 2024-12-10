"""Class for tracking performance"""

import json


class Scoreboard:
    """Primary class for tracking performance of an exercise"""

    def __init__(self) -> None:

        # Dictionary for score results
        self.persistant_scores = {}

    def append_score(self, test_element, trial_score: int):
        """Populate the dictionary with the trial types being scored"""

        if not isinstance(trial_score, int):
            raise TypeError

        if trial_score < 1 or trial_score > 4:
            raise IndexError

        score2record = 1
        if trial_score == 4:
            score2record = 8
        elif trial_score == 3:
            score2record = 4
        elif trial_score == 2:
            score2record = 2

        # Have we scored this element yet?
        if test_element in self.persistant_scores:

            # Get the existing score tuple
            score_list = self.persistant_scores[test_element]

            # Only keep 100
            if len(score_list) >= 30:
                score_list.pop(0)

            score_list.append(score2record)

            # Update
            self.persistant_scores[test_element] = score_list

        else:

            # Add a new test element
            score_list = [score2record]
            self.persistant_scores[test_element] = score_list

    def get_element_score(self, test_element):
        """Retrieve the score of an existing element"""

        if test_element in self.persistant_scores:
            score_list = self.persistant_scores[test_element]
            return sum(score_list)/len(score_list)

        return 1

    def open(self):
        """Read the scores from a saved file"""

        # Clear the deck
        self.persistant_scores.clear()

        try:
            with open('scores.json', 'r', encoding="utf-8") as score_file:
                self.persistant_scores = json.load(score_file)
        except FileNotFoundError:
            return

    def save(self):
        """Write the persistant scores to a file"""

        with open('scores.json', 'w', encoding="utf-8") as score_file:
            score_file.write(json.dumps(self.persistant_scores))

    def __str__(self):
        """An output to screen method"""

        return str(self.persistant_scores)
