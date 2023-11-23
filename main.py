"""Main entry point into script"""

import logging

from src.application import Application
from src.exercise import OneString, OneOctaveEasy, OneOctaveHard, OnePosition, ChordTones
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
    app.register_exercise(OneOctaveHard(player))
    app.register_exercise(OnePosition(player))
    app.register_exercise(ChordTones(player))

    # Doit
    app.run()


if __name__ == "__main__":
    main()
