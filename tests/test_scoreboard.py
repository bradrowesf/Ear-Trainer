"""Unit Tests for Scoreboard class"""
import json
import unittest
from copy import deepcopy
from unittest.mock import patch, mock_open, MagicMock

from src.scoreboard import Scoreboard


class TestScoreboardAppendScore(unittest.TestCase):
    """Tests for append_score()"""

    def setUp(self):
        self.sb = Scoreboard()

    def test_append_creates_entry(self):
        """First append creates a new key with a one-element list"""
        self.sb.append_score("test", "elem", 5.0)
        key = self.sb.get_test_prefix("test", "elem")
        self.assertEqual(self.sb.active_scores[key], [5.0])

    def test_append_to_existing(self):
        """Subsequent appends grow the list"""
        self.sb.append_score("test", "elem", 3.0)
        self.sb.append_score("test", "elem", 4.0)
        key = self.sb.get_test_prefix("test", "elem")
        self.assertEqual(self.sb.active_scores[key], [3.0, 4.0])

    def test_append_caps_at_30(self):
        """List never exceeds 30 entries"""
        for i in range(35):
            self.sb.append_score("test", "elem", float(i % 20))
        key = self.sb.get_test_prefix("test", "elem")
        self.assertEqual(len(self.sb.active_scores[key]), 30)

    def test_append_caps_drops_oldest(self):
        """When capped, the oldest score is removed"""
        for i in range(31):
            self.sb.append_score("test", "elem", float(i % 20))
        key = self.sb.get_test_prefix("test", "elem")
        # First score (0.0) should have been popped; second (1.0) is now first
        self.assertEqual(self.sb.active_scores[key][0], 1.0)

    def test_append_type_error_for_non_float(self):
        """Non-float value raises TypeError"""
        with self.assertRaises(TypeError):
            self.sb.append_score("test", "elem", 5)

    def test_append_index_error_for_negative(self):
        """Negative value raises IndexError"""
        with self.assertRaises(IndexError):
            self.sb.append_score("test", "elem", -1.0)

    def test_append_index_error_for_over_20(self):
        """Value > 20 raises IndexError"""
        with self.assertRaises(IndexError):
            self.sb.append_score("test", "elem", 20.1)

    def test_append_boundary_zero(self):
        """0.0 is a valid score"""
        self.sb.append_score("test", "elem", 0.0)
        key = self.sb.get_test_prefix("test", "elem")
        self.assertEqual(self.sb.active_scores[key], [0.0])

    def test_append_boundary_twenty(self):
        """20.0 is a valid score"""
        self.sb.append_score("test", "elem", 20.0)
        key = self.sb.get_test_prefix("test", "elem")
        self.assertEqual(self.sb.active_scores[key], [20.0])


class TestScoreboardGetScores(unittest.TestCase):
    """Tests for score retrieval methods"""

    def setUp(self):
        self.sb = Scoreboard()

    def test_get_raw_element_score_average(self):
        """Returns the average of stored scores"""
        self.sb.append_score("t", "e", 4.0)
        self.sb.append_score("t", "e", 6.0)
        key = self.sb.get_test_prefix("t", "e")
        self.assertAlmostEqual(self.sb.get_raw_element_score(key), 5.0)

    def test_get_raw_element_score_missing_key(self):
        """Returns 20 for a missing key"""
        self.assertEqual(self.sb.get_raw_element_score("missing"), 20)

    def test_get_persistent_raw_element_score_missing_key(self):
        """Returns 20 for a missing persistent key"""
        self.assertEqual(self.sb.get_persistent_raw_element_score("missing"), 20)

    def test_get_adjusted_element_score_insufficient_trials(self):
        """Returns 20 when fewer than 5 trials exist"""
        self.sb.append_score("t", "e", 3.0)
        self.sb.append_score("t", "e", 3.0)
        key = self.sb.get_test_prefix("t", "e")
        self.assertEqual(self.sb.get_adjusted_element_score(key), 20)

    def test_get_adjusted_element_score_sufficient_trials(self):
        """Returns average when 5+ trials exist"""
        for _ in range(5):
            self.sb.append_score("t", "e", 4.0)
        key = self.sb.get_test_prefix("t", "e")
        self.assertAlmostEqual(self.sb.get_adjusted_element_score(key), 4.0)

    def test_get_adjusted_element_score_missing_key(self):
        """Returns 20 for a missing key"""
        self.assertEqual(self.sb.get_adjusted_element_score("missing"), 20)


