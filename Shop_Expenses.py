import sqlite3
from tkinter import *
from tkinter import messagebox

class ShopExpensesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shop Expenses")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f8ff")

        self.purchase_goods = DoubleVar(self.root)
        self.shop_rent = DoubleVar(self.root)
        self.employee_wages = DoubleVar(self.root)
        self.utilities = DoubleVar(self.root)
        self.pos_subscription = DoubleVar(self.root)
        self.miscellaneous = DoubleVar(self.root)
        self.total_expenses = 0.0
        self.total_sales = 0.0
        self.profit = 0.0
        self.net_profit = 0.0

        title = Label(self.root, text="Shop Expenses & Profit Calculation", font=("Arial", 20, "bold"), bg="#4682b4", fg="white")
        title.pack(side=TOP, fill=X)

        self.create_expense_field("Purchase of Goods (₹):", self.purchase_goods, 60, readonly=True)
        self.create_expense_field("Shop Rent (₹):", self.shop_rent, 100)
        self.create_expense_field("Employee Wages (₹):", self.employee_wages, 140)
        self.create_expense_field("Utilities (₹):", self.utilities, 180)
        self.create_expense_field("POS Software Subscription (₹):", self.pos_subscription, 220)
        self.create_expense_field("Miscellaneous (₹):", self.miscellaneous, 260)

        btn_calculate_expenses = Button(self.root, text="Calculate Expenses", font=("Arial", 14, "bold"), bg="green", fg="white",
                                        command=self.calculate_expenses)
        btn_calculate_expenses.place(x=50, y=320, width=200)

        btn_calculate_profit = Button(self.root, text="Calculate Profit", font=("Arial", 14, "bold"), bg="blue", fg="white",
                                      command=self.calculate_profit)
        btn_calculate_profit.place(x=350, y=320, width=200)

        btn_total_revenue = Button(self.root, text="Total Revenue", font=("Arial", 14, "bold"), bg="orange", fg="white",
                                   command=self.calculate_total_revenue)
        btn_total_revenue.place(x=200, y=370, width=200)

        self.result_frame = Frame(self.root, bg="#e6f7ff", bd=2, relief=RIDGE)
        self.result_frame.place(x=20, y=420, width=560, height=150)

        self.lbl_result_title = Label(self.result_frame, text="Results", font=("Arial", 16, "bold"), bg="#e6f7ff", fg="#333333")
        self.lbl_result_title.pack(pady=5)

        self.lbl_result = Label(self.result_frame, text="", font=("Arial", 14), bg="#e6f7ff", fg="#333333", justify=LEFT)
        self.lbl_result.pack(pady=5)

        self.fetch_and_calculate_purchase_goods()

    def create_expense_field(self, label_text, variable, y_position, readonly=False):
        lbl = Label(self.root, text=label_text, font=("Arial", 14), bg="#f0f8ff")
        lbl.place(x=20, y=y_position)
        txt = Entry(self.root, textvariable=variable, font=("Arial", 14), bg="lightyellow", state="readonly" if readonly else "normal")
        txt.place(x=300, y=y_position, width=250)

    def fetch_and_calculate_purchase_goods(self):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_name TEXT,
                            customer_phone TEXT,
                            total_order_price REAL,
                            payment_method TEXT,
                            balance_given REAL
                        )''')

        cursor.execute("SELECT SUM(total_order_price) FROM transactions")
        self.total_sales = cursor.fetchone()[0] or 0.0
        conn.close()

        purchase_goods_value = self.total_sales * 0.88  
        self.purchase_goods.set(round(purchase_goods_value, 2))

    def calculate_expenses(self):
        self.total_expenses = (
            self.purchase_goods.get() +
            self.shop_rent.get() +
            self.employee_wages.get() +
            self.utilities.get() +
            self.pos_subscription.get() +
            self.miscellaneous.get()
        )
        messagebox.showinfo("Total Expenses", f"Total Expenses: ₹{self.total_expenses:.2f}")

    def calculate_profit(self):
        self.profit = self.total_sales * 0.12  
        self.net_profit = self.profit - (
            self.shop_rent.get() +
            self.employee_wages.get() +
            self.utilities.get() +
            self.pos_subscription.get() +
            self.miscellaneous.get()
        )

        result_text = f"Total Sales: ₹{self.total_sales:.2f}\n" \
                      f"Total Expenses: ₹{self.total_expenses:.2f}\n" \
                      f"Profit (12% Margin): ₹{self.profit:.2f}\n" \
                      f"Net Profit: ₹{self.net_profit:.2f}"
        self.lbl_result.config(text=result_text)

    def calculate_total_revenue(self):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_name TEXT,
                            customer_phone TEXT,
                            total_order_price REAL,
                            payment_method TEXT,
                            balance_given REAL
                        )''')

        cursor.execute("SELECT SUM(total_order_price) FROM transactions")
        total_revenue = cursor.fetchone()[0] or 0.0
        conn.close()

        messagebox.showinfo("Total Revenue", f"Total Revenue: ₹{total_revenue:.2f}")

if __name__ == "__main__":
    root = Tk()
    app = ShopExpensesApp(root)
    root.mainloop()
