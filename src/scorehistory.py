"""Class for tracking score and displaying score history"""

import csv
import time
import pandas as pd


class ScoreHistory:
    """Class for all of the historical score function"""

    HISTORY_FILENAME = 'scorehistory.csv'

    def __init__(self):
        pass

    def append_to_history(self, scores: dict):
        """Take the passed dictionary and append to the scores"""

        # Get the current time
        timestamp = time.time()

        # Build the list to write
        csv_list = []
        for key, score in scores.items():
            score_record = [key, score, timestamp]
            csv_list.append(score_record)

        # Open the score history file.
        with open(ScoreHistory.HISTORY_FILENAME, 'a', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_list)
            csvfile.close()

        print('History saved.')

    def get_dataframe(self):
        """Get the df for visualization purposes"""

        return pd.read_csv(ScoreHistory.HISTORY_FILENAME, header=None)
