"""Class for tracking performance"""

import json


class Scoreboard:
    """Primary class for tracking performance of an exercise"""

    SCORE_MULTIPLIER = [1, 1, 1.3333333, 2]

    def __init__(self) -> None:

        # Dictionary for score results
        self.persistant_scores = {}

    def get_test_prefix(self, name, element):
        """Standardize dictionary key naming"""

        return name + ":" + element

    def append_score(self, test_name, test_element, trial_score: int):
        """Populate the dictionary with the trial types being scored"""

        if not isinstance(trial_score, int):
            raise TypeError

        if trial_score < 1 or trial_score > 4:
            raise IndexError

        test_key = self.get_test_prefix(test_name, test_element)
        # Have we scored this element yet?
        if test_key in self.persistant_scores:

            # Get the existing score tuple
            score_list = self.persistant_scores[test_key]

            # Only keep 30
            if len(score_list) >= 30:
                score_list.pop(0)

            score_list.append(trial_score)

            # Update
            self.persistant_scores[test_key] = score_list

        else:

            # Add a new test element
            score_list = [trial_score]
            self.persistant_scores[test_key] = score_list

    def get_raw_element_score(self, test_element):
        """Retrieve the raw score of an existing element"""

        if test_element in self.persistant_scores:
            score_list = self.persistant_scores[test_element]
            return sum(score_list)/len(score_list)

        return 1

    def get_adjusted_element_score(self, test_element):
        """Retrieve the score of an existing element"""

        if test_element in self.persistant_scores:
            if len(self.persistant_scores[test_element]) < 5:
                return 1    # Need more trials for significance
            score_list = self.persistant_scores[test_element]
            adjusted_scores = []
            for raw_score in score_list:
                adjusted_scores.append(
                    raw_score*Scoreboard.SCORE_MULTIPLIER[raw_score-1])

            return sum(adjusted_scores)/len(adjusted_scores)

        return 1

    def output_scores(self, element_prefix):
        """Show the scores for the provided test name"""

        output_dictionary = {}
        for score_key in self.persistant_scores.keys():
            if score_key.find(element_prefix) == 0:
                output_dictionary[score_key] = self.get_raw_element_score(
                    score_key)

        sorted_tuples = sorted(output_dictionary.items(),
                               key=lambda x: x[1], reverse=True)
        sorted_dictionary = dict(sorted_tuples)

        print("--------------")
        print("Updated Scores")
        print("--------------")

        for key, score in sorted_dictionary.items():
            print(f"{key} --- {score}")

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
