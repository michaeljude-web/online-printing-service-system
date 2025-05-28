from tkinter import *

def customer_profile(parent):
    for widget in parent.winfo_children():
        widget.destroy()



    Label(parent,
          text="No notificatiggon",
          font=("Arial", 12, "bold"),
          bg="#f5f5f5",
          fg="black").pack(fill="x", pady=10)





