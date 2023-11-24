"""Quick code testing file"""

import keyboard


def test_key_press(message, options):
    """Test the key press message function"""

    print(message)
    while True:
        key_press = keyboard.read_key(True)
        for option in options:
            if option == key_press:
                return key_press


test_key_press("Press enter:", ["enter", "y"])

test_key_press("Press enter:", ["enter", "y"])
