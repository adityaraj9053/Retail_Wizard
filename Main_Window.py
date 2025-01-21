import tkinter as tk

root=tk.Tk()
root.title("Retail Wizard") # Title of window
root.configure(bg="#2B2B2B")

root.attributes('-fullscreen',True) # Make the window fullscreen

# Search Bar
search_label=tk.Label(root,text="Search Products:",font=("Arial",16),bg="#2B2B2B",fg="white") # fg=foreground
search_label.place(relx=0.02,rely=0.02)
search_bar=tk.Entry(root,font=("Arial",14),bg="#404040",fg="white",insertbackground="white",relief="flat")
search_bar.place(relx=0.17,rely=0.02,relwidth=0.6,height=35) # height is 35 px
# insertbackground="white" :Sets the color of the blinking cursor in the text input field to white. Without this, the cursor might not be visible against a dark background.
# relief="flat" : Removes the 3D border around the input box, making it flat and modern-looking.


# Table Section
table_frame=tk.Frame(root,bg="#3C3C3C",bd=1,relief="ridge")
table_frame.place(relx=0.02,rely=0.08,relwidth=0.8,relheight=0.6)

# Table Headers
headers=["Product Name","Quantity","Price","Amount"]
header_bg="#505050"
header_fg="white"

for i,header in enumerate(headers):  # i:index and header:header text
    tk.Label(table_frame,text=header,bg=header_bg,fg=header_fg,font=("Arial", 12, "bold")).place(relx=i*0.25,rely=0,relwidth=0.25,height=30)


# Totals Section
totals_frame=tk.Frame(root,bg="#2B2B2B")
totals_frame.place(relx=0.02,rely=0.7,relwidth=0.8,relheight=0.15)# relwidth=0.8 covers 80% of window width

totals_labels=["Subtotal","Tax","Total"]
totals_bg_colors=["#404040","#505050","#606060"]
for i,label in enumerate(totals_labels):
    tk.Label(totals_frame,text=label,fg="white",bg=totals_bg_colors[i],font=("Arial",12),anchor="w",padx=10,).place(relx=0.02,rely=0.1+i*0.25,relwidth=0.4,relheight=0.2)
    tk.Label(totals_frame,text="0.00",fg="white",bg=totals_bg_colors[i],font=("Arial", 12),anchor="e",padx=10,).place(relx=0.6,rely=0.1+i*0.25,relwidth=0.4,relheight=0.2)
    # anchor = e i.e. east of frame


# Button Section
button_frame=tk.Frame(root,bg="#404040",bd=1,relief="ridge") # bd=border width 2 px
button_frame.place(relx=0.85,rely=0.08,relwidth=0.13,relheight=0.77)

buttons=[
    ("Product Catalogue",""),
    ("Voucher",""),
    ("Reports",""),
    ("Accounts",""),
    ("Payment",""),
    ("Reset","")
]

button_colors=["#00AEEF", "#FFA500","#FF4C4C","#6C63FF"]
for i,(text,shortcut) in enumerate(buttons):
    color=button_colors[i % len(button_colors)]
    tk.Button(button_frame,text=f"{text}\n{shortcut}",bg=color,fg="white",font=("Arial", 11, "bold"),bd=0,activebackground="#303030",activeforeground="white",relief="flat").place(relx=0.05, rely=i * 0.055, relwidth=0.9, relheight=0.05)

# Footer Section
footer=tk.Label(root,text="Retail Wizard",bg="#202020",fg="white",font=("Arial",12,"italic"),anchor="center",)
footer.place(relx=0,rely=0.95,relwidth=1,relheight=0.05)

root.mainloop()
