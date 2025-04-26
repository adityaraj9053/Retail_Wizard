import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import qrcode
from PIL import Image, ImageTk
from fpdf import FPDF
import os
import sqlite3


class InvoiceApp:
    def __init__(self, root, invoice_data):
        self.root = root
        self.root.title("Invoice")
        self.root.geometry("800x600")

        self.invoice_data = invoice_data

        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(transactions)")
        columns = [col[1] for col in cursor.fetchall()]

        if "payment_method" not in columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN payment_method TEXT")
        if "balance_given" not in columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN balance_given REAL")

        conn.commit()
        conn.close()

        title_label = tk.Label(root, text="INVOICE", font=("Arial", 18, "bold"), fg="blue")
        title_label.pack()

        main_frame = tk.Frame(root)
        main_frame.pack()

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", padx=10)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", padx=10)

        qr_data = "upi://pay?pa=7070025828@pthdfc&pn=Mr%20Aditya%20Raj"
        qr = qrcode.make(qr_data)
        qr.save("qr_invoice.png")

        qr_image = Image.open("qr_invoice.png")
        qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
        qr_photo = ImageTk.PhotoImage(qr_image)

        qr_label = tk.Label(left_frame, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack()

        table_frame = ttk.Frame(right_frame)
        table_frame.pack()

        headers = ["Product Category", "Brand", "Price", "Discount (%)", "Final Price"]
        for j, header in enumerate(headers):
            lbl = ttk.Label(table_frame, text=header, borderwidth=1, relief="solid", padding=5, font=("Arial", 10, "bold"))
            lbl.grid(row=0, column=j, sticky="nsew")

        self.total_sum = 0.0
        for i, row in enumerate(self.invoice_data, start=1):
            try:
                values = [row.get(header, "N/A") for header in headers]  
                for j, item in enumerate(values):
                    lbl = ttk.Label(table_frame, text=item, borderwidth=1, relief="solid", padding=5)
                    lbl.grid(row=i, column=j, sticky="nsew")

                self.total_sum += float(row.get("Final Price", 0))
            except ValueError as e:
                print(f"Skipping invalid entry: {e}")

        sum_label = tk.Label(root, text="Sum of All Products (Rs.):", font=("Arial", 12))
        sum_label.pack(pady=5)
        self.sum_entry = tk.Entry(root, font=("Arial", 12))
        self.sum_entry.pack(pady=5)
        self.sum_entry.insert(0, f"Rs. {self.total_sum:.2f}")
        self.sum_entry.config(state="readonly")

        cancel_button = tk.Button(root, text="Cancel", font=("Arial", 14, "bold"), bg="red", fg="white", command=self.cancel_invoice)
        cancel_button.pack(padx=1, pady=10)

        pay_button = tk.Button(root, text="Pay", font=("Arial", 14, "bold"), bg="green", fg="white", command=self.select_payment_method)
        pay_button.pack(padx=20, pady=10)

    def cancel_invoice(self):
        self.root.destroy()

    def select_payment_method(self):
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Select Payment Method")
        payment_window.geometry("300x200")

        tk.Label(payment_window, text="Choose Payment Method:", font=("Arial", 12)).pack(pady=10)

        cash_button = tk.Button(payment_window, text="Cash", font=("Arial", 12), bg="orange", fg="black", command=lambda: self.handle_cash_payment(payment_window))
        cash_button.pack(pady=5)

        upi_button = tk.Button(payment_window, text="UPI", font=("Arial", 12), bg="blue", fg="white", command=lambda: self.handle_upi_payment(payment_window))
        upi_button.pack(pady=5)

    def handle_cash_payment(self, window):
        window.destroy()
        amount_given = simpledialog.askfloat("Cash Payment", "Enter amount given by customer:")
        if amount_given is None:
            return

        balance = max(0, int(amount_given - self.total_sum))

        if amount_given < self.total_sum:
            messagebox.showerror("Error", "Insufficient amount given!")
        else:
            messagebox.showinfo("Payment Successful", f"Payment received. Change: Rs. {balance}")
            self.update_transaction("Cash", balance)
            self.reset_selected_product_table() 
            self.clear_invoice_data()  
            self.generate_invoice_pdf()

    def handle_upi_payment(self, window):
        window.destroy()
        messagebox.showinfo("UPI Payment", "Payment received successfully!")
        self.update_transaction("UPI", 0)
        self.reset_selected_product_table() 
        self.clear_invoice_data()
        self.generate_invoice_pdf()

    def update_transaction(self, payment_method, balance_given):
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE transactions SET payment_method = ?, balance_given = ? WHERE id = (SELECT MAX(id) FROM transactions)", (payment_method, balance_given))
        conn.commit()
        conn.close()


    def generate_invoice_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(10, 10, 10)

        pdf.set_font("Arial", size=16)
        pdf.cell(190, 10, txt="INVOICE", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(5)

        headers = ["Product Category", "Brand", "Price", "Discount (%)", "Final Price"]
        col_widths = [50, 40, 30, 30, 40]  

        # Table header
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, txt=header, border=1, align="C")
        pdf.ln()

        # Table data
        for row in self.invoice_data:
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, txt=str(row.get(header, "N/A")).encode("latin-1", "replace").decode("latin-1"), border=1, align="C")
            pdf.ln()

        pdf.ln(5)
        total_text = f"Total Amount: Rs. {self.total_sum:.2f}"
        pdf.cell(190, 10, txt=total_text.encode("latin-1", "replace").decode("latin-1"), ln=True, align="R")

        try:
            pdf.output("invoice.pdf", "F")
            messagebox.showinfo("Success", "Invoice has been generated as PDF.")
            os.startfile("invoice.pdf")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")

    def reset_selected_product_table(self):
        """Save selected_product data to sales_report before clearing it."""
        conn = sqlite3.connect("grocery.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_report (
                sr_no INTEGER,
                product_name TEXT,
                quantity INTEGER,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO stock_report (sr_no, product_name, quantity)
            SELECT sr_no, product_name, COUNT(*) FROM selected_product GROUP BY sr_no, product_name
        """)

        cursor.execute("DELETE FROM selected_product")

        conn.commit()
        conn.close()


    def clear_invoice_data(self):
        """Resets invoice_data.json by writing an empty list."""
        with open("invoice_data.json", "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

if __name__ == "__main__":
    if __name__ == "__main__":
        if not os.path.exists("invoice_data.json"):
            with open("invoice_data.json", "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

        with open("invoice_data.json", "r", encoding="utf-8") as f:
            invoice_data = json.load(f)

    root = tk.Tk()
    app = InvoiceApp(root, invoice_data)
    root.mainloop()
