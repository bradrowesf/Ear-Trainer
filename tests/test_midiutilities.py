"""Unit tests for MidiUtil class"""
import unittest

from midiutilities import MidiUtil


class TestMidiUtil(unittest.TestCase):
    """Testing class"""

    def setUp(self):
        """Setup"""

        self.mu = MidiUtil()

    def test_getitem(self):
        """Test Method"""

        self.assertEqual(self.mu[70], 'A#4')
        self.assertEqual(self.mu[112], 'E8')
        self.assertEqual(self.mu[97], 'C#7')
        self.assertEqual(self.mu[42], 'F#2')
        self.assertEqual(self.mu[56], 'G#3')
        self.assertEqual(self.mu[65], 'F4')

        with self.assertRaises(IndexError):
            _ = self.mu[128]

    def test_index(self):
        """Test Method"""

        self.assertEqual(self.mu.index('E6'), 88)
        self.assertEqual(self.mu.index('D#2'), 39)
        self.assertEqual(self.mu.index('G4'), 67)
        self.assertEqual(self.mu.index('A#5'), 82)
        self.assertEqual(self.mu.index('C5'), 72)
        self.assertEqual(self.mu.index('B1'), 35)

        with self.assertRaises(ValueError):
            self.mu.index('H#9')
