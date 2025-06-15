import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
from database.db_connection import db_connection


def inventory(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    conn = db_connection()
    if not conn:
        return
    cursor = conn.cursor()

    parent.configure(bg="white")
    Label(
        parent,
        text="Inventory List",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="black",
    ).pack(anchor="w", padx=20, pady=10)

    cursor.execute("SELECT inventory_id, item_name, quantity, unit FROM inventory")
    inventory_items = cursor.fetchall()

    def open_item(inventory_id, name, current_stock, unit):
        for widget in parent.winfo_children():
            widget.destroy()

        Label(
            parent,
            text=name.upper(),
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
        ).pack(pady=(15, 10))

        info_frame = Frame(parent, bg="white")
        info_frame.pack(pady=20)

        Label(
            info_frame, text="Current Stock", font=("Arial", 12), bg="white", fg="black"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=10)
        display_stock = (
            int(current_stock) if current_stock == int(current_stock) else current_stock
        )
        stock_label = Label(
            info_frame,
            text=f"{display_stock} {unit}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black",
        )

        stock_label.grid(row=0, column=1, sticky="w", padx=20)

        Label(
            info_frame, text="Add Stock", font=("Arial", 12), bg="white", fg="black"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        add_entry = Entry(
            info_frame, width=13, font=("Arial", 12), bd=2, relief="solid"
        )
        add_entry.grid(row=1, column=1, sticky="w", padx=20)

        Label(
            info_frame, text="Reduce Stock", font=("Arial", 12), bg="white", fg="black"
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        reduce_entry = Entry(
            info_frame, width=13, font=("Arial", 12), bd=2, relief="solid"
        )
        reduce_entry.grid(row=2, column=1, sticky="w", padx=20)

        def update_stock():
            try:
                add_val = int(add_entry.get() or 0)
                reduce_val = int(reduce_entry.get() or 0)

                if add_val == 0 and reduce_val == 0:
                    messagebox.showinfo("No Action", "No stock change.")
                    return

                new_stock = current_stock + add_val - reduce_val
                new_stock = max(new_stock, 0)

                confirm = messagebox.askyesno(
                    "Confirm Update", f"Are you sure you want to update the stock?\n\n"
                )
                #  f"Add: {add_val} {unit}\nReduce: {reduce_val} {unit}\n"
                #  f"New total: {new_stock} {unit}")
                if not confirm:
                    return

                cursor.execute(
                    "UPDATE inventory SET quantity = %s WHERE inventory_id = %s",
                    (new_stock, inventory_id),
                )
                conn.commit()

                messagebox.showinfo("Success", "Stock updated successfully!")
                inventory(parent)

            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Please enter valid numeric values only."
                )

        Button(
            parent,
            text="Update Stock",
            bg="#1E3A8A",
            fg="white",
            font=("Arial", 12),
            width=25,
            command=update_stock,
        ).pack(pady=30)

    for inventory_id, item_name, current_stock, unit in inventory_items:
        name_label = Label(
            parent,
            text=item_name,
            font=("Arial", 11),
            fg="black",
            bg="white",
            cursor="hand2",
        )
        name_label.pack(anchor="w", padx=30, pady=5)
        Frame(parent, height=1, bg="gray").pack(fill="x", padx=30, pady=(0, 5))
        name_label.bind(
            "<Button-1>",
            lambda e, iid=inventory_id, name=item_name, qty=current_stock, u=unit: open_item(
                iid, name, qty, u
            ),
        )
