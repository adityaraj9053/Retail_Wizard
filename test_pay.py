import unittest
import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import os
from unittest.mock import patch, MagicMock
from pay import InvoiceApp


class TestInvoiceApp(unittest.TestCase):
    def setUp(self):
        """Set up the environment before each test."""
        self.root = tk.Tk()
        self.invoice_data = [
            {
                "Product Category": "Beverages",
                "Brand": "Nescafé",
                "Price": 194.0,
                "Discount (%)": 3,
                "Final Price": 188.18
            }
        ]
        self.app = InvoiceApp(self.root, self.invoice_data)

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_phone TEXT,
                total_order_price REAL,
                payment_method TEXT,
                balance_given REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS selected_product (
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
            )
        """)
        cursor.execute(
            "INSERT INTO transactions (customer_name, customer_phone, total_order_price) VALUES (?, ?, ?)",
            ("John Doe", "1234567890", 188.18),
        )
        cursor.execute(
            "INSERT INTO selected_product (sr_no, category, product_name, brand, price, discount, final_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, "Beverages", "Nescafé Coffee Pouch", "Nescafé", 194.0, 3, 188.18),
        )
        conn.commit()
        conn.close()
        
        with open("invoice_data.json", "w", encoding="utf-8") as f:
            json.dump(self.invoice_data, f, indent=4)

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.root.destroy()
        except:
            pass

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM selected_product")
        cursor.execute("DELETE FROM stock_report")
        conn.commit()
        conn.close()
        
        if os.path.exists("invoice_data.json"):
            os.remove("invoice_data.json")
        if os.path.exists("invoice.pdf"):
            os.remove("invoice.pdf")
        if os.path.exists("qr_invoice.png"):
            os.remove("qr_invoice.png")

    def test_initialization(self):
        """Test the initialization of InvoiceApp."""
        self.assertEqual(self.app.root.title(), "Invoice")
        self.assertEqual(self.app.invoice_data, self.invoice_data)
        self.assertAlmostEqual(self.app.total_sum, 188.18, places=2)
        self.assertEqual(
            self.app.sum_entry.get(), f"Rs. {self.app.total_sum:.2f}"
        )

    def test_cancel_invoice(self):
        """Test the cancel_invoice method."""
        with patch.object(self.root, "destroy") as mock_destroy:
            self.app.cancel_invoice()
            mock_destroy.assert_called_once()



    @patch("pay.InvoiceApp.generate_invoice_pdf")
    @patch("pay.messagebox")
    @patch("pay.simpledialog")
    def test_handle_cash_payment_sufficient_amount(
            self, mock_simpledialog, mock_messagebox, mock_generate_invoice_pdf
    ):
        """Test cash payment with sufficient amount."""
        payment_window = tk.Toplevel()
        mock_simpledialog.askfloat.return_value = 200.0

        self.app.handle_cash_payment(payment_window)
        
        mock_messagebox.showinfo.assert_called_with(
            "Payment Successful", "Payment received. Change: Rs. 11"
        )

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payment_method, balance_given FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result, ("Cash", 11.0))

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM selected_product")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)

        with open("invoice_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [])

    @patch("pay.InvoiceApp.generate_invoice_pdf")
    @patch("pay.messagebox")
    def test_handle_upi_payment(self, mock_messagebox, mock_generate_invoice_pdf):
        """Test UPI payment."""
        payment_window = tk.Toplevel()

        self.app.handle_upi_payment(payment_window)

        mock_messagebox.showinfo.assert_called_with(
            "UPI Payment", "Payment received successfully!"
        )

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payment_method, balance_given FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result, ("UPI", 0))
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM selected_product")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)

        with open("invoice_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [])



    @patch("pay.messagebox")
    @patch("pay.simpledialog")
    def test_handle_cash_payment_insufficient_amount(
        self, mock_simpledialog, mock_messagebox
    ):
        """Test cash payment with insufficient amount."""
        payment_window = tk.Toplevel()
        mock_simpledialog.askfloat.return_value = 100.0

        self.app.handle_cash_payment(payment_window)

        mock_messagebox.showerror.assert_called_with(
            "Error", "Insufficient amount given!"
        )
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payment_method, balance_given FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result, (None, None))
        
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM selected_product")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)


    @patch("pay.messagebox")
    @patch("pay.os.startfile")
    def test_generate_invoice_pdf(self, mock_startfile, mock_messagebox):
        """Test PDF generation."""
        self.app.generate_invoice_pdf()

        self.assertTrue(os.path.exists("invoice.pdf"))

        mock_messagebox.showinfo.assert_called_with(
            "Success", "Invoice has been generated as PDF."
        )
        mock_startfile.assert_called_with("invoice.pdf")

    def test_update_transaction(self):
        """Test the update_transaction method."""
        self.app.update_transaction("Cash", 10.0)

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payment_method, balance_given FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result, ("Cash", 10.0))

    def test_reset_selected_product_table(self):
        """Test the reset_selected_product_table method."""
        self.app.reset_selected_product_table()

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sr_no, product_name, quantity FROM stock_report")
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(
            result, (1, "Nescafé Coffee Pouch", 1), "Stock report not updated correctly"
        )
        
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM selected_product")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0, "Selected product table not cleared")

    def test_clear_invoice_data(self):
        """Test the clear_invoice_data method."""
        self.app.clear_invoice_data()

        with open("invoice_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [], "invoice_data.json not cleared")

    @patch("pay.messagebox")
    @patch("pay.simpledialog")
    def test_handle_cash_payment_cancelled(
        self, mock_simpledialog, mock_messagebox
    ):
        """Test cash payment when user cancels input."""
        payment_window = tk.Toplevel()
        mock_simpledialog.askfloat.return_value = None

        self.app.handle_cash_payment(payment_window)

        mock_messagebox.showinfo.assert_not_called()
        mock_messagebox.showerror.assert_not_called()

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payment_method, balance_given FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result, (None, None))


if __name__ == "__main__":
    unittest.main()