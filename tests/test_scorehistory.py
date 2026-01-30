"""Unit Tests for ScoreHistory class"""
import unittest
from unittest.mock import patch, mock_open, MagicMock, call

from src.scorehistory import ScoreHistory


class TestScoreHistoryAppend(unittest.TestCase):
    """Tests for append_to_history()"""

    @patch('builtins.print')
    @patch('src.scorehistory.time.time', return_value=1000.0)
    @patch('src.scorehistory.csv.writer')
    @patch('builtins.open', new_callable=mock_open)
    def test_append_writes_correct_rows(self, m_open, m_writer, m_time, m_print):
        """Correct CSV rows written with timestamp"""
        mock_csv = MagicMock()
        m_writer.return_value = mock_csv

        sh = ScoreHistory()
        scores = {"test:m3": 3.5, "test:P5": 5.0}
        sh.append_to_history(scores)

        m_open.assert_called_once_with(
            ScoreHistory.HISTORY_FILENAME, 'a', newline='', encoding="utf-8")
        mock_csv.writerows.assert_called_once_with([
            ["test:m3", 3.5, 1000.0],
            ["test:P5", 5.0, 1000.0],
        ])

    @patch('builtins.print')
    @patch('src.scorehistory.time.time', return_value=2000.0)
    @patch('src.scorehistory.csv.writer')
    @patch('builtins.open', new_callable=mock_open)
    def test_append_empty_dict(self, m_open, m_writer, m_time, m_print):
        """Empty dict still opens file but writes empty list"""
        mock_csv = MagicMock()
        m_writer.return_value = mock_csv

        sh = ScoreHistory()
        sh.append_to_history({})

        mock_csv.writerows.assert_called_once_with([])


class TestScoreHistoryGetDataframe(unittest.TestCase):
    """Tests for get_dataframe()"""

    @patch('src.scorehistory.pd.read_csv')
    def test_get_dataframe_calls_read_csv(self, m_read_csv):
        """get_dataframe passes the right filename and header=None"""
        m_read_csv.return_value = MagicMock()

        sh = ScoreHistory()
        sh.get_dataframe()

        m_read_csv.assert_called_once_with(
            ScoreHistory.HISTORY_FILENAME, header=None)

    @patch('src.scorehistory.pd.read_csv')
    def test_get_dataframe_returns_result(self, m_read_csv):
        """get_dataframe returns what read_csv returns"""
        sentinel = MagicMock()
        m_read_csv.return_value = sentinel

        sh = ScoreHistory()
        result = sh.get_dataframe()
        self.assertIs(result, sentinel)
