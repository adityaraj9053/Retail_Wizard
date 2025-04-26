import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import sqlite3

def connect_db():
    conn = sqlite3.connect("grocery.db", timeout=10)
    return conn

def create_table():
    conn = sqlite3.connect("grocery.db", timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;") 
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS grocery (
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
    conn.commit()
    conn.close()


def insert_data(data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO grocery (sr_no, category, product_name, brand, product_code, item_serial_code, quantity, price, discount, final_price, stock_available, expiry_date, manufacturing_date) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        messagebox.showinfo("Success", "Data inserted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Insert failed: {e}")
    finally:
        conn.close()


def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        tree.delete(*tree.get_children())

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=row.tolist())

        insert_data(df.values.tolist())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")


def send_to_main_window():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select an item to send!")
        return

    selected_data = []
    for item in selected_items:
        row_data = tree.item(item, "values")
        selected_data.append(row_data)

    selected_text.delete('1.0', tk.END)
    for row in selected_data:
        selected_text.insert(tk.END, f"{row}\n")

    conn = None 
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS selected_product (
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

        cursor.executemany("INSERT INTO selected_product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", selected_data)
        conn.commit()
        messagebox.showinfo("Success", "Product sent to main window!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send product: {e}")
    finally:
        if conn is not None:
            conn.close()

# GUI Setup
root = tk.Tk()
root.title("Product Catalogue")
root.geometry("1000x600")
root.configure(bg="#2B2B2B")

tk.Button(root, text="Load Excel File", command=load_file, bg="#00AEEF", fg="white", font=("Arial", 12, "bold"),
          relief="flat").pack(pady=10)

cols = ["Sr No", "Category", "Product Name", "Brand", "Product Code", "Item Serial Code", "Quantity", "Price (₹)",
        "Discount (%)", "Final Price (₹)", "Stock Available", "Expiry Date", "Manufacturing Date"]

frame = tk.Frame(root, bg="#2B2B2B")
frame.pack(expand=True, fill='both')

x_scroll = tk.Scrollbar(frame, orient='horizontal')
y_scroll = tk.Scrollbar(frame, orient='vertical')

tree = ttk.Treeview(frame, columns=cols, show='headings', xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                    style="Custom.Treeview")

x_scroll.config(command=tree.xview)
y_scroll.config(command=tree.yview)

x_scroll.pack(side='bottom', fill='x')
y_scroll.pack(side='right', fill='y')
tree.pack(expand=True, fill='both')

style = ttk.Style()
style.configure("Custom.Treeview", background="#404040", foreground="white", fieldbackground="#404040",
                font=("Arial", 10))
style.configure("Custom.Treeview.Heading", background="yellow", foreground="black", font=("Arial", 11, "bold"))

column_widths = {
    "Sr No": 50,
    "Category": 150,
    "Product Name": 200,
    "Brand": 150,
    "Product Code": 120,
    "Item Serial Code": 150,
    "Quantity": 100,
    "Price (₹)": 80,
    "Discount (%)": 100,
    "Final Price (₹)": 100,
    "Stock Available": 120,
    "Expiry Date": 120,
    "Manufacturing Date": 120
}

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=column_widths.get(col, 100), anchor='center')

tk.Button(root, text="Send to Main Window", command=send_to_main_window, bg="#00AEEF", fg="white",
          font=("Arial", 12, "bold"), relief="flat").pack(pady=10)

selected_text = tk.Text(root, height=5, width=100, bg="#404040", fg="white", font=("Arial", 10))
selected_text.pack(pady=10)

create_table()
root.mainloop()
