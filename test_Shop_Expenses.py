import unittest
from unittest.mock import patch, MagicMock
from Shop_Expenses import ShopExpensesApp
from tkinter import Tk, DoubleVar


class TestShopExpensesApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.app = ShopExpensesApp(self.root)

        self.app.total_expenses = 0.0
        self.app.total_sales = 0.0
        self.app.profit = 0.0
        self.app.net_profit = 0.0

        patcher = patch("Shop_Expenses.messagebox")
        self.mock_messagebox = patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        self.app.root.destroy()

    @patch("sqlite3.connect")
    def test_fetch_and_calculate_purchase_goods(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1000.0,)

        self.app.fetch_and_calculate_purchase_goods()

        expected_purchase = 1000.0 * 0.88
        self.assertEqual(self.app.purchase_goods.get(), round(expected_purchase, 2))
        mock_connect.assert_called_with("grocery.db")
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_cursor.execute.assert_any_call("SELECT SUM(total_order_price) FROM transactions")
        mock_conn.close.assert_called()

        mock_cursor.fetchone.return_value = (None,)
        self.app.fetch_and_calculate_purchase_goods()
        self.assertEqual(self.app.purchase_goods.get(), 0.0)

    def test_calculate_expenses(self):
        self.app.purchase_goods.set(500.0)
        self.app.shop_rent.set(200.0)
        self.app.employee_wages.set(300.0)
        self.app.utilities.set(100.0)
        self.app.pos_subscription.set(50.0)
        self.app.miscellaneous.set(50.0)

        self.app.calculate_expenses()

        expected_total = 500.0 + 200.0 + 300.0 + 100.0 + 50.0 + 50.0
        self.assertEqual(self.app.total_expenses, expected_total)
        self.mock_messagebox.showinfo.assert_called_with("Total Expenses", f"Total Expenses: ₹{expected_total:.2f}")

    def test_calculate_profit(self):
        self.app.total_sales = 1000.0
        self.app.total_expenses = 700.0
        self.app.shop_rent.set(200.0)
        self.app.employee_wages.set(300.0)
        self.app.utilities.set(100.0)
        self.app.pos_subscription.set(50.0)
        self.app.miscellaneous.set(50.0)

        self.app.calculate_profit()

        expected_profit = 1000.0 * 0.12
        expected_net_profit = expected_profit - (200.0 + 300.0 + 100.0 + 50.0 + 50.0)
        result_text = (f"Total Sales: ₹1000.00\n"
                       f"Total Expenses: ₹700.00\n"
                       f"Profit (12% Margin): ₹{expected_profit:.2f}\n"
                       f"Net Profit: ₹{expected_net_profit:.2f}")
        self.assertEqual(self.app.profit, round(expected_profit, 2))
        self.assertEqual(self.app.net_profit, round(expected_net_profit, 2))
        self.assertEqual(self.app.lbl_result.cget("text"), result_text)

    @patch("sqlite3.connect")
    def test_calculate_total_revenue(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1500.0,)

        self.app.calculate_total_revenue()

        mock_connect.assert_called_with("grocery.db")
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_cursor.execute.assert_any_call("SELECT SUM(total_order_price) FROM transactions")
        self.mock_messagebox.showinfo.assert_called_with("Total Revenue", "Total Revenue: ₹1500.00")
        mock_conn.close.assert_called()

        mock_cursor.fetchone.return_value = (None,)
        self.app.calculate_total_revenue()
        self.mock_messagebox.showinfo.assert_called_with("Total Revenue", "Total Revenue: ₹0.00")

    def test_create_expense_field(self):
        var = DoubleVar()
        self.app.create_expense_field("Test Label", var, 50)
        var.set(100.0)
        self.assertEqual(var.get(), 100.0)

    def test_init(self):
        root = Tk()
        root.withdraw()
        app = ShopExpensesApp(root)
        self.assertIsInstance(app.root, Tk)
        root.update()
        self.assertTrue(app.root.geometry().startswith("600x600"))
        root.destroy()


if __name__ == "__main__":
    unittest.main()