import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from database.db_connection import db_connection
import mysql.connector
from datetime import datetime


def notification(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")

    try:
        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT c.full_name, ct.size, ct.print_type, ct.copies, ct.transaction_date
            FROM customer_transaction ct
            JOIN customer c ON ct.customer_id = c.customer_id
            WHERE ct.status = 'pending'
            ORDER BY ct.transaction_date DESC
        """
        )
        notifications = cursor.fetchall()

        if not notifications:
            Label(
                parent,
                text="No notifications",
                font=("Arial", 12),
                bg="white",
                fg="black",
            ).pack(fill="x", pady=10)
            return

        for full_name, size, print_type, copies, transaction_date in notifications:
            dt = datetime.strptime(str(transaction_date), "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%B %d %Y %I:%M %p")

            frame = Frame(parent, bg="white", bd=1, relief="solid", padx=10, pady=5)
            frame.pack(fill="x", padx=10, pady=5)

            Label(
                frame,
                text=full_name,
                font=("Arial", 11, "bold"),
                anchor="w",
                bg="white",
            ).pack(fill="x")

            info_frame = Frame(frame, bg="white")
            info_frame.pack(fill="x")

            left_text = f"{size} ({print_type}) {copies} copies"
            Label(
                info_frame, text=left_text, font=("Arial", 10), anchor="w", bg="white"
            ).pack(side=LEFT)

            Label(
                info_frame, text=date_str, font=("Arial", 10), anchor="e", bg="white"
            ).pack(side=RIGHT)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        Label(
            parent,
            text=f"Database error: {err}",
            font=("Arial", 10),
            fg="red",
            bg="white",
        ).pack(fill="x", pady=10)
