import tkinter as tk
from tkinter import *

from tkinter import ttk, messagebox
import pandas as pd
import subprocess
import sqlite3
import tkinter.font as tkfont
import subprocess
import sys
import os
import json
class RetailWizardApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Retail Wizard")
        self.root.config(bg="black")
        self.root.state("zoomed") 
        self.var_search = StringVar()
        self.var_Category = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        self.var_cal_input = StringVar()
        self.SrNo = StringVar()
        self.Category = StringVar()
        self.ProductCategory = StringVar()
        self.Brand = StringVar()
        self.ProductCode = StringVar()
        self.ItemSerialCode = StringVar()
        self.Quantity = StringVar()
        self.Price = StringVar()
        self.Discount = StringVar()
        self.FinalPrice = StringVar()
        self.StockAvailable = StringVar()
        self.ExpiryDate = StringVar()
        self.ManufacturingDate = StringVar()

        def open_product_catalogue():
            subprocess.Popen(["python", "Product_Catalogue.py"])

        def open_reports():
            subprocess.Popen(["python", "Reports.py"])


        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="Black")
        CustomerFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)


        lbl_Name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="Black", fg="White").place(x=5, y=37)
        txt_Name = Entry(CustomerFrame, textvariable=self.var_name, font=("times new roman", 13),bg="lightyellow").place(x=68, y=37, width=150, height=22)


        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="Black", fg="White").place(x=260,y=37)

        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13),bg="lightyellow").place(x=380, y=37, width=110, height=22)

        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="Black")
        Cal_Cart_Frame.place(relx=0, rely=0.1, relwidth=1, relheight=1)

        Cal_Frame = Frame(Cal_Cart_Frame, bd=2, relief=RIDGE, bg="Black")
        Cal_Frame.place(relx=0, rely=0.018, relwidth=0.2, relheight=1.0)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10, relief=GROOVE)
        txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(Cal_Frame, text="7", font=('arial', 15, 'bold'), command = lambda:self.get_input(7), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=0)
        btn_8 = Button(Cal_Frame, text="8", font=('arial', 15, 'bold'), command = lambda:self.get_input(8), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=1)
        btn_9 = Button(Cal_Frame, text="9", font=('arial', 15, 'bold'), command = lambda:self.get_input(9), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=2)
        btn_sum = Button(Cal_Frame, text="+", font=('arial', 15, 'bold'), command = lambda:self.get_input('+'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=3)

        btn_4 = Button(Cal_Frame, text="4", font=('arial', 15, 'bold'), command = lambda:self.get_input(4), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=0)
        btn_5 = Button(Cal_Frame, text="5", font=('arial', 15, 'bold'), command = lambda:self.get_input(5), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=1)
        btn_6 = Button(Cal_Frame, text="6", font=('arial', 15, 'bold'), command = lambda:self.get_input(6), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=2)
        btn_sub = Button(Cal_Frame, text="-", font=('arial', 15, 'bold'), command = lambda:self.get_input('-'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=3)

        btn_1 = Button(Cal_Frame, text="1", font=('arial', 15, 'bold'), command = lambda:self.get_input(1), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=0)
        btn_2 = Button(Cal_Frame, text="2", font=('arial', 15, 'bold'), command = lambda:self.get_input(2), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=1)
        btn_3 = Button(Cal_Frame, text="3", font=('arial', 15, 'bold'), command = lambda:self.get_input(3), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=2)
        btn_mul = Button(Cal_Frame, text="*", font=('arial', 15, 'bold'), command = lambda:self.get_input('*'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=3)

        btn_0 = Button(Cal_Frame, text="0", font=('arial', 15, 'bold'), command = lambda:self.get_input(0), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=4, column=0)
        btn_clear = Button(Cal_Frame, text="C", font=('arial', 15, 'bold'), command = self.clear_cal, bd=5, width=4, pady=10,
                           cursor="hand2").grid(row=4, column=1)
        btn_equal = Button(Cal_Frame, text="=", font=('arial', 15, 'bold'), command = self.perform_cal, bd=5, width=4, pady=10,
                           cursor="hand2").grid(row=4, column=2)
        btn_div = Button(Cal_Frame, text="/", font=('arial', 15, 'bold'), command = lambda:self.get_input('/'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=4, column=3)

        self.cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        self.cart_Frame.place(relx=0.2, rely=0.018, relwidth=0.8, relheight=0.84)

        cartTitle = Label(self.cart_Frame, text="Shopping Cart", font=("goudy old style", 15), bg="lightgray")
        cartTitle.pack()

        scrolly = Scrollbar(self.cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(
            self.cart_Frame,
            columns=("Sr No", "Category", "Product Category", "Brand", "Product Code",
                     "Item Serial Code", "Quantity", "Price (₹)", "Discount (%)",
                     "Final Price (₹)", "Stock Available", "Expiry Date", "Manufacturing Date"), show='headings',
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        self.CartTable.heading("Sr No", text="Sr No.")
        self.CartTable.heading("Category", text="Category")
        self.CartTable.heading("Product Category", text="Product Category")
        self.CartTable.heading("Brand", text="Brand")
        self.CartTable.heading("Product Code", text="Product Code")
        self.CartTable.heading("Item Serial Code", text="Item Serial Code")
        self.CartTable.heading("Quantity", text="Quantity")
        self.CartTable.heading("Price (₹)", text="Price (₹)")
        self.CartTable.heading("Discount (%)", text="Discount (%)")
        self.CartTable.heading("Final Price (₹)", text="Final Price (₹)")
        self.CartTable.heading("Stock Available", text="Stock Available")
        self.CartTable.heading("Expiry Date", text="Expiry Date")
        self.CartTable.heading("Manufacturing Date", text="Manufacturing Date")

        self.CartTable["show"] = "headings"

        self.CartTable.column("Sr No", width=120)
        self.CartTable.column("Category", width=150)
        self.CartTable.column("Product Category", width=150)
        self.CartTable.column("Brand", width=150)
        self.CartTable.column("Product Code", width=150)
        self.CartTable.column("Item Serial Code", width=150)
        self.CartTable.column("Quantity", width=100)
        self.CartTable.column("Price (₹)", width=120)
        self.CartTable.column("Discount (%)", width=120)
        self.CartTable.column("Final Price (₹)", width=150)
        self.CartTable.column("Stock Available", width=150)
        self.CartTable.column("Expiry Date", width=150)
        self.CartTable.column("Manufacturing Date", width=150)

        self.CartTable.pack(fill=BOTH, expand=1)

        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="Black")
        Add_CartWidgetsFrame.place(relx=0, rely=0.56, relwidth=0.2, relheight=0.4)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock [9999]", font=("times new roman", 15), bg="Black",
                                 fg="White")
        self.lbl_inStock.place(x=1, y=20)

        btn_load = Button(Add_CartWidgetsFrame, text="Load", font=("times new roman", 15, "bold"), bg="lightgray",
                          cursor="hand2", command=self.show_selected_data)
        btn_load.place(x=10, y=60, width=200, height=30)

        btn_add_cart = Button(Add_CartWidgetsFrame, text="Checkout & Pay", font=("times new roman", 15, "bold"),
                      bg="orange", cursor="hand2", command=self.checkout)

        btn_add_cart.place(x=10, y=100, width=250, height=30)

        buttons = [
            ("Product Catalogue", open_product_catalogue),
            ("Reports", open_reports),
            ("LogOut", self.logout),
            
        ]

        button_colors = ["#00AEEF", "#FFA500", "#FF4C4C"]

        for i, (text, command) in enumerate(buttons):
            color = button_colors[i % len(button_colors)]
            btn = tk.Button(Add_CartWidgetsFrame, text=text,  bg=color, fg="Black", font=("times new roman", 15, "bold"), bd=0,
                            activebackground="#303030", activeforeground="Black", relief="flat", command=command)
            btn.place(x=10, y=139 + i * 40, width=250, height=30) 

        footer = tk.Label(self.root, text="Retail Wizard", bg="#202020", fg="White", font=("Arial", 12, "italic"),
                          anchor="center")
        footer.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

    def show_selected_data(self):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("SELECT *  FROM selected_product")
        selected_rows = cursor.fetchall()
        columns = [description[0].capitalize() for description in cursor.description]
        conn.close()

        if not selected_rows:
            messagebox.showinfo("Info", "No data available.")
            return

        df = pd.DataFrame(selected_rows, columns=columns)

        for widget in self.cart_Frame.winfo_children():
            widget.destroy()

        tree_frame = tk.Frame(self.cart_Frame, bg="#D3D3D3")
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center") 

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scrolly = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollx = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side="right", fill="y")
        scrollx.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#D3D3D3", font=("Arial", 12))
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"), background="#B0B0B0")

        delete_button = tk.Button(self.cart_Frame, text="Delete Selected", font=("Arial", 12, "bold"),
                                  bg="#FF6347", fg="white",
                                  command=lambda: self.delete_selected_product(tree))
        delete_button.pack(pady=10)


    def delete_selected_product(self, tree):
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No product selected.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected product(s)?")
        if not confirm:
            return

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        for item in selected_items:
            values = tree.item(item)["values"]
            print("Selected row values:", values) 

            if len(values) < 2:
                messagebox.showerror("Error", "Invalid product data.")
                conn.close()
                return

            try:
                product_id = int(values[0])  
                print("Deleting Product ID:", product_id) 
                cursor.execute('DELETE FROM selected_product WHERE sr_no=?', (product_id,))
            except ValueError:
                messagebox.showerror("Error", "Invalid product ID format.")
                conn.close()
                return

        conn.commit()
        conn.close()

        for item in selected_items:
            tree.delete(item)

        messagebox.showinfo("Info", "Product(s) deleted successfully.")

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        try:
            result = self.var_cal_input.get()
            self.var_cal_input.set(eval(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def checkout(self):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        columns_mapping = {
            "category": "Product Category",
            "brand": "Brand",
            "price": "Price",
            "discount": "Discount (%)",
            "final_price": "Final Price"
        }

        db_columns = list(columns_mapping.keys())

        query = f"SELECT {', '.join(db_columns)} FROM selected_product"
        cursor.execute(query)
        rows = cursor.fetchall()

        data = [dict(zip(columns_mapping.values(), row)) for row in rows]

        with open("invoice_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_name TEXT,
                            customer_phone TEXT,
                            total_order_price REAL
                        )''')

        customer_name = self.var_name.get().strip()
        customer_phone = self.var_contact.get().strip()

        if not customer_name or not customer_phone:
            messagebox.showwarning("Warning", "Please enter customer name and phone number.")
            conn.close()
            return

        cursor.execute("SELECT SUM(final_price) FROM selected_product")
        total_price = cursor.fetchone()[0]

        if total_price is None:
            total_price = 0 

        cursor.execute("INSERT INTO transactions (customer_name, customer_phone, total_order_price) VALUES (?, ?, ?)",
                    (customer_name, customer_phone, total_price))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Transaction recorded!\nTotal Order Price: ₹{total_price:.2f}")

        subprocess.Popen(["python", "pay.py"])


    def logout(self, event=None):
        self.root.destroy() 

        if getattr(sys, 'frozen', False):
            subprocess.Popen([sys.executable, os.path.join(sys._MEIPASS, "Sign_In.py")])
        else:
            subprocess.Popen([sys.executable, "Sign_In.py"])


if __name__ == "__main__":

    root = tk.Tk()
    app = RetailWizardApp(root)
    root.mainloop()