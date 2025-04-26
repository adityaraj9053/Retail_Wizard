import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox 

STOCK_THRESHOLD = 2  

def generate_stock_report():
   
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(grocery)")
    columns = [col[1] for col in cursor.fetchall()]

    if "sr_no" in columns and "product_name" in columns and "quantity" in columns:
        cursor.execute("SELECT sr_no, product_name, CAST(quantity AS INTEGER) FROM grocery")
    else:
        conn.close()
        return "Error: Column names might be incorrect in grocery table. Check the database schema."

    grocery_stock = {row[0]: {'name': row[1], 'quantity': row[2]} for row in cursor.fetchall()}

    cursor.execute("PRAGMA table_info(stock_report)")
    stock_columns = [col[1] for col in cursor.fetchall()]

    if "sr_no" in stock_columns:
        cursor.execute("SELECT sr_no, SUM(quantity) FROM stock_report GROUP BY sr_no")
    else:
        conn.close()
        return "Error: Column names might be incorrect in stock_report table."

    stock_data = cursor.fetchall()

    for product_id, sold_quantity in stock_data:
        if product_id in grocery_stock:
            grocery_stock[product_id]['quantity'] -= sold_quantity

    conn.close()
    return grocery_stock


def check_stock_alerts(grocery_stock):
    low_stock_items = [f"{data['name']} (Stock Left: {data['quantity']})"
                       for product_id, data in grocery_stock.items() if data['quantity'] < STOCK_THRESHOLD]

    if low_stock_items:
        alert_message = "⚠️ Low Stock Alert!\n\n" + "\n".join(low_stock_items)
        messagebox.showwarning("Stock Alert", alert_message)

def display_stock_report():

    grocery_stock = generate_stock_report()

    if isinstance(grocery_stock, str): 
        print(grocery_stock)
        return
 
    stock_window = tk.Tk()
    stock_window.title("Stock Report")
    stock_window.geometry("600x400")

    header_frame = tk.Frame(stock_window)
    header_frame.pack(fill=tk.X, padx=10, pady=10)

    title_label = tk.Label(header_frame, text="Stock Report", font=("Arial", 16, "bold"), fg="white", bg="#4CAF50", anchor="w", padx=10)
    title_label.pack(fill=tk.X, pady=5)

    treeview_frame = tk.Frame(stock_window)
    treeview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Product ID", "Product Name", "Stock Left")
    tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", height=15)

    tree.heading("Product ID", text="Product ID", anchor="w")
    tree.heading("Product Name", text="Product Name", anchor="w")
    tree.heading("Stock Left", text="Stock Left", anchor="w")

    tree.column("Product ID", width=100, anchor="center")
    tree.column("Product Name", width=200, anchor="w")
    tree.column("Stock Left", width=100, anchor="center")

    for product_id, data in grocery_stock.items():
        tree.insert("", tk.END, values=(product_id, data['name'], data['quantity']))

    scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    tree.pack(fill=tk.BOTH, expand=True)

    check_stock_alerts(grocery_stock)

    stock_window.mainloop()

if __name__ == "__main__":
    display_stock_report()
