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

    def test_build_from_intervals(self):
        """Test Method"""

        self.assertEqual(self.mu.build_from_intervals(
            40, 'Dorian'), [40, 42, 43, 45, 47, 49, 50, 52])
        self.assertEqual(self.mu.build_from_intervals(
            63, 'IV7'), [63, 66, 68, 72, 75])
        self.assertEqual(self.mu.build_from_intervals(
            90, 'Major Pentatonic'), [90, 92, 94, 97, 99, 102])
        self.assertEqual(self.mu.build_from_intervals(
            52, 'Blues Scale'), [52, 55, 57, 58, 59, 62, 64])
        self.assertEqual(self.mu.build_from_intervals(
            71, 'Minor Seventh'), [71, 74, 78, 81, 83])

        with self.assertRaises(KeyError):
            self.mu.build_from_intervals(50, 'Drojan')

    def test_build_note_list(self):
        """Test Method"""

        self.assertEqual(self.mu.build_note_list(40, 55, ['Ionian'], 'C#'), [
                         [41, 42, 44, 46, 48, 49, 51, 53, 54]])
        self.assertEqual(self.mu.build_note_list(52, 70, ['I7', 'IV7'], 'D'), [
                         [54, 57, 60, 62, 66, 69], [53, 55, 59, 62, 65, 67]])
        self.assertEqual(self.mu.build_note_list(71, 90, ['Minor Pentatonic', 'Major Pentatonic'], 'F'), [
                         [72, 75, 77, 80, 82, 84, 87, 89], [72, 74, 77, 79, 81, 84, 86, 89]])
        self.assertEqual(self.mu.build_note_list(40, 55, ['Major Seventh', 'Minor Seventh', 'Dominant Seventh']), [
                         [40, 44, 47, 51, 52], [40, 43, 47, 50, 52, 55], [40, 44, 47, 50, 52]])
        self.assertEqual(self.mu.build_note_list(83, 100, ['Mixolydian'], 'A#'), [
                         [84, 86, 87, 89, 91, 92, 94, 96, 98, 99]])

    def test_list_of_midi_notes(self):
        """Test Method"""

        self.assertEqual(self.mu.list_of_midi_notes('B', 30, 50), [35, 47])
        self.assertEqual(self.mu.list_of_midi_notes(
            'A#', 42, 90), [46, 58, 70, 82])
        self.assertEqual(self.mu.list_of_midi_notes('G#', 91, 111), [92, 104])
        self.assertEqual(self.mu.list_of_midi_notes('F', 60, 90), [65, 77, 89])
        self.assertEqual(self.mu.list_of_midi_notes(
            'C', 20, 63), [24, 36, 48, 60])
        self.assertEqual(self.mu.list_of_midi_notes('E', 52, 65), [64])
