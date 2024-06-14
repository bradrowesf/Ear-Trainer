"""Main entry point into script"""

import logging

from src.application import Application
from src.exercise import OneString, OneOctaveEasy, OneOctaveMedium, OneOctaveHard
from src.exercise import OnePositionEasy, OnePositionMedium, OnePositionHard
from src.exercise import ChordTones, AudiationEasy, AudiationHard, JustTheIntervals
from src.player import Player


def main():
    """Main function of script"""

    # Set logger
    logging.basicConfig(filename='eartrainer.log',
                        level=logging.DEBUG, filemode='w', force=True)

    # Instantiate the application
    app = Application()

    # Make a player
    player = Player()

    # Register the exercises
    app.register_exercise(OneString(player))
    app.register_exercise(OneOctaveEasy(player))
    app.register_exercise(OneOctaveMedium(player))
    app.register_exercise(OneOctaveHard(player))
    app.register_exercise(OnePositionEasy(player))
    app.register_exercise(OnePositionMedium(player))
    app.register_exercise(OnePositionHard(player))
    app.register_exercise(ChordTones(player))
    app.register_exercise(AudiationEasy(player))
    app.register_exercise(AudiationHard(player))
    app.register_exercise(JustTheIntervals(player))

    # Doit
    app.run()


if __name__ == "__main__":
    main()
