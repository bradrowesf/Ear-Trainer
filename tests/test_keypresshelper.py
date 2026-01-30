"""Unit Tests for KeyPressHelper functions"""
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock keyboard before importing
sys.modules.setdefault('keyboard', MagicMock())

from src.keypresshelper import key_press_message, any_key_press


class TestKeyPressMessage(unittest.TestCase):
    """Tests for key_press_message()"""

    @patch('src.keypresshelper.keyboard.read_key')
    @patch('builtins.print')
    def test_returns_matching_key(self, mock_print, mock_read_key):
        """Returns the key when it matches an option"""
        mock_read_key.return_value = 'space'
        result = key_press_message("Press space", ["space", "x"])
        self.assertEqual(result, 'space')

    @patch('src.keypresshelper.keyboard.read_key')
    @patch('builtins.print')
    def test_ignores_non_option_keys(self, mock_print, mock_read_key):
        """Keeps reading until a valid option key is pressed"""
        mock_read_key.side_effect = ['a', 'b', 'x']
        result = key_press_message("Press x", ["space", "x"])
        self.assertEqual(result, 'x')
        self.assertEqual(mock_read_key.call_count, 3)


class TestAnyKeyPress(unittest.TestCase):
    """Tests for any_key_press()"""

    @patch('src.keypresshelper.keyboard.wait')
    @patch('builtins.print')
    def test_calls_keyboard_wait_space(self, mock_print, mock_wait):
        """any_key_press calls keyboard.wait('space')"""
        any_key_press("Press Any Key")
        mock_wait.assert_called_once_with('space')
        mock_print.assert_called_once_with("Press Any Key")
