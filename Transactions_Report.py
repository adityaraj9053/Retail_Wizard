import tkinter as tk
from tkinter import ttk
import sqlite3

def show_transaction_report():
    report_window = tk.Toplevel()
    report_window.title("Transaction Report")
    report_window.geometry("1200x700")  
    report_window.configure(bg="#f0f0f0") 

    tk.Label(report_window, text="Transaction Report", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    frame = tk.Frame(report_window)
    frame.pack(expand=True, fill="both", padx=20, pady=10)

    tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
    tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")

    columns = ("Transaction ID", "Customer Name", "Phone Number", "Total Order Price", "Payment Method", "Balance Given")
    tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=150)  

    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, customer_name, customer_phone, total_order_price, payment_method, balance_given FROM transactions")
    transactions = cursor.fetchall()
    conn.close()

    for row in transactions:
        tree.insert("", "end", values=row)
    
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x.pack(side="bottom", fill="x")
    tree.pack(expand=True, fill="both")

    close_button = tk.Button(report_window, text="Close", font=("Arial", 12, "bold"), bg="red", fg="white", command=report_window.destroy)
    close_button.pack(pady=10)

root = tk.Tk()
root.withdraw()
show_transaction_report()
root.mainloop()