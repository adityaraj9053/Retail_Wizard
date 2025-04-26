import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
from Stock_Report import generate_stock_report

def show_pnl():
    try:
        subprocess.Popen(["python", "Shop_Expenses.py"])  
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Shop_Expenses.py\n{e}")


def show_stock():
    try:
        subprocess.Popen(["python", "Stock_Report.py"])  
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Transactions_Report.py\n{e}")


def show_transaction():
    try:
        subprocess.Popen(["python", "Transactions_Report.py"]) 
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Transactions_Report.py\n{e}")   

def show_sales():
    try:
        subprocess.Popen(["python", "Sales.py"]) 
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Sales.py\n{e}")


def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Reports Section")
root.geometry("300x300")
root.resizable(False, False)

tk.Label(root, text="Reports", font=("Arial", 12, "bold")).pack(pady=5)

frame = tk.Frame(root)
frame.pack()

button_style = {
    "width": 25,
    "bd": 4,  # Border width
    "relief": "raised",  # 3D effect
    "font": ("Arial", 10, "bold")
}

tk.Button(frame, text="Profit & Loss Report", command=show_pnl, bg="#FF9999", fg="black", **button_style).pack(pady=6)
tk.Button(frame, text="Stock Report", command=show_stock, bg="#99FF99", fg="black", **button_style).pack(pady=6)
tk.Button(frame, text="Transaction Report", command=show_transaction, bg="#9999FF", fg="black", **button_style).pack(pady=6)
tk.Button(frame, text="Sales Report", command=show_sales, bg="#FFFF99", fg="black", **button_style).pack(pady=6)
tk.Button(frame, text="Exit", command=exit_app, bg="red", fg="white", **button_style).pack(pady=6)

root.mainloop()
