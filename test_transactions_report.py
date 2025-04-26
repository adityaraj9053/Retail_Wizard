import unittest
from unittest.mock import patch, MagicMock
from Transactions_Report import show_transaction_report
import pytest
class TestMinimal(unittest.TestCase):
    @patch("tkinter.Tk")
    @patch("tkinter.Toplevel")
    def test_minimal(self, mock_toplevel, mock_tk):
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_root.mainloop = MagicMock()
        show_transaction_report()
        mock_root.mainloop.assert_not_called()

if __name__ == "__main__":
    unittest.main(verbosity=2)