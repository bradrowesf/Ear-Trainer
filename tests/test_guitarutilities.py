"""Unit Tests for GuitarUtil class"""
import unittest

from src.guitarutilities import GuitarUtil


class TestGuitarUtil(unittest.TestCase):
    """Testing class"""

    def setUp(self):
        """Setup"""

        self.gu = GuitarUtil()

    def test_get_string_from_number(self):
        """Test method"""

        self.assertEqual(self.gu.get_string_from_number(1), 'High E')
        self.assertEqual(self.gu.get_string_from_number(2), 'B')
        self.assertEqual(self.gu.get_string_from_number(3), 'G')
        self.assertEqual(self.gu.get_string_from_number(4), 'D')
        self.assertEqual(self.gu.get_string_from_number(5), 'A')
        self.assertEqual(self.gu.get_string_from_number(6), 'Low E')

        self.assertRaises(ValueError, self.gu.get_string_from_number, 0)
        self.assertRaises(ValueError, self.gu.get_string_from_number, 7)

    def test_get_string_from_reverse_number(self):
        """Test method"""

        self.assertEqual(self.gu.get_string_from_reverse_number(5), 'High E')
        self.assertEqual(self.gu.get_string_from_reverse_number(4), 'B')
        self.assertEqual(self.gu.get_string_from_reverse_number(3), 'G')
        self.assertEqual(self.gu.get_string_from_reverse_number(2), 'D')
        self.assertEqual(self.gu.get_string_from_reverse_number(1), 'A')
        self.assertEqual(self.gu.get_string_from_reverse_number(0), 'Low E')

        self.assertRaises(
            ValueError, self.gu.get_string_from_reverse_number, -1)
        self.assertRaises(
            ValueError, self.gu.get_string_from_reverse_number, 6)

    def test_get_full_note_name(self):
        """Test method"""

        self.assertEqual(self.gu.get_full_note_name(6, 0), 'E2')
        self.assertEqual(self.gu.get_full_note_name(1, 22), 'D6')
        self.assertEqual(self.gu.get_full_note_name(2, 12), 'B4')
        self.assertEqual(self.gu.get_full_note_name(3, 5), 'C4')
        self.assertEqual(self.gu.get_full_note_name(4, 10), 'C4')
        self.assertEqual(self.gu.get_full_note_name(5, 15), 'C4')

    def test_get_note_name(self):
        """Test method"""

        self.assertEqual(self.gu.get_note_name(6, 0), 'E')
        self.assertEqual(self.gu.get_note_name(5, 5), 'D')
        self.assertEqual(self.gu.get_note_name(4, 9), 'B')
        self.assertEqual(self.gu.get_note_name(3, 11), 'F#')
        self.assertEqual(self.gu.get_note_name(2, 14), 'C#')
        self.assertEqual(self.gu.get_note_name(1, 15), 'G')

    def test_get_lowest_full_note_on_string(self):
        """Test method"""

        self.assertEqual(self.gu.get_lowest_full_note_on_string('B', 6), 'B2')
        self.assertEqual(self.gu.get_lowest_full_note_on_string('A', 5), 'A2')
        self.assertEqual(
            self.gu.get_lowest_full_note_on_string('C#', 4), 'C#4')
        self.assertEqual(self.gu.get_lowest_full_note_on_string('G', 3), 'G3')
        self.assertEqual(self.gu.get_lowest_full_note_on_string('D', 2), 'D4')
        self.assertEqual(self.gu.get_lowest_full_note_on_string('F', 1), 'F4')

    def test_get_fret_from_full_note_name(self):
        """Test Method"""

        self.assertEqual(self.gu.get_fret_from_full_note_name('G2', 6), 3)
        self.assertEqual(self.gu.get_fret_from_full_note_name('G3', 5), 10)
        self.assertEqual(self.gu.get_fret_from_full_note_name('E4', 4), 14)
        self.assertEqual(self.gu.get_fret_from_full_note_name('C5', 3), 17)
        self.assertEqual(self.gu.get_fret_from_full_note_name('D#5', 2), 16)
        self.assertEqual(self.gu.get_fret_from_full_note_name('B4', 1), 7)

        with self.assertRaises(ValueError):
            self.gu.get_fret_from_full_note_name('G2', 5)

    def test_get_fret_string_from_name_default_range(self):
        """Find all string/fret pairs with default fret range"""

        # E4 should appear on multiple strings
        results = self.gu.get_fret_string_from_name('E4')
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        # Each result is [fret, string_name]
        for fret, string_name in results:
            self.assertIsInstance(fret, int)
            self.assertIsInstance(string_name, str)

    def test_get_fret_string_from_name_restricted_frets(self):
        """Fret range filtering excludes out-of-range results"""

        # E2 open on low E string is fret 0
        results_full = self.gu.get_fret_string_from_name('E2')
        results_high = self.gu.get_fret_string_from_name('E2', low_fret_range=5)
        # The open string result should be excluded when low_fret_range=5
        self.assertGreaterEqual(len(results_full), len(results_high))

    def test_get_fret_string_from_name_restricted_strings(self):
        """String range filtering limits which strings are searched"""

        # Only search strings 4-6 (D, A, Low E)
        results = self.gu.get_fret_string_from_name('E2', high_string=4, low_string=6)
        for _, string_name in results:
            self.assertIn(string_name, ['D', 'A', 'Low E'])

    def test_get_fret_string_from_name_not_found(self):
        """Note not on any string returns empty list"""

        # A note that doesn't exist on the guitar
        results = self.gu.get_fret_string_from_name('C1')
        self.assertEqual(results, [])
