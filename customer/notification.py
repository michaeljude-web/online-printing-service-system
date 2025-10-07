import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from database.db_connection import db_connection
from datetime import datetime


def notification(parent, customer_id=None):
    for widget in parent.winfo_children():
        widget.destroy()

    if customer_id is None:
        try:
            from customer_dashboard import CURRENT_CUSTOMER_ID

            customer_id = CURRENT_CUSTOMER_ID
        except ImportError:
            Label(
                parent,
                text="Error: Customer ID not available",
                font=("Arial", 12, "bold"),
                bg="#f8f8f8",
                fg="red",
            ).place(relx=0.5, rely=0.5, anchor="center")
            return

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT transaction_id, file_path, status, transaction_date, total
        FROM customer_transaction
        WHERE customer_id = %s AND status IN ('read', 'declined', 'completed')
        ORDER BY transaction_date DESC
    """,
        (customer_id,),
    )
    notifications = cursor.fetchall()
    conn.close()

    if not notifications:
        Label(
            parent,
            text="No notifications",
            font=("Arial", 12, "bold"),
            bg="#f8f8f8",
            fg="gray",
        ).place(relx=0.5, rely=0.5, anchor="center")
        return

    canvas = Canvas(parent, bg="#f8f8f8")
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_content = Frame(canvas, bg="#f8f8f8")

    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_width = event.width
        canvas.itemconfig(canvas_window, width=canvas_width)

    scrollable_content.bind("<Configure>", configure_canvas)

    canvas_window = canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind("<Configure>", configure_canvas)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for notification in notifications:
        filename = os.path.basename(notification[1])
        status = notification[2].lower()
        date = notification[3]
        total = notification[4]

        if status == "completed":
            status_color = "#28a745"
            status_text = "COMPLETED"
            message = f"Your printing request for '{filename}' has been completed!"
        elif status == "declined":
            status_color = "#dc3545"
            status_text = "DECLINED"
            message = f"Your printing request for '{filename}' has been declined."
        elif status == "read":
            status_color = "#17a2b8"
            status_text = "READ"
            message = f"Your printing request for '{filename}' has been read by admin."

        notification_frame = Frame(scrollable_content, bg="white", bd=1, relief="solid")
        notification_frame.pack(fill="x", pady=5, padx=5)

        header_frame = Frame(notification_frame, bg="white")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))

        status_label = Label(
            header_frame,
            text=status_text,
            bg=status_color,
            fg="white",
            font=("Arial", 8, "bold"),
            width=10,
            anchor="center",
        )
        status_label.pack(side="left")

        date_label = Label(
            header_frame, text=str(date), bg="white", fg="gray", font=("Arial", 8)
        )
        date_label.pack(side="right")

        message_label = Label(
            notification_frame,
            text=message,
            bg="white",
            fg="black",
            font=("Arial", 10),
            wraplength=800,
            justify="left",
        )
        message_label.pack(anchor="w", padx=15, pady=(0, 5))

        if total:
            total_label = Label(
                notification_frame,
                text=f"Total: P{total}",
                bg="white",
                fg="black",
                font=("Arial", 9, "bold"),
            )
            total_label.pack(anchor="w", padx=15, pady=(0, 10))
