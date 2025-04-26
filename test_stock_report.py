
import unittest
import tkinter as tk
from tkinter import ttk
import sqlite3
from unittest.mock import patch, MagicMock, ANY
from Stock_Report import generate_stock_report, check_stock_alerts, display_stock_report, STOCK_THRESHOLD


class TestStockReport(unittest.TestCase):
    def setUp(self):
        """Set up the environment before each test."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE grocery (
                sr_no INTEGER,
                product_name TEXT,
                quantity INTEGER,
                category TEXT,
                brand TEXT,
                price REAL,
                discount INTEGER,
                final_price REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE stock_report (
                sr_no INTEGER,
                product_name TEXT,
                quantity INTEGER,
                sale_date TIMESTAMP
            )
        """)

        self.cursor.execute(
            "INSERT INTO grocery (sr_no, product_name, quantity) VALUES (?, ?, ?)",
            (1, "Nescafé Coffee Pouch", 10)
        )
        self.cursor.execute(
            "INSERT INTO grocery (sr_no, product_name, quantity) VALUES (?, ?, ?)",
            (2, "Chips", 1)
        )
        self.cursor.execute(
            "INSERT INTO stock_report (sr_no, product_name, quantity) VALUES (?, ?, ?)",
            (1, "Nescafé Coffee Pouch", 3)
        )
        self.conn.commit()

    def tearDown(self):
        """Clean up after each test."""
        self.conn.close()

    def test_generate_stock_report_success(self):
        """Test generate_stock_report with valid database schema."""
        with patch("Stock_Report.sqlite3.connect") as mock_connect:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            mock_cursor.fetchall.side_effect = [
                [(0, "sr_no"), (1, "product_name"), (2, "quantity")],  # grocery columns
                [(1, "Nescafé Coffee Pouch", 10), (2, "Chips", 1)],    # grocery data
                [(0, "sr_no"), (1, "product_name"), (2, "quantity")],  # stock_report columns
                [(1, 3)]                                               # stock_report data
            ]

            result = generate_stock_report()

            expected = {
                1: {"name": "Nescafé Coffee Pouch", "quantity": 7},  # 10 - 3
                2: {"name": "Chips", "quantity": 1}
            }
            self.assertEqual(result, expected)
            mock_conn.close.assert_called_once()

    def test_generate_stock_report_invalid_grocery_schema(self):
        """Test generate_stock_report with invalid grocery table schema."""
        with patch("Stock_Report.sqlite3.connect") as mock_connect:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            mock_cursor.fetchall.return_value = [(0, "id"), (1, "name")]

            result = generate_stock_report()

            self.assertEqual(
                result,
                "Error: Column names might be incorrect in grocery table. Check the database schema."
            )
            mock_conn.close.assert_called_once()

    def test_generate_stock_report_invalid_stock_report_schema(self):
        """Test generate_stock_report with invalid stock_report table schema."""
        with patch("Stock_Report.sqlite3.connect") as mock_connect:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            mock_cursor.fetchall.side_effect = [
                [(0, "sr_no"), (1, "product_name"), (2, "quantity")], 
                [(1, "Nescafé Coffee Pouch", 10)],                    
                [(0, "id"), (1, "name")]                               
            ]

            result = generate_stock_report()

            self.assertEqual(
                result,
                "Error: Column names might be incorrect in stock_report table."
            )
            mock_conn.close.assert_called_once()

    def test_check_stock_alerts_low_stock(self):
        """Test check_stock_alerts with low stock items."""
        grocery_stock = {
            1: {"name": "Nescafé Coffee Pouch", "quantity": 1},
            2: {"name": "Chips", "quantity": 5}
        }
        with patch("Stock_Report.messagebox") as mock_messagebox:
            check_stock_alerts(grocery_stock)

            expected_message = (
                "⚠️ Low Stock Alert!\n\n"
                "Nescafé Coffee Pouch (Stock Left: 1)"
            )
            mock_messagebox.showwarning.assert_called_once_with(
                "Stock Alert",
                expected_message
            )

    def test_check_stock_alerts_no_low_stock(self):
        """Test check_stock_alerts with no low stock items."""
        grocery_stock = {
            1: {"name": "Nescafé Coffee Pouch", "quantity": 5},
            2: {"name": "Chips", "quantity": 3}
        }
        with patch("Stock_Report.messagebox") as mock_messagebox:
            check_stock_alerts(grocery_stock)

            mock_messagebox.showwarning.assert_not_called()

    @patch("Stock_Report.messagebox")
    @patch("Stock_Report.ttk.Treeview")
    @patch("Stock_Report.ttk.Scrollbar")
    @patch("Stock_Report.tk.Tk")
    def test_display_stock_report(self, mock_tk, mock_scrollbar, mock_treeview, mock_messagebox):
        """Test display_stock_report with valid stock data."""
        with patch("Stock_Report.generate_stock_report") as mock_generate:
            mock_generate.return_value = {
                1: {"name": "Nescafé Coffee Pouch", "quantity": 7},
                2: {"name": "Chips", "quantity": 1}
            }
            mock_window = MagicMock()
            mock_tk.return_value = mock_window
            mock_tree = MagicMock()
            mock_treeview.return_value = mock_tree
            mock_scroll = MagicMock()
            mock_scrollbar.return_value = mock_scroll

            display_stock_report()

            mock_window.title.assert_called_once_with("Stock Report")
            mock_window.geometry.assert_called_once_with("600x400")

            mock_treeview.assert_called_once_with(
                ANY, 
                columns=("Product ID", "Product Name", "Stock Left"),
                show="headings",
                height=15
            )
            mock_tree.heading.assert_any_call("Product ID", text="Product ID", anchor="w")
            mock_tree.heading.assert_any_call("Product Name", text="Product Name", anchor="w")
            mock_tree.heading.assert_any_call("Stock Left", text="Stock Left", anchor="w")
            mock_tree.column.assert_any_call("Product ID", width=100, anchor="center")
            mock_tree.column.assert_any_call("Product Name", width=200, anchor="w")
            mock_tree.column.assert_any_call("Stock Left", width=100, anchor="center")

            mock_tree.insert.assert_any_call(
                "", tk.END, values=(1, "Nescafé Coffee Pouch", 7)
            )
            mock_tree.insert.assert_any_call(
                "", tk.END, values=(2, "Chips", 1)
            )
            mock_scrollbar.assert_called_once_with(
                ANY, 
                orient="vertical",
                command=mock_tree.yview
            )
            mock_scroll.pack.assert_called_once_with(side="right", fill="y")
            mock_tree.configure.assert_called_once_with(yscrollcommand=mock_scroll.set)

            mock_messagebox.showwarning.assert_called_once_with(
                "Stock Alert",
                "⚠️ Low Stock Alert!\n\nChips (Stock Left: 1)"
            )

            mock_window.mainloop.assert_called_once()

    @patch("Stock_Report.generate_stock_report")
    def test_display_stock_report_error(self, mock_generate):
        """Test display_stock_report with error from generate_stock_report."""
        mock_generate.return_value = "Error: Invalid schema"

        with patch("builtins.print") as mock_print:
            display_stock_report()

            mock_print.assert_called_once_with("Error: Invalid schema")

if __name__ == "__main__":
    unittest.main()
