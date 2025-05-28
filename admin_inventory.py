from tkinter import *

def inventory(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")
    Label(parent, text="Inventory List",
          font=("Arial", 12, "bold"),
          bg="white", fg="black").pack(anchor="w", padx=20, pady=10)

    item_name = "INK"
    current_stock = 120

    def open_item(name, current_stock):
        for widget in parent.winfo_children():
            widget.destroy()

        Label(parent, text=name.upper(),
              font=("Arial", 12, "bold"),
              bg="white", fg="black").pack(pady=(10, 5))

        info_frame = Frame(parent,
                           bg="white")
        info_frame.pack(pady=10)

        Label(info_frame,
              text="Current stock",
              font=("Arial", 10),
              bg="white", fg="black").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        Label(info_frame,
              text=str(current_stock),
              font=("Arial", 16, "bold"),
              bg="white", fg="black").grid(row=0, column=1, sticky="w", padx=10)

        Label(info_frame,
              text="Add stock",
              font=("Arial", 10),
              bg="white",
              fg="black").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        Label(info_frame,
              text="0  +",
              font=("Arial", 11),
              bg="white",
              fg="black").grid(row=1, column=1, sticky="w", padx=10)

        Label(info_frame,
              text="Reduce stock",
              font=("Arial", 10),
              bg="white",
              fg="black").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        Label(info_frame,
              text="0  -",
              font=("Arial", 11),
              bg="white",
              fg="black").grid(row=2, column=1, sticky="w", padx=10)

        Button(parent,
               text="Update stock",
               bg="#1E3A8A",
               fg="white",
               font=("Arial", 10),
               width=20).pack(pady=20)

    name_label = Label(parent,
                       text=item_name,
                       font=("Arial", 11),
                       fg="black", bg="white",
                       cursor="hand2")
    name_label.pack(anchor="w",
                    padx=30,
                    pady=5)
    Frame(parent,
          height=1,
          bg="gray").pack(fill="x",
                          padx=30, pady=(0, 5))
    name_label.bind("<Button-1>",
                    lambda e,
                    name=item_name,
                    stock=current_stock: open_item(name, stock))
