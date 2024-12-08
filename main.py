"""Main entry point into script"""

import logging

from src.application import Application
from src.exercise import OneString, OneOctaveEasy, OneOctaveMedium, OneOctaveHard
from src.exercise import OnePositionEasy, OnePositionMedium, OnePositionHard
from src.exercise import ChordTones, AudiationEasy, AudiationHard, JustTheIntervals
from src.exercise import SingTheIntervalsEasy, SingTheIntervalsHard
from src.exercise import SingTheIntervalsScored
from src.player import Player
from src.scoreboard import Scoreboard


def main():
    """Main function of script"""

    # Set logger
    logging.basicConfig(filename='eartrainer.log',
                        level=logging.DEBUG, filemode='w', force=True)

    # Instantiate the application
    app = Application()

    # Make a player
    player = Player()

    # Create and open the scoreboard
    scoreboard = Scoreboard()
    scoreboard.open()

    # Register the exercises
    app.register_exercise(OneString(player, scoreboard))
    app.register_exercise(OneOctaveEasy(player, scoreboard))
    app.register_exercise(OneOctaveMedium(player, scoreboard))
    app.register_exercise(OneOctaveHard(player, scoreboard))
    app.register_exercise(OnePositionEasy(player, scoreboard))
    app.register_exercise(OnePositionMedium(player, scoreboard))
    app.register_exercise(OnePositionHard(player, scoreboard))
    app.register_exercise(ChordTones(player, scoreboard))
    app.register_exercise(AudiationEasy(player, scoreboard))
    app.register_exercise(AudiationHard(player, scoreboard))
    app.register_exercise(SingTheIntervalsEasy(player, scoreboard))
    app.register_exercise(SingTheIntervalsHard(player, scoreboard))
    app.register_exercise(SingTheIntervalsScored(player, scoreboard))
    app.register_exercise(JustTheIntervals(player, scoreboard))

    # Doit
    app.run()

    # Save scores
    scoreboard.save()


if __name__ == "__main__":
    main()
