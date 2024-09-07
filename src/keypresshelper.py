"""Key press helper functions"""
import keyboard


def key_press_message(message, options):
    """Print a message and wait until specific key is hit"""

    print(message)
    while True:
        key_press = keyboard.read_key(True)
        # print(f"Key pressed: {key_press}")
        for option in options:
            if option == key_press:
                return key_press


def any_key_press(message):
    """Accept any keypress"""

    print(message)
    keyboard.wait('space')
