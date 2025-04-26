
import unittest
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock, ANY
from Product_Catalogue import connect_db, create_table, insert_data, load_file, send_to_main_window


class TestProductCatalogue(unittest.TestCase):
    def setUp(self):
        """Set up the environment before each test."""
  
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS grocery (
            sr_no INTEGER PRIMARY KEY,
            category TEXT,
            product_name TEXT,
            brand TEXT,
            product_code TEXT,
            item_serial_code TEXT,
            quantity TEXT,
            price REAL,
            discount INTEGER,
            final_price REAL,
            stock_available TEXT,
            expiry_date TEXT,
            manufacturing_date TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS selected_product (
            sr_no INTEGER,
            category TEXT,
            product_name TEXT,
            brand TEXT,
            product_code TEXT,
            item_serial_code TEXT,
            quantity TEXT,
            price REAL,
            discount INTEGER,
            final_price REAL,
            stock_available TEXT,
            expiry_date TEXT,
            manufacturing_date TEXT
        )''')
        self.conn.commit()

        global tree, selected_text
        tree = MagicMock()
        tree.get_children.return_value = ["item1"] 
        selected_text = MagicMock()

    def tearDown(self):
        """Clean up after each test."""
        self.conn.close()

    @patch("sqlite3.connect")
    def test_connect_db(self, mock_connect):
        """Test connect_db function."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = connect_db()
        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once_with("grocery.db", timeout=10)

    def test_create_table(self):
        """Test create_table function."""
        create_table()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='grocery'")
        self.assertEqual(self.cursor.fetchone()[0], "grocery")

    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("sqlite3.connect")
    def test_insert_data_success(self, mock_connect, mock_showerror, mock_showinfo):
        """Test insert_data function with successful insertion."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = [(1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", "P001", "S001", "5", 200.0, 10, 180.0, "Yes", "2025-12-31", "2024-12-31")]
        insert_data(data)

        mock_cursor.executemany.assert_called_once_with(
            '''INSERT INTO grocery (sr_no, category, product_name, brand, product_code, item_serial_code, quantity, price, discount, final_price, stock_available, expiry_date, manufacturing_date) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            data
        )
        mock_conn.commit.assert_called_once()
        mock_showinfo.assert_called_once_with("Success", "Data inserted successfully!")
        mock_showerror.assert_not_called()

    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("sqlite3.connect")
    def test_insert_data_error(self, mock_connect, mock_showerror, mock_showinfo):
        """Test insert_data function with error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.executemany.side_effect = sqlite3.IntegrityError("Unique constraint failed")

        data = [(1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", "P001", "S001", "5", 200.0, 10, 180.0, "Yes", "2025-12-31", "2024-12-31")]
        insert_data(data)

        mock_showerror.assert_called_once_with("Error", "Insert failed: Unique constraint failed")
        mock_showinfo.assert_not_called()

    @patch("tkinter.filedialog.askopenfilename")
    @patch("pandas.read_excel")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.ttk.Treeview.insert")
    @patch("tkinter.ttk.Treeview.delete")
    @patch("Product_Catalogue.insert_data")
    def test_load_file_success(self, mock_insert_data, mock_delete, mock_insert, mock_showerror, mock_read_excel, mock_askopenfilename):
        """Test load_file function with successful file load."""
  
        mock_askopenfilename.return_value = "test.xlsx"

        df = pd.DataFrame({
            "sr_no": [1], "category": ["Beverages"], "product_name": ["Nescafé Coffee Pouch"],
            "brand": ["Nescafé"], "product_code": ["P001"], "item_serial_code": ["S001"],
            "quantity": ["5"], "price": [200.0], "discount": [10], "final_price": [180.0],
            "stock_available": ["Yes"], "expiry_date": ["2025-12-31"], "manufacturing_date": ["2024-12-31"]
        })
        mock_read_excel.return_value = df
        global tree
        tree.delete = mock_delete
        tree.insert = mock_insert
        tree.get_children.return_value = ["item1"] 

        load_file()

        mock_askopenfilename.assert_called_once()
        mock_read_excel.assert_called_once_with("test.xlsx")
        mock_delete.assert_called_once_with(["item1"])
        mock_insert.assert_called_once_with("", tk.END, values=df.iloc[0].tolist())
        mock_insert_data.assert_called_once_with(df.values.tolist())
        mock_showerror.assert_not_called()

    @patch("tkinter.filedialog.askopenfilename")
    @patch("tkinter.messagebox.showerror")
    def test_load_file_error(self, mock_showerror, mock_askopenfilename):
        """Test load_file function with file load error."""
     
        mock_askopenfilename.return_value = ""

        global tree
        tree = MagicMock()
        tree.delete = MagicMock()
        tree.insert = MagicMock()
        tree.get_children.return_value = ()

        load_file()

        mock_askopenfilename.assert_called_once()
        mock_showerror.assert_not_called() 

        mock_askopenfilename.return_value = "test.xlsx"
        with patch("pandas.read_excel", side_effect=ValueError("Invalid file")):
            load_file()
            mock_showerror.assert_called_once_with("Error", "Failed to load file: Invalid file")

    @patch("tkinter.ttk.Treeview.selection")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showwarning")
    @patch("tkinter.Text.delete")
    @patch("tkinter.Text.insert")
    @patch("sqlite3.connect")
    def test_send_to_main_window_success(self, mock_connect, mock_insert, mock_delete, mock_showwarning, mock_showerror, mock_showinfo, mock_selection):
        """Test send_to_main_window function with successful send."""
        global tree, selected_text
        tree.selection.return_value = ["item1"]
        tree.item.return_value = {"values": (1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", "P001", "S001", "5", 200.0, 10, 180.0, "Yes", "2025-12-31", "2024-12-31")}
        selected_text.delete = mock_delete
        selected_text.insert = mock_insert

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        send_to_main_window()

        mock_selection.assert_called_once()
        mock_showwarning.assert_not_called()
        mock_delete.assert_called_once_with('1.0', tk.END)
    
        mock_insert.assert_called_once_with(tk.END, str((1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", "P001", "S001", "5", 200.0, 10, 180.0, "Yes", "2025-12-31", "2024-12-31")) + "\n")
        mock_connect.assert_called_once_with("grocery.db", timeout=10)
        mock_cursor.execute.assert_any_call('''CREATE TABLE IF NOT EXISTS selected_product (
            sr_no INTEGER,
            category TEXT,
            product_name TEXT,
            brand TEXT,
            product_code TEXT,
            item_serial_code TEXT,
            quantity TEXT,
            price REAL,
            discount INTEGER,
            final_price REAL,
            stock_available TEXT,
            expiry_date TEXT,
            manufacturing_date TEXT
        )''')
        mock_cursor.executemany.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_showinfo.assert_called_once_with("Success", "Product sent to main window!")
        mock_showerror.assert_not_called()
        print("Insert calls:", mock_insert.call_args_list)

    @patch("tkinter.ttk.Treeview.selection")
    @patch("tkinter.messagebox.showwarning")
    def test_send_to_main_window_no_selection(self, mock_showwarning, mock_selection):
        """Test send_to_main_window function with no selection."""
        global tree, selected_text
        tree = MagicMock()
        selected_text = MagicMock()
        mock_selection.return_value = []

        send_to_main_window()

        mock_selection.assert_called_once()
        mock_showwarning.assert_called_once_with("Warning", "Please select an item to send!")

    @patch("tkinter.ttk.Treeview.selection")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Text.delete")
    @patch("tkinter.Text.insert")
    @patch("sqlite3.connect")
    def test_send_to_main_window_error(self, mock_connect, mock_insert, mock_delete, mock_showerror, mock_selection):
        """Test send_to_main_window function with database error."""
        global tree, selected_text
        tree.selection.return_value = ["item1"]
        tree.item.return_value = {"values": (1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", "P001", "S001", "5", 200.0, 10, 180.0, "Yes", "2025-12-31", "2024-12-31")}
        selected_text.delete = mock_delete
        selected_text.insert = mock_insert
        mock_connect.side_effect = sqlite3.OperationalError("Database locked")

        send_to_main_window()

        mock_showerror.assert_called_once_with("Error", "Failed to send product: Database locked")


if __name__ == "__main__":
    unittest.main()
