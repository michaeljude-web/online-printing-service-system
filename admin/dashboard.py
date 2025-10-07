import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mysql.connector
from tkinter import Frame, Label, messagebox
from database.db_connection import db_connection


def get_pending_completed_counts():
    connection = db_connection()
    if connection is None:
        return 0, 0

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM customer_transaction WHERE status = 'pending'"
        )
        pending_count = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM customer_transaction WHERE status = 'completed'"
        )
        completed_count = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        messagebox.showerror(
            "Database Error", f"Error fetching transaction counts: {err}"
        )
        pending_count, completed_count = 0, 0
    finally:
        cursor.close()
        connection.close()

    return pending_count, completed_count


def get_inventory_totals():
    connection = db_connection()
    if connection is None:
        return 0, 0, 0

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT quantity FROM inventory WHERE item_name = 'Short Bond Paper'"
        )
        short_bond_result = cursor.fetchone()
        short_bond_quantity = short_bond_result[0] if short_bond_result else 0

        cursor.execute(
            "SELECT quantity FROM inventory WHERE item_name = 'Long Bond Paper'"
        )
        long_bond_result = cursor.fetchone()
        long_bond_quantity = long_bond_result[0] if long_bond_result else 0

        cursor.execute(
            "SELECT quantity FROM inventory WHERE item_name = 'A4 Bond Paper'"
        )
        a4_bond_result = cursor.fetchone()
        a4_bond_quantity = a4_bond_result[0] if a4_bond_result else 0

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching inventory data: {err}")
        short_bond_quantity, long_bond_quantity, a4_bond_quantity = 0, 0, 0
    finally:
        cursor.close()
        connection.close()

    return short_bond_quantity, long_bond_quantity, a4_bond_quantity


def dashboard(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    container = Frame(parent, bg="white")
    container.pack(expand=True, fill="both", padx=20, pady=20)

    left_frame = Frame(container, bg="white")
    left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    right_frame = Frame(container, bg="white")
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)
    container.grid_rowconfigure(0, weight=1)

    left_frame.grid_rowconfigure(0, weight=3)
    right_frame.grid_rowconfigure(0, weight=3)

    pending_count, completed_count = get_pending_completed_counts()

    short_bond_qty, long_bond_qty, a4_bond_qty = get_inventory_totals()
    inventory_stats = [
        ("Short Bond Paper", short_bond_qty),
        ("Long Bond Paper", long_bond_qty),
        ("A4 Bond Paper", a4_bond_qty),
    ]

    for i, (label, quantity) in enumerate(inventory_stats):
        box = Frame(left_frame, bg="#1e3a8a", bd=1, relief="solid")
        box.grid(row=i, column=0, padx=10, pady=15, sticky="nsew")
        box.grid_propagate(False)

        Label(
            box,
            text=label,
            bg="#1e3a8a",
            fg="white",
            font=("Arial", 10, "bold"),
            anchor="center",
        ).pack(pady=(10, 0), expand=True)
        Label(
            box,
            text=str(quantity),
            bg="#1e3a8a",
            fg="white",
            font=("Arial", 16, "bold"),
            anchor="center",
        ).pack(pady=(5, 10), expand=True)

    stats = [("PENDING", pending_count), ("COMPLETED", completed_count)]

    for i, (label, count) in enumerate(stats):
        box = Frame(right_frame, bg="#34D399", bd=1, relief="solid")
        box.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")
        box.grid_propagate(False)
        box.configure(height=150)

        Label(
            box,
            text=label,
            bg="#34D399",
            fg="white",
            font=("Arial", 10, "bold"),
            anchor="center",
        ).pack(pady=(10, 0), expand=True)
        Label(
            box,
            text=str(count),
            bg="#34D399",
            fg="white",
            font=("Arial", 16, "bold"),
            anchor="center",
        ).pack(pady=(5, 10), expand=True)

    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)