class TestScoreboardGetTestPrefix(unittest.TestCase):
    """Tests for get_test_prefix()"""

    def test_key_concatenation(self):
        """Key is name:element"""
        sb = Scoreboard()
        self.assertEqual(sb.get_test_prefix("MyTest", "m3"), "MyTest:m3")


class TestScoreboardFileIO(unittest.TestCase):
    """Tests for open() and save()"""

    def test_open_loads_json(self):
        """open() loads JSON into both active and persistent scores"""
        data = {"key1": [1.0, 2.0], "key2": [3.0]}
        json_str = json.dumps(data)

        sb = Scoreboard()
        with patch("builtins.open", mock_open(read_data=json_str)):
            sb.open()

        self.assertEqual(sb.active_scores, data)
        self.assertEqual(sb.persistent_scores, data)

    def test_open_deep_copies(self):
        """active_scores and persistent_scores are independent after open"""
        data = {"key1": [1.0, 2.0]}
        json_str = json.dumps(data)

        sb = Scoreboard()
        with patch("builtins.open", mock_open(read_data=json_str)):
            sb.open()

        # Mutating active shouldn't affect persistent
        sb.active_scores["key1"].append(9.0)
        self.assertNotEqual(sb.active_scores["key1"], sb.persistent_scores["key1"])

    def test_open_file_not_found(self):
        """FileNotFoundError is handled silently"""
        sb = Scoreboard()
        with patch("builtins.open", side_effect=FileNotFoundError):
            sb.open()  # should not raise

        self.assertEqual(sb.active_scores, {})

    def test_save_writes_json(self):
        """save() writes active_scores as JSON"""
        sb = Scoreboard()
        sb.active_scores = {"key": [1.0, 2.0]}

        m = mock_open()
        with patch("builtins.open", m):
            sb.save()

        m.assert_called_once_with('scores.json', 'w', encoding="utf-8")
        written = ''.join(
            call.args[0] for call in m().write.call_args_list)
        self.assertEqual(json.loads(written), {"key": [1.0, 2.0]})


class TestScoreboardOutputScores(unittest.TestCase):
    """Tests for output_scores()"""

    def setUp(self):
        self.sb = Scoreboard()

    @patch('src.scoreboard.ScoreHistory')
    @patch('builtins.print')
    def test_output_promotion(self, mock_print, mock_sh_class):
        """Scores below 3.5 show promotion candidate"""
        for _ in range(5):
            self.sb.append_score("Test", "m3", 2.0)
        # Also set persistent scores for delta calculation
        self.sb.persistent_scores = deepcopy(self.sb.active_scores)

        self.sb.output_scores("Test", ["m3"])

        # Check that "Promotion Candidate" appeared in some print call
        printed_text = ' '.join(
            str(call) for call in mock_print.call_args_list)
        self.assertIn("Promotion Candidate", printed_text)

    @patch('src.scoreboard.ScoreHistory')
    @patch('builtins.print')
    def test_output_demotion(self, mock_print, mock_sh_class):
        """Scores above 7.5 show demotion candidate"""
        for _ in range(5):
            self.sb.append_score("Test", "m3", 10.0)
        self.sb.persistent_scores = deepcopy(self.sb.active_scores)

        self.sb.output_scores("Test", ["m3"])

        printed_text = ' '.join(
            str(call) for call in mock_print.call_args_list)
        self.assertIn("Demotion Candidate", printed_text)

    @patch('src.scoreboard.ScoreHistory')
    @patch('builtins.print')
    def test_output_sorted_descending(self, mock_print, mock_sh_class):
        """Output is sorted by score descending"""
        self.sb.append_score("Test", "high", 10.0)
        self.sb.append_score("Test", "low", 2.0)
        self.sb.persistent_scores = deepcopy(self.sb.active_scores)

        self.sb.output_scores("Test", ["high", "low"])

        # Find the score print calls (those containing the test key)
        score_lines = []
        for call in mock_print.call_args_list:
            line = str(call)
            if "Test:" in line:
                score_lines.append(line)

        # "high" (10.0) should come before "low" (2.0) in descending order
        self.assertEqual(len(score_lines), 2)
        self.assertIn("high", score_lines[0])
        self.assertIn("low", score_lines[1])


class TestScoreboardStr(unittest.TestCase):
    """Tests for __str__()"""

    def test_str_representation(self):
        """__str__ returns string of active_scores dict"""
        sb = Scoreboard()
        sb.active_scores = {"a": [1.0]}
        self.assertEqual(str(sb), str({"a": [1.0]}))
