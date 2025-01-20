import tkinter as tk

import pymysql

# Create main window
root = tk.Tk() # tkinter module is calling Tk() constructor for creating a window.
root.title("Sign Up") # tittle of the window created
root.geometry("400x500") # setting the dimensions of the window
root.configure(bg="#4a00e0") # setting the background color of window.

# Add frame for form
frame = tk.Frame(root, bg="white", padx=20, pady=20)
# root specifying that this frame would be placed inside the root window
# bg setting the background color of the frame
# padx adding horizontal padding
# pady adding vertical padding

frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

# Title
tk.Label(frame, text="Sign Up", font=("Arial", 18, "bold"), bg="white").pack(pady=(10, 20))

# Fullname
tk.Label(frame, text="Fullname", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
# "anchor" specifies how text will be aligned within the label. "w" stands for west i.e.  left side on a map
#  .pack(fill="x") tells the label to expand horizontally to fill the entire
# relief specifies the style of the border around the Entry label. flat means there will be no visible 3D effect on the border, and the Entry will appear flat
entry_fullname = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", width=30)
entry_fullname.pack(pady=5)

# Email
tk.Label(frame, text="Username", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
entry_email = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", width=30)
entry_email.pack(pady=5)

# Password
tk.Label(frame, text="Password", font=("Arial", 10), bg="white", anchor="w").pack(fill="x")
entry_password = tk.Entry(frame, font=("Arial", 12), bg="#f3f3f3", relief="flat", show="*", width=30)
entry_password.pack(pady=5)

# Sign Up Button
tk.Button(frame, text="Sign up", bg="#4a00e0", fg="white", font=("Arial", 12), width=15, relief="flat").pack(pady=20)

# Already have an account?
tk.Label(frame, text="Already have an account?", font=("Arial", 10), bg="white").pack()
tk.Button(frame, text="Login in", bg="white", fg="#4a00e0", font=("Arial", 10, "bold"), relief="flat").pack(pady=(5, 10))


# Run the application
root.mainloop()
