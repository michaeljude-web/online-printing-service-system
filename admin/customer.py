import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from database.db_connection import db_connection
from tkinter import messagebox


def approve_customer(customer_id, refresh_func):
    try:
        mydb = db_connection()
        cursor = mydb.cursor()
        cursor.execute(
            "UPDATE customer SET status = 'Approved' WHERE customer_id = %s",
            (customer_id,),
        )
        mydb.commit()
        messagebox.showinfo("Approved", "Customer approved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        mydb.close()
        refresh_func()


def delete_customer(customer_id, refresh_func):
    confirm = messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this customer?"
    )
    if confirm:
        try:
            mydb = db_connection()
            cursor = mydb.cursor()
            cursor.execute(
                "DELETE FROM customer WHERE customer_id = %s", (customer_id,)
            )
            mydb.commit()
            messagebox.showinfo("Deleted", "Customer deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            mydb.close()
            refresh_func()


def customer(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")

    Label(
        parent,
        text="Pending Customer Approvals",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="black",
    ).pack(anchor="w", padx=20, pady=10)

    try:
        mydb = db_connection()
        cursor = mydb.cursor()
        cursor.execute(
            "SELECT customer_id, full_name, email FROM customer WHERE status = 'Pending'"
        )
        pending_customers = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return
    finally:
        cursor.close()
        mydb.close()

    if not pending_customers:
        Label(
            parent, text="No pending customers.", font=("Arial", 10), bg="white"
        ).pack(padx=20, pady=20)
        return

    for customer_data in pending_customers:
        customer_id, full_name, email = customer_data

        row = Frame(parent, bg="white")
        row.pack(fill="x", padx=20, pady=10)

        info = Frame(row, bg="white")
        info.pack(side="left", fill="x", expand=True)

        Label(
            info, text=full_name, font=("Arial", 10, "bold"), bg="white", fg="black"
        ).pack(anchor="w")

        Label(info, text=email, font=("Arial", 9), bg="white", fg="black").pack(
            anchor="w"
        )

        buttons = Frame(row, bg="white")
        buttons.pack(side="right")

        Button(
            buttons,
            text="Approve",
            bg="#1E3A8A",
            fg="white",
            font=("Arial", 9),
            width=10,
            command=lambda cid=customer_id: approve_customer(
                cid, lambda: customer(parent)
            ),
        ).pack(side="left", padx=5)

        Button(
            buttons,
            text="❌",
            bg="#7f1d1d",
            fg="white",
            font=("Arial", 9),
            width=3,
            command=lambda cid=customer_id: delete_customer(
                cid, lambda: customer(parent)
            ),
        ).pack(side="left", padx=5)
