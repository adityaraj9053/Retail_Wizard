import tkinter as tk
import subprocess
from Sign_Up_DB import verify_user

root = tk.Tk()
root.title("Login Page")
root.geometry("300x400")
root.configure(bg="#3f00ff")
root.state("zoomed") 
form_frame = tk.Frame(root, bg="white", width=250, height=320)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(form_frame, text="Login", font=("Arial", 16, "bold"), bg="white")
title_label.place(relx=0.5, y=30, anchor=tk.CENTER)

username_label = tk.Label(form_frame, text="Username", bg="white", font=("Arial", 10))
username_label.place(x=25, y=70)
username_entry = tk.Entry(form_frame, width=25, font=("Arial", 10))
username_entry.place(x=25, y=95)

password_label = tk.Label(form_frame, text="Password", bg="white", font=("Arial", 10))
password_label.place(x=25, y=130)
password_entry = tk.Entry(form_frame, width=25, font=("Arial", 10), show="*")
password_entry.place(x=25, y=155)

status_label = tk.Label(form_frame, text="", bg="white", font=("Arial", 10))
status_label.place(relx=0.5, y=180, anchor=tk.CENTER)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if verify_user(username, password):
        root.destroy()
        subprocess.run(["python", "Main_Window.py"])
    else:
        status_label.config(text="Invalid credentials", fg="red")

def open_signup():
    root.destroy()
    subprocess.run(["python", "SignUp.py"])

def open_forgot_password():
    root.destroy()
    subprocess.run(["python", "Forgot_Password.py"])

tk.Button(form_frame, text="Login", bg="#3f00ff", fg="white", font=("Arial", 12, "bold"), command=login).place(relx=0.5, y=200, anchor=tk.CENTER)

val_label = tk.Label(form_frame, text="Don't have an account?", bg="white", font=("Arial", 10))
val_label.place(relx=0.5, y=240, anchor=tk.CENTER)
tk.Button(form_frame, text="Sign Up", bg="white", fg="#4a00e0", font=("Arial", 10, "bold"), relief="flat", command=open_signup).place(relx=0.5, y=270, anchor=tk.CENTER)

forgot_password_button = tk.Button(form_frame, text="Forgot Password?", bg="white", fg="red", font=("Arial", 10, "bold"), relief="flat", command=open_forgot_password)
forgot_password_button.place(relx=0.5, y=300, anchor=tk.CENTER)

root.mainloop()
