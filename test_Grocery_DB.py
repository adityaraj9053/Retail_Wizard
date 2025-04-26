import unittest
from unittest.mock import patch, MagicMock
import Grocery_DB


class TestGroceryDB(unittest.TestCase):

    @patch('Grocery_DB.sqlite3.connect')
    @patch('builtins.print')
    def test_view_database_with_data(self, mock_print, mock_connect):

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [('apple', 10), ('banana', 5)],  # grocery data
            [('id', 'name', 'price')],  # grocery schema
            [('id', 'name')],  # selected_product schema
            [('milk', 2)]  # selected_product data
        ]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        Grocery_DB.view_database()

        self.assertTrue(mock_print.called)
        mock_cursor.execute.assert_any_call("SELECT * FROM grocery")
        mock_cursor.execute.assert_any_call("PRAGMA table_info(grocery);")
        mock_cursor.execute.assert_any_call("PRAGMA table_info(selected_product);")
        mock_cursor.execute.assert_any_call("SELECT * FROM selected_product")




if __name__ == "__main__":
    unittest.main()

