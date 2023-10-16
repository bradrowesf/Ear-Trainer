"""Application Menu"""

import datetime
import os
import random
import time


class Application:
    """Register exercises and operate the application menu"""

    def __init__(self):
        self.exercises = []
        self.options = ["m", "r", "e", "x"]   # Our default options

    def register_exercise(self, exercise):
        """Add a new exercise to the menu"""

        self.exercises.append(exercise)
        self.options.append(str(self.exercises.index(exercise)))

    def show_menu(self):
        """Show the user options"""

        os.system('clear')

        print("--------------------------------------")
        print("Exercise Options")
        print("--------------------------------------")

        for index, exercise in enumerate(self.exercises):

            # Iterate across all registered exercises.
            print(f"{index} - {exercise}")

        print("m - Exercise mixer")
        print("r - Random single exercise")
        print("e - Everything (in random order)")
        print("x - Exit")
        print("\n")

    def run_mixer(self):
        """Run a session of mixed trial sets"""

        run_time = 1200  # 20 minutes, in seconds

        start_time = time.time()
        remain_time = run_time
        while remain_time > 0:
            print(
                f"\n--------Time remaining: {str(datetime.timedelta(seconds=int(remain_time)))}--------\n")
            random.choice(self.exercises).do_singleton()
            remain_time = run_time - (time.time() - start_time)

    def run_random(self):
        """Pick an exercise to run at random"""

        exercise = random.choice(self.exercises)
        exercise.do_exercise()

    def run_all_random(self):
        """Do every exercise once, in a random order"""

        for exercise in random.sample(self.exercises, len(self.exercises)):
            exercise.do_exercise()

    def run(self):
        """Run our application"""

        while True:
            while True:
                self.show_menu()

                # What's our choice?
                selection = input("Your Selection: ")

                if selection in self.options:
                    break   # legit option selected

                else:
                    print("Option not available!")
                    print("\n")

            # Execute the selection
            if selection == "m":
                self.run_mixer()
            elif selection == "r":
                self.run_random()
            elif selection == "e":
                self.run_all_random()
            elif selection == "x":
                break
            else:
                self.exercises[int(selection)].do_exercise()
