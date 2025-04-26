import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import messagebox
from Main_Window import RetailWizardApp 

class TestRetailWizardApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = RetailWizardApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("sqlite3.connect")
    def test_show_selected_data_empty(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_connect.return_value.cursor.return_value = mock_cursor

        with patch.object(messagebox, "showinfo") as mock_showinfo:
            self.app.show_selected_data()
            mock_showinfo.assert_called_with("Info", "No data available.")


    @patch("sqlite3.connect")
    def test_delete_selected_product(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_tree = MagicMock()
        mock_tree.selection.return_value = [1]  
        mock_tree.item.return_value = {"values": [1, "Category", "Product", "Brand", "P001", "S001", 5, 100.0, 10, 90.0, 50, "2025-12-31", "2025-01-01"]}

        with patch.object(messagebox, "askyesno", return_value=True):
            with patch.object(messagebox, "showinfo") as mock_showinfo:
                self.app.delete_selected_product(mock_tree)
                mock_showinfo.assert_called_with("Info", "Product(s) deleted successfully.")

    @patch("sqlite3.connect")
    def test_checkout(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = [1000.0] 
        self.app.var_name.set("John Doe")
        self.app.var_contact.set("1234567890")

        with patch("json.dump") as mock_json_dump:
            self.app.checkout()
            mock_json_dump.assert_called_once()
            mock_cursor.execute.assert_any_call("SELECT SUM(final_price) FROM selected_product")

    @patch("sqlite3.connect")
    def test_checkout_missing_customer_details(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        self.app.var_name.set("") 
        self.app.var_contact.set("1234567890")

        with patch.object(messagebox, "showwarning") as mock_showwarning:
            self.app.checkout()
            mock_showwarning.assert_called_with("Warning", "Please enter customer name and phone number.")

if __name__ == "__main__":
    unittest.main()
