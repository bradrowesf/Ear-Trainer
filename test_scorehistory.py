"""Some test scripts for Scorehistory"""

from src.scoreboard import Scoreboard

sb = Scoreboard()
sb.open()
element_list = [
    'M3', '-M3',
    'm6', '-m6',
    '-m7',
    'M7', '-M7',
    'Aug4', '-Aug4'
]
test_name = 'Singing the Hard Intervals'
sb.output_scores(test_name, element_list)
