import unittest

from guitarutilities import GuitarUtil


class test_GuitarUtil(unittest.TestCase):

    def setUp(self):

        self.gu = GuitarUtil()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_string_from_number(self):

        self.assertEqual(self.gu.get_string_from_number(1), 'High E')
        self.assertEqual(self.gu.get_string_from_number(2), 'B')
        self.assertEqual(self.gu.get_string_from_number(3), 'G')
        self.assertEqual(self.gu.get_string_from_number(4), 'D')
        self.assertEqual(self.gu.get_string_from_number(5), 'A')
        self.assertEqual(self.gu.get_string_from_number(6), 'Low E')

        self.assertRaises(ValueError, self.gu.get_string_from_number, 0)
        self.assertRaises(ValueError, self.gu.get_string_from_number, 7)

    def test_get_string_from_reverse_number(self):

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

        self.assertEqual(self.gu.get_full_note_name(6, 0), 'E2')
        self.assertEqual(self.gu.get_full_note_name(1, 22), 'D6')
        self.assertEqual(self.gu.get_full_note_name(2, 12), 'B4')
        self.assertEqual(self.gu.get_full_note_name(3, 5), 'C4')
        self.assertEqual(self.gu.get_full_note_name(4, 10), 'C4')
        self.assertEqual(self.gu.get_full_note_name(5, 15), 'C4')
