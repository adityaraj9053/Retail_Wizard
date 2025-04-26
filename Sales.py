import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Sales Report")
        self.root.geometry("900x600")

        self.create_header()
        
        self.create_display_area()

    def create_header(self):
        """Creates a header UI with title and action buttons"""
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=60)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="Grocery Sales Dashboard",
                               font=("Helvetica", 20, "bold"), fg="white", bg="#4CAF50")
        title_label.grid(row=0, column=0, padx=20, pady=10)

        action_button1 = tk.Button(header_frame, text="Fetch Data", font=("Helvetica", 12), bg="#FFC107",
                                   command=self.fetch_data)
        action_button1.grid(row=0, column=1, padx=20, pady=10)

        action_button2 = tk.Button(header_frame, text="Show Sales Chart", font=("Helvetica", 12), bg="#FFC107",
                                   command=self.plot_sales_chart)
        action_button2.grid(row=0, column=2, padx=20, pady=10)

    def create_display_area(self):
        """Creates the display area for data and chart"""
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(padx=10, pady=10, fill=tk.X)

        self.treeview = ttk.Treeview(self.tree_frame, columns=("Category", "Product", "Units Sold", "Revenue"),
                                     show="headings")
        self.treeview.heading("Category", text="Category")
        self.treeview.heading("Product", text="Product")
        self.treeview.heading("Units Sold", text="Units Sold")
        self.treeview.heading("Revenue", text="Revenue")
        self.treeview.pack(fill=tk.X)

        self.revenue_label = tk.Label(self.root, text="Total Revenue: ₹0.00", font=("Helvetica", 14, "bold"))
        self.revenue_label.pack(pady=10)

        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(padx=10, pady=10)

    def fetch_data(self):
        """Fetch data from the database and display it."""
        conn = sqlite3.connect('grocery.db')
        cursor = conn.cursor()

        cursor.execute("SELECT product_name, quantity FROM stock_report")
        stock_data = {row[0]: row[1] for row in cursor.fetchall()}

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        total_revenue = 0 
        category_sales = {} 

        for product, units_sold in stock_data.items():
            cursor.execute("SELECT category, final_price FROM Grocery WHERE product_name = ?", (product,))
            result = cursor.fetchone()

            if result:
                category, final_price = result
                revenue = units_sold * final_price
                total_revenue += revenue  
                
                if category in category_sales:
                    category_sales[category] += units_sold
                else:
                    category_sales[category] = units_sold

                self.treeview.insert("", "end", values=(category, product, units_sold, f"₹{revenue:.2f}"))

        conn.close()

        self.revenue_label.config(text=f"Total Revenue: ₹{total_revenue:.2f}")

        self.plot_sales_chart(category_sales)

    def plot_sales_chart(self, category_sales=None):
        """Plots a bar chart of category-wise product sales."""
        if not category_sales:
            return

        categories = list(category_sales.keys())
        units_sold = list(category_sales.values())

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(categories, units_sold, color='blue')
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Units Sold")
        ax.set_title("Most Sold Product Categories")
        plt.xticks(rotation=45)
        
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame) 
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryApp(root)
    root.mainloop()
