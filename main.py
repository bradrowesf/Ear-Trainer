"""Main entry point into script"""

import logging

from application import Application
# from exercise import OneString_old, TwoString, OnePosition,
# OnePositionHammer, Sequence, Simon, OneStringHammer
from exercise import OneString, OneOctave, OnePosition


def main():
    """Main function of script"""

    # Set logging level
    logging.getLogger().setLevel(logging.ERROR)

    # Instantiate the application
    app = Application()

    # Register the exercises
#    app.register_exercise(OneString_old(player))
#    app.register_exercise(OneStringHammer(player))
#    app.register_exercise(TwoString(player))
#    app.register_exercise(OnePosition(player))
#    app.register_exercise(OnePositionHammer(player))
#    app.register_exercise(Sequence(player))
#    app.register_exercise(Simon(player))
    app.register_exercise(OneString())
    app.register_exercise(OneOctave())
    app.register_exercise(OnePosition())

    # Doit
    app.run()


if __name__ == "__main__":
    main()
