import tkinter as tk
import sqlite3
from Sign_Up_DB import update_password

root = tk.Tk()
root.title("Forgot Password")
root.geometry("300x400")
root.configure(bg="#3f00ff")
root.state("zoomed") 
form_frame = tk.Frame(root, bg="white", width=250, height=300)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(form_frame, text="Reset Password", font=("Arial", 16, "bold"), bg="white")
title_label.place(relx=0.5, y=30, anchor=tk.CENTER)

email_label = tk.Label(form_frame, text="Email", bg="white", font=("Arial", 10))
email_label.place(x=25, y=70)
email_entry = tk.Entry(form_frame, width=25, font=("Arial", 10))
email_entry.place(x=25, y=95)

new_pass_label = tk.Label(form_frame, text="New Password", bg="white", font=("Arial", 10))
new_pass_label.place(x=25, y=130)
new_pass_entry = tk.Entry(form_frame, width=25, font=("Arial", 10), show="*")
new_pass_entry.place(x=25, y=155)

confirm_pass_label = tk.Label(form_frame, text="Confirm Password", bg="white", font=("Arial", 10))
confirm_pass_label.place(x=25, y=190)
confirm_pass_entry = tk.Entry(form_frame, width=25, font=("Arial", 10), show="*")
confirm_pass_entry.place(x=25, y=215)

status_label = tk.Label(form_frame, text="", bg="white", font=("Arial", 10))
status_label.place(relx=0.5, y=250, anchor=tk.CENTER)

def reset_password():
    email = email_entry.get()
    new_password = new_pass_entry.get()
    confirm_password = confirm_pass_entry.get()

    if new_password != confirm_password:
        status_label.config(text="Passwords do not match!", fg="red")
        return
    
    if update_password(email, new_password):
        status_label.config(text="Password reset successful!", fg="green")
    else:
        status_label.config(text="Email not found!", fg="red")

tk.Button(form_frame, text="Reset Password", bg="#3f00ff", fg="white", font=("Arial", 12, "bold"), command=reset_password).place(relx=0.5, y=280, anchor=tk.CENTER)

root.mainloop()
