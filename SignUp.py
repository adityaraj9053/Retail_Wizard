import tkinter as tk
import subprocess
from Sign_Up_DB import store_user

root = tk.Tk()
root.title("Sign Up")
root.geometry("400x500")
root.configure(bg="#4a00e0")
root.state("zoomed") 
frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Sign Up", font=("Arial", 18, "bold"), bg="white").pack(pady=(10, 20))

tk.Label(frame, text="Fullname", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
entry_fullname = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", width=30)
entry_fullname.pack(pady=5)

tk.Label(frame, text="Username", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
entry_email = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", width=30)
entry_email.pack(pady=5)

tk.Label(frame, text="Password", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
entry_password = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", show="*", width=30)
entry_password.pack(pady=5)

def signup():
    fullname = entry_fullname.get()
    username = entry_email.get()
    password = entry_password.get()
    message, color = store_user(fullname, username, password)
    status_label.config(text=message, fg=color)

def open_login():
    root.destroy()
    subprocess.run(["python", "sign_in.py"])

tk.Button(frame, text="Sign up", bg="#4a00e0", fg="white", font=("Arial", 12), width=15, relief="flat", command=signup).pack(pady=20)

status_label = tk.Label(frame, text="", font=("Arial", 10), bg="white")
status_label.pack()

tk.Label(frame, text="Already have an account?", font=("Arial", 10), bg="white").pack()
tk.Button(frame, text="Log In", bg="white", fg="#4a00e0", font=("Arial", 10, "bold"), relief="flat", command=open_login).pack(pady=(5, 10))

root.mainloop()
