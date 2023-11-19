"""Main entry point into script"""

import logging

from application import Application
from exercise import OneString, OneOctave, OnePosition, ChordTones
from player import Player


def main():
    """Main function of script"""

    # Set logging level
    logging.getLogger().setLevel(logging.ERROR)

    # Instantiate the application
    app = Application()

    # Make a player
    player = Player()

    # Register the exercises
    app.register_exercise(OneString(player))
    app.register_exercise(OneOctave(player))
    app.register_exercise(OnePosition(player))
    app.register_exercise(ChordTones(player))

    # Doit
    app.run()


if __name__ == "__main__":
    main()
