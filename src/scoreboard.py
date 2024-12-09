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
                score_list = self.persistant_scores[test_element]

                # Only keep 100
                if len(score_list) >= 100:
                    score_list.pop(0)

                score_list.append(trial_score)

                # Update
                self.persistant_scores[test_element] = score_list

            else:

                # Add a new test element
                score_list = [trial_score]
                self.persistant_scores[test_element] = score_list

        # clear the active scores and flag
        self.active_scores.clear()
        self.new_scores = False

    def get_element_score(self, test_element):
        """Retrieve the score of an existing element"""

        if test_element in self.persistant_scores:
            score_list = self.persistant_scores[test_element]
            return sum(score_list)/len(score_list)

        return 1

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


sc = Scoreboard()
sc.open()
for x in range(1, 110):
    sc.append_score("Test", x/7)
    sc.assemble_scores()
    if x % 5 == 0:
        print(sc.get_element_score("Test"))
sc.save()
