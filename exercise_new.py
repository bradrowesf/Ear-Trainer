"""All of the exercises, version 2"""
import random

from midiutilities import MidiUtil
from guitarutilities import GuitarUtil
from player_new import Player_new


class Exercise_new:
    """Parent Class for Exercises"""

    def __init__(self, name, series_size, trials_size, sequence_size) -> None:

        # The classes we'll need
        self.m_u = MidiUtil()
        self.g_u = GuitarUtil()
        self.player = Player_new()

        # The configuration data
        self.name = name
        self.series_size = series_size
        self.trials_size = trials_size
        self.sequence_size = sequence_size

    def __str__(self):
        return self.name

    def do_exercise(self):
        """In child classes, do the exercise in question"""
        print(f"{self.name} -- Exercise not defined.")

    def output_exercise_title(self):
        """Visual for exercise"""

        print('---------------------------------------------------------------------')
        print(f"Exercise: {self.name}")
        print('---------------------------------------------------------------------')

    def output_series_information(self, series, strings, key, mode, position):
        """Visual for series"""

        print("*****")
        print(f"Series: {series + 1} of {self.series_size}")
        print(f"String: {strings}")
        # print(f"Key: {self.key_string(key,mode)}")
        print(f"Position: {position}")
        print("*****")
