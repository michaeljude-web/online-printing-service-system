from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_connection import db_connection
import os
from customer_transaction import open_transaction_popup
from customer_notification import customer_notification
from customer_profile import customer_profile


def cancel_transaction(transaction_id, frame_to_remove):
    def confirm_cancel():
        result = messagebox.askquestion(
            "Cancel Transaction", "Are you sure you want to cancel this transaction?"
        )

        if result == "yes":
            try:
                conn = db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM customer_transaction WHERE transaction_id = %s
                """,
                    (transaction_id,),
                )

                conn.commit()
                conn.close()

                frame_to_remove.destroy()

                print(f"Transaction #{transaction_id} has been successfully canceled.")

                display_transactions(content)

            except Exception as e:
                print(f"Error occurred while canceling transaction: {e}")
        else:
            print("Transaction cancelation was aborted.")

    confirm_cancel()


def open_details_window(txn, parent_frame):
    top = Toplevel()
    top.title(f"Transaction")##{txn[0]}
    top.geometry("400x300")
    top.configure(bg="white")

    filename = os.path.basename(txn[1])
    size = txn[2].upper()
    copies = f"{txn[3]} COPIES"
    print_type = txn[4].upper()
    total = f"P{txn[7]}"
    status = txn[6].lower()

    main_frame = Frame(top, bg="white")
    main_frame.pack(expand=True, fill="both", padx=30, pady=30)

    top_row = Frame(main_frame, bg="white")
    top_row.pack(fill="x")

    Label(top_row, text=filename, bg="white", font=("Arial", 10, "bold")).pack(
        side="left"
    )
    right = Frame(top_row, bg="white")
    right.pack(side="right")

    Label(right, text="Your total bill", bg="white", font=("Arial", 8)).pack(anchor="e")
    Label(right, text=total, bg="white", fg="black", font=("Arial", 12, "bold")).pack(
        anchor="e"
    )

    Label(main_frame, text=size, bg="white", font=("Arial", 10)).pack(
        anchor="w", pady=(15, 3)
    )
    Label(main_frame, text=copies, bg="white", font=("Arial", 10)).pack(
        anchor="w", pady=3
    )
    Label(main_frame, text=print_type, bg="white", font=("Arial", 10)).pack(
        anchor="w", pady=3
    )

    if status == "pending":
        Button(
            main_frame,
            text="Cancel",
            bg="#801b16",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=lambda: cancel_transaction(txn[0], parent_frame),
        ).pack(pady=(20, 0))


def display_transactions(parent):
    for widget in parent.winfo_children():
        if widget != fab:
            widget.destroy()

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT transaction_id, file_path, size, copies, print_type, transaction_date, status, total
        FROM customer_transaction
        WHERE customer_id = %s
        ORDER BY transaction_date DESC
    """,
        (CURRENT_CUSTOMER_ID,),
    )
    transactions = cursor.fetchall()
    conn.close()

    if not transactions:
        Label(
            parent,
            text="No transactions...",
            bg="#f8f8f8",
            fg="gray",
            font=("Arial", 10),
        ).place(relx=0.5, rely=0.5, anchor="center")
        return

    for txn in transactions:
        filename = os.path.basename(txn[1])
        status_color = "green" if txn[6].lower() == "completed" else "black"

        frame = Frame(parent, bg="white", bd=1, relief="solid", cursor="hand2")
        frame.pack(fill="x", padx=10, pady=5)
        frame.bind("<Button-1>", lambda e, txn=txn: open_details_window(txn, frame))

        filename_label = Label(frame, text=filename, bg="white", font=("Arial", 10))
        filename_label.pack(side="left", padx=10, pady=5)
        filename_label.bind(
            "<Button-1>", lambda e, txn=txn: open_details_window(txn, frame)
        )

        status_label = Label(
            frame, text=txn[6], bg="white", fg=status_color, font=("Arial", 10, "bold")
        )
        status_label.pack(side="right", padx=10)
        status_label.bind(
            "<Button-1>", lambda e, txn=txn: open_details_window(txn, frame)
        )


def initialize_main_window(customer_id):
    global CURRENT_CUSTOMER_ID
    CURRENT_CUSTOMER_ID = customer_id

    pages = {"Notification": customer_notification, "Profile": customer_profile}
    icon_images = {}

    def load_icon(path, size=(20, 20)):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def load(page):
        for widget in content.winfo_children():
            widget.destroy()
        if page in pages:
            pages[page](content)

    def create_navbar(parent):
        navbar = Frame(parent, bg="white", height=50)
        navbar.pack(side="top", fill="x")
        navbar.pack_propagate(False)

        brand_label = Label(
            navbar,
            text="Hera Online Printing",
            bg="white",
            fg="black",
            font=("Arial", 12, "bold"),
        )
        brand_label.pack(side="left", padx=10)

        notif_icon = load_icon("assets/img/notification.png")
        profile_icon = load_icon("assets/img/profile.png")

        icon_images["notif"] = notif_icon
        icon_images["profile"] = profile_icon

        profile_btn = Label(navbar, image=profile_icon, bg="white", cursor="hand2")
        profile_btn.pack(side="right", padx=10, pady=10)
        profile_btn.bind("<Button-1>", lambda e: load("Profile"))

        notif_btn = Label(navbar, image=notif_icon, bg="white", cursor="hand2")
        notif_btn.pack(side="right", padx=10, pady=10)
        notif_btn.bind("<Button-1>", lambda e: load("Notification"))

    def create_main_content(parent):
        global content, fab
        content = Frame(parent, bg="#f8f8f8")
        content.pack(expand=True, fill="both")

        display_transactions(content)

        fab = Button(
            content,
            text="+",
            font=("Arial", 18, "bold"),
            bg="#123285",
            fg="white",
            activebackground="#0d245e",
            relief="flat",
            bd=0,
            width=3,
            height=1,
            cursor="hand2",
            command=lambda: open_transaction_popup(
                CURRENT_CUSTOMER_ID, refresh_transactions
            ),
        )
        fab.place(relx=0.95, rely=0.95, anchor="se")

    window = Tk()
    window.title("Hera Online Printing")
    window.geometry("900x500")
    window.configure(bg="white")

    create_navbar(window)
    create_main_content(window)

    window.mainloop()


def refresh_transactions():
    display_transactions(content)
    fab.place(relx=0.95, rely=0.95, anchor="se")
