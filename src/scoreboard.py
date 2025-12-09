"""Class for tracking performance"""

import json

from src.scorehistory import ScoreHistory


class Scoreboard:
    """Primary class for tracking performance of an exercise"""

    SCORE_MULTIPLIR = [1, 4, 10, 22, 44]
    SCORE_DELIMITER = ':'
    SCORE_PROMOTE = 3.5
    SCORE_DEMOTE = 7.5

    def __init__(self) -> None:

        # Dictionary for score results
        self.persistant_scores = {}

    def get_test_prefix(self, name, element):
        """Standardize dictionary key naming"""

        return name + Scoreboard.SCORE_DELIMITER + element

    def append_score(self, test_name, test_element, trial_avg_times: float):
        """Populate the dictionary with the trial types being scored"""

        if not isinstance(trial_avg_times, float):
            raise TypeError

        if trial_avg_times < 0 or trial_avg_times > 20:
            raise IndexError

        test_key = self.get_test_prefix(test_name, test_element)
        # Have we scored this element yet?
        if test_key in self.persistant_scores:

            # Get the existing score tuple
            score_list = self.persistant_scores[test_key]

            # Only keep 30
            if len(score_list) >= 30:
                score_list.pop(0)

            score_list.append(trial_avg_times)

            # Update
            self.persistant_scores[test_key] = score_list

        else:

            # Add a new test element
            score_list = [trial_avg_times]
            self.persistant_scores[test_key] = score_list

    def get_raw_element_score(self, test_element):
        """Retrieve the raw score of an existing element"""

        if test_element in self.persistant_scores:
            score_list = self.persistant_scores[test_element]
            return sum(score_list)/len(score_list)

        return 20

    def get_adjusted_element_score(self, test_element):
        """Retrieve the score of an existing element"""

        if test_element in self.persistant_scores:
            if len(self.persistant_scores[test_element]) < 5:
                return 20    # Need more trials for significance
            score_list = self.persistant_scores[test_element]

            # Return the average
            return sum(score_list)/len(score_list)

        return 20

    def output_scores(self, test_name, element_list):
        """Show the scores for the provided test name"""

        output_dictionary = {}
        for score_key in self.persistant_scores.keys():
            score_split = score_key.split(Scoreboard.SCORE_DELIMITER)
            if score_split[0] == test_name and \
                    score_split[1] in element_list:
                output_dictionary[score_key] = self.get_raw_element_score(
                    score_key)

        sorted_tuples = sorted(output_dictionary.items(),
                               key=lambda x: x[1], reverse=True)
        sorted_dictionary = dict(sorted_tuples)

        print("--------------")
        print("Updated Scores")
        print("--------------")

        promote_str = "Promotion Candidate"
        demote_str = "Demotion Candidate"
        nada_str = ''
        for key, score in sorted_dictionary.items():

            # Build the "dot" string
            dot_count = 40-len(key)
            dot_string = ""
            while dot_count > 0:
                dot_string += "."
                dot_count -= 1

            # Choose the promote/demote/nada string
            pdn_str = nada_str
            if score <= Scoreboard.SCORE_PROMOTE:
                pdn_str = promote_str
            elif score >= Scoreboard.SCORE_DEMOTE:
                pdn_str = demote_str

            print(f"{key}  {dot_string}  {score:.3f} {pdn_str}")

        # Capture for posterity
        sh = ScoreHistory()
        sh.append_to_history(sorted_dictionary)

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
