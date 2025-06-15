import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
from database.db_connection import db_connection
import shutil
from datetime import datetime


def transaction(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")

    Label(
        parent,
        text="Transaction List",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="black",
    ).pack(anchor="w", padx=20, pady=10)

    def display_transactions(parent):
        for widget in parent.winfo_children():
            widget.destroy()

        parent.configure(bg="white")

        Label(
            parent,
            text="Transaction List",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
        ).pack(anchor="w", padx=20, pady=10)

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.transaction_id, t.customer_id, c.full_name, t.status, t.transaction_date
            FROM customer_transaction t
            JOIN customer c ON t.customer_id = c.customer_id
            WHERE t.status IN ('pending', 'read')
            ORDER BY t.transaction_date DESC
        """
        )
        transactions = cursor.fetchall()
        conn.close()

        if not transactions:
            Label(parent, text="No transactions found", bg="white", fg="black").pack(
                anchor="w", padx=20, pady=20
            )
        else:
            for txn in transactions:
                txn_id, customer_id, full_name, status, transaction_date = txn
                date_obj = (
                    datetime.strptime(transaction_date, "%Y-%m-%d %H:%M:%S")
                    if isinstance(transaction_date, str)
                    else transaction_date
                )
                formatted_date = date_obj.strftime("%b %d %Y %I:%M %p").upper()

                row_frame = Frame(parent, bg="white")
                row_frame.pack(fill="x", padx=30, pady=5)

                name_label = Label(
                    row_frame,
                    text=full_name,
                    font=("Arial", 11),
                    fg="black",
                    bg="white",
                    cursor="hand2",
                )
                name_label.pack(side="left")

                date_label = Label(
                    row_frame,
                    text=formatted_date,
                    font=("Arial", 11),
                    fg="black",
                    bg="white",
                )
                date_label.pack(side="right")

                Frame(parent, height=1, bg="gray").pack(fill="x", padx=30, pady=(0, 5))
                name_label.bind(
                    "<Button-1>",
                    lambda e, txn_id=txn_id: open_transaction_details(txn_id),
                )

    def open_transaction_details(transaction_id):
        top = Toplevel()
        top.title(f"Transaction #{transaction_id}")
        top.geometry("400x300")
        top.configure(bg="white")

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT file_path, size, copies, print_type, total, status
            FROM customer_transaction
            WHERE transaction_id = %s
        """,
            (transaction_id,),
        )
        txn = cursor.fetchone()
        conn.close()

        if txn:
            file_path, size, copies, print_type, total, status = txn
            filename = os.path.basename(file_path)
            size_upper = size.strip().upper()
            copies_int = int(copies)

            main_frame = Frame(top, bg="white")
            main_frame.pack(expand=True, fill="both", padx=30, pady=30)

            Label(
                main_frame, text=filename, bg="white", font=("Arial", 10, "bold")
            ).pack(anchor="w")
            Label(main_frame, text=size_upper, bg="white", font=("Arial", 10)).pack(
                anchor="w", pady=(10, 0)
            )
            Label(
                main_frame, text=f"{copies} COPIES", bg="white", font=("Arial", 10)
            ).pack(anchor="w")
            Label(
                main_frame, text=print_type.upper(), bg="white", font=("Arial", 10)
            ).pack(anchor="w", pady=(0, 10))
            Label(
                main_frame,
                text=f"TOTAL: P{total}",
                bg="white",
                font=("Arial", 12, "bold"),
                fg="black",
            ).pack(anchor="w", pady=5)

            button_frame = Frame(main_frame, bg="white")
            button_frame.pack(pady=20)

            def decline_transaction():
                if messagebox.askyesno(
                    "Decline", "Are you sure you want to decline this transaction?"
                ):
                    conn = db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE customer_transaction SET status = 'declined' WHERE transaction_id = %s",
                        (transaction_id,),
                    )
                    conn.commit()
                    conn.close()
                    display_transactions(parent)
                    messagebox.showinfo("Declined", "Transaction has been declined.")

            def accept_transaction():
                if messagebox.askyesno(
                    "Accept", "Are you sure you want to complete this transaction?"
                ):
                    conn = db_connection()
                    cursor = conn.cursor()

                    if "BOND PAPER" in size_upper:
                        inventory_name = size_upper.strip()
                    else:
                        inventory_name = f"{size_upper} BOND PAPER".strip()

                    cursor.execute(
                        "SELECT quantity FROM inventory WHERE UPPER(TRIM(item_name)) = %s",
                        (inventory_name,),
                    )
                    result = cursor.fetchone()

                    if not result:
                        conn.close()
                        messagebox.showerror(
                            "Inventory Error",
                            f"No inventory record for {inventory_name}.",
                        )
                        return

                    current_quantity = float(result[0])
                    if current_quantity < copies_int:
                        conn.close()
                        messagebox.showwarning(
                            "Insufficient Stock",
                            f"Only {current_quantity} {inventory_name} available.",
                        )
                        return

                    new_quantity = current_quantity - copies_int
                    cursor.execute(
                        "UPDATE inventory SET quantity = %s WHERE UPPER(TRIM(item_name)) = %s",
                        (new_quantity, inventory_name),
                    )
                    cursor.execute(
                        "UPDATE customer_transaction SET status = 'completed' WHERE transaction_id = %s",
                        (transaction_id,),
                    )
                    conn.commit()
                    conn.close()

                    download_folder = (
                        "/home/black/Documents/online-printing-service-system/Customer Files"
                    )
                    if not os.path.exists(download_folder):
                        os.makedirs(download_folder)

                    if os.path.exists(file_path):
                        shutil.copy(file_path, os.path.join(download_folder, filename))
                        messagebox.showinfo(
                            "Success", "Transaction completed. File downloaded."
                        )
                    else:
                        messagebox.showwarning(
                            "File Not Found",
                            "Transaction completed but file not found.",
                        )

                    display_transactions(parent)

            Button(
                button_frame,
                text="Decline",
                bg="darkred",
                fg="white",
                command=decline_transaction,
                width=10,
            ).pack(side="left", padx=10)
            Button(
                button_frame,
                text="Accept",
                bg="darkblue",
                fg="white",
                command=accept_transaction,
                width=10,
            ).pack(side="left", padx=10)

    display_transactions(parent)
