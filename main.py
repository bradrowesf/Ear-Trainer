"""Main entry point into script"""

from player import Player

from application import Application
from exercise import OneString, TwoString, OnePosition, Sequence, Simon

import logging


def main():
    """Main function of script"""

    # Set logging level
    logging.getLogger().setLevel(logging.ERROR)

    # Instantiate the application
    app = Application()

    # Make the player
    player = Player()

    # Register the exercises
    app.register_exercise(OneString(player))
    app.register_exercise(TwoString(player))
    app.register_exercise(OnePosition(player))
    app.register_exercise(Sequence(player))
    app.register_exercise(Simon(player))

    # Doit
    app.run()


if __name__ == "__main__":
    main()
