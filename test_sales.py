
import unittest
import tkinter as tk
from tkinter import ttk
import sqlite3
from unittest.mock import patch, MagicMock
from Sales import GroceryApp


class TestGroceryApp(unittest.TestCase):
    def setUp(self):
        """Set up the environment before each test."""
        self.root = tk.Tk()
        self.app = GroceryApp(self.root)

        self.root.update()

        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE stock_report (
                sr_no INTEGER,
                product_name TEXT,
                quantity INTEGER,
                sale_date TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE Grocery (
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

        self.cursor.execute(
            "INSERT INTO stock_report (sr_no, product_name, quantity) VALUES (?, ?, ?)",
            (1, "Nescafé Coffee Pouch", 5)
        )
        self.cursor.execute(
            "INSERT INTO Grocery (sr_no, category, product_name, final_price) VALUES (?, ?, ?, ?)",
            (1, "Beverages", "Nescafé Coffee Pouch", 188.18)
        )
        self.conn.commit()

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.root.destroy()
        except:
            pass
        self.conn.close()

    def test_initialization(self):
        """Test the initialization of GroceryApp."""
        self.assertEqual(self.app.root.title(), "Grocery Sales Report")

        geometry = self.app.root.geometry()
        self.assertTrue(geometry.startswith("900x600"), f"Expected geometry to start with '900x600', got {geometry}")
        self.assertIsInstance(self.app.treeview, ttk.Treeview)
        self.assertIsInstance(self.app.revenue_label, tk.Label)
        self.assertIsInstance(self.app.chart_frame, tk.Frame)

    def test_create_header(self):
        """Test the create_header method."""
        header_frame = self.app.root.winfo_children()[0]
        self.assertEqual(header_frame.cget("bg"), "#4CAF50")

        title_label = header_frame.winfo_children()[0]
        self.assertEqual(title_label.cget("text"), "Grocery Sales Dashboard")
        self.assertEqual(title_label.cget("fg"), "white")
        self.assertEqual(title_label.cget("bg"), "#4CAF50")

        buttons = header_frame.winfo_children()[1:3]
        self.assertEqual(buttons[0].cget("text"), "Fetch Data")
        self.assertEqual(buttons[1].cget("text"), "Show Sales Chart")
        self.assertEqual(buttons[0].cget("bg"), "#FFC107")
        self.assertEqual(buttons[1].cget("bg"), "#FFC107")

    def test_create_display_area(self):
        """Test the create_display_area method."""
        show_value = self.app.treeview.cget("show")
        self.assertIn("headings", str(show_value), f"Expected 'headings' in show value, got {show_value}")
        self.assertEqual(
            self.app.treeview.cget("columns"),
            ("Category", "Product", "Units Sold", "Revenue")
        )
        self.assertEqual(
            self.app.treeview.heading("Category", "text"), "Category"
        )
        self.assertEqual(
            self.app.treeview.heading("Product", "text"), "Product"
        )
        self.assertEqual(
            self.app.treeview.heading("Units Sold", "text"), "Units Sold"
        )
        self.assertEqual(
            self.app.treeview.heading("Revenue", "text"), "Revenue"
        )
        
        self.assertEqual(
            self.app.revenue_label.cget("text"), "Total Revenue: ₹0.00"
        )

        self.assertIsInstance(self.app.chart_frame, tk.Frame)

    @patch("Sales.sqlite3.connect")
    def test_fetch_data(self, mock_connect):
        """Test the fetch_data method."""
   
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.side_effect = [
            [("Nescafé Coffee Pouch", 5)]  
        ]
        mock_cursor.fetchone.side_effect = [
            ("Beverages", 188.18)  
        ]

        for row in self.app.treeview.get_children():
            self.app.treeview.delete(row)

        self.app.fetch_data()

        treeview_items = list(self.app.treeview.get_children())
        self.assertEqual(len(treeview_items), 1)
        item_values = self.app.treeview.item(treeview_items[0], "values")
        self.assertEqual(
            item_values,
            ("Beverages", "Nescafé Coffee Pouch", "5", "₹940.90")
        )
    
        self.assertEqual(
            self.app.revenue_label.cget("text"),
            "Total Revenue: ₹940.90"
        )

    @patch("Sales.plt")
    @patch("Sales.FigureCanvasTkAgg")
    def test_plot_sales_chart(self, mock_canvas, mock_plt):
        """Test the plot_sales_chart method."""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        mock_plt.xticks = MagicMock()

        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        mock_canvas_instance.get_tk_widget.return_value = MagicMock()

        category_sales = {"Beverages": 5, "Snacks": 3}
        self.app.plot_sales_chart(category_sales)

        mock_plt.subplots.assert_called_once_with(figsize=(10, 5))
        mock_ax.bar.assert_called_once_with(
            ["Beverages", "Snacks"], [5, 3], color="blue"
        )
        mock_ax.set_xlabel.assert_called_once_with("Product Category")
        mock_ax.set_ylabel.assert_called_once_with("Units Sold")
        mock_ax.set_title.assert_called_once_with(
            "Most Sold Product Categories"
        )
        mock_plt.xticks.assert_called_once_with(rotation=45)

        mock_canvas.assert_called_once_with(mock_fig, master=self.app.chart_frame)
        mock_canvas_instance.draw.assert_called_once()
        mock_canvas_instance.get_tk_widget.return_value.pack.assert_called_once()

    @patch("Sales.plt")
    @patch("Sales.FigureCanvasTkAgg")
    def test_plot_sales_chart_empty(self, mock_canvas, mock_plt):
        """Test plot_sales_chart with no data."""
        self.app.plot_sales_chart(None)
        
        mock_plt.subplots.assert_not_called()
        mock_canvas.assert_not_called()

if __name__ == "__main__":
    unittest.main()
