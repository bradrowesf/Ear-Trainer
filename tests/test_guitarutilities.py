"""Unit Tests for GuitarUtil class"""
import unittest

from guitarutilities import GuitarUtil


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
