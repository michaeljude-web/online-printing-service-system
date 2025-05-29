from tkinter import *
from tkinter import messagebox
from db_connection import db_connection  
import os  
import shutil  

def transaction(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")

    Label(parent, text="Transaction List", font=("Arial", 12, "bold"), bg="white", fg="black").pack(anchor="w", padx=20, pady=10)

    def display_transactions(parent):
        for widget in parent.winfo_children():
            widget.destroy()

        parent.configure(bg="white")

        Label(parent, text="Transaction List", font=("Arial", 12, "bold"), bg="white", fg="black").pack(anchor="w", padx=20, pady=10)

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.transaction_id, t.customer_id, c.full_name
            FROM customer_transaction t
            JOIN customer c ON t.customer_id = c.customer_id
            WHERE t.status = 'pending'
        """)
        transactions = cursor.fetchall()

        if not transactions:
            Label(parent, text="No pending transactions", bg="white", fg="black").pack(anchor="w", padx=20, pady=20)
        else:
            for txn in transactions:
                txn_id, customer_id, full_name = txn

                name_label = Label(parent,
                                   text=full_name,
                                   font=("Arial", 11),
                                   fg="black", bg="white",
                                   cursor="hand2")
                name_label.pack(anchor="w", padx=30, pady=5)

                Frame(parent, height=1, bg="gray").pack(fill="x", padx=30, pady=(0, 5))

                name_label.bind("<Button-1>", lambda e, txn_id=txn_id: open_transaction_details(txn_id))

    def open_transaction_details(transaction_id):
        top = Toplevel()
        top.title(f"Transaction #{transaction_id}")
        top.geometry("400x300")
        top.configure(bg="white")

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT file_path, size, copies, print_type, total, status
            FROM customer_transaction
            WHERE transaction_id = %s
        """, (transaction_id,))
        txn = cursor.fetchone()
        conn.close()

        if txn:
            file_path, size, copies, print_type, total, status = txn

            filename = os.path.basename(file_path)
            size = size.upper()
            copies = f"{copies} COPIES"
            print_type = print_type.upper()
            total = f"P{total}"

            main_frame = Frame(top, bg="white")
            main_frame.pack(expand=True, fill="both", padx=30, pady=30)

            top_row = Frame(main_frame, bg="white")
            top_row.pack(fill="x")

            Label(top_row, text=filename, bg="white", font=("Arial", 10, "bold")).pack(side="left")
            right = Frame(top_row, bg="white")
            right.pack(side="right")

            Label(right, text="Total bill", bg="white", font=("Arial", 8)).pack(anchor="e")
            Label(right, text=total, bg="white", fg="black", font=("Arial", 12, "bold")).pack(anchor="e")

            Label(main_frame, text=size, bg="white", font=("Arial", 10)).pack(anchor="w", pady=(15, 3))
            Label(main_frame, text=copies, bg="white", font=("Arial", 10)).pack(anchor="w", pady=3)
            Label(main_frame, text=print_type, bg="white", font=("Arial", 10)).pack(anchor="w", pady=3)

            button_frame = Frame(main_frame, bg="white")
            button_frame.pack(pady=20)

            def decline_transaction():
                result = messagebox.askquestion("Decline Transaction", "Are you sure you want to decline this transaction?")
                if result == 'yes':
                    try:
                        conn = db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE customer_transaction
                            SET status = 'declined'
                            WHERE transaction_id = %s
                        """, (transaction_id,))
                        conn.commit()
                        conn.close()

                        display_transactions(parent)  # <--
                        messagebox.showinfo("Success", "Transaction has been declined.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error occurred while declining transaction: {e}")

            def accept_transaction():
                result = messagebox.askquestion("Complete Transaction", "Are you sure you want to complete this transaction?")
                if result == 'yes':
                    try:
                        conn = db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE customer_transaction
                            SET status = 'completed'
                            WHERE transaction_id = %s
                        """, (transaction_id,))
                        conn.commit()
                        conn.close()
#DIRI ----------------------------------------------------------------------------------------------------------#
                        download_folder = "C:/Users/agard/Documents/Final AppDev/Customer Files"
                        if not os.path.exists(download_folder): 
                            os.makedirs(download_folder)  

                        if os.path.exists(file_path):
                            shutil.copy(file_path, os.path.join(download_folder, filename))  
                            messagebox.showinfo("Success", f"Transaction has been completed and file is downloaded.")
                        else:
                            messagebox.showerror("Error", "File not found for download.")


                        display_transactions(parent)  # <--
                    except Exception as e:
                        messagebox.showerror("Error", f"Error occurred while completing transaction: {e}")

            Button(button_frame, text="Decline", bg="darkred", fg="white", width=10, command=decline_transaction).pack(side="left", padx=10)

            Button(button_frame, text="Accept", bg="darkblue", fg="white", width=10, command=accept_transaction).pack(side="left", padx=10)


    display_transactions(parent) 
