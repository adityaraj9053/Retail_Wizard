import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("300x400")
root.configure(bg="#3f00ff")  # Set background color to purple

# Create the frame for the login form
form_frame = tk.Frame(root, bg="white", width=250, height=300)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title
title_label = tk.Label(form_frame, text="Login", font=("Arial", 16, "bold"), bg="white")
title_label.place(relx=0.5, y=30, anchor=tk.CENTER)

# Username label and entry
username_label = tk.Label(form_frame, text="Username", bg="white", font=("Arial", 10))
username_label.place(x=25, y=70)
username_entry = tk.Entry(form_frame, width=25, font=("Arial", 10))
username_entry.place(x=25, y=95)

# Password label and entry
password_label = tk.Label(form_frame, text="Password", bg="white", font=("Arial", 10))
password_label.place(x=25, y=130)
password_entry = tk.Entry(form_frame, width=25, font=("Arial", 10), show="*")
password_entry.place(x=25, y=155)

# Login button
login_button = tk.Button(form_frame, text="Login", bg="#3f00ff", fg="white", font=("Arial", 12, "bold"))
login_button.place(relx=0.5, y=200, anchor=tk.CENTER)

val_label = tk.Label(form_frame, text="Don't have an account?", bg="white", font=("Arial", 10))
val_label.place(relx=0.5, y=240, anchor=tk.CENTER)
tk.Button(form_frame, text="Sign Up", bg="white", fg="#4a00e0", font=("Arial", 10, "bold"), relief="flat").place(relx=0.5, y=270, anchor=tk.CENTER)

# Run the application
root.mainloop()
