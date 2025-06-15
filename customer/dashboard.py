import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from database.db_connection import db_connection
from transaction import transaction_open
from notification import notification
from profile import profile


def asset(path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", path)
    )


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

                show_txn(content)

            except Exception as e:
                print(f"Error occurred while canceling transaction: {e}")
        else:
            print("Transaction cancelation was aborted.")

    confirm_cancel()


def open_details_window(txn, parent_frame):
    top = Toplevel()
    top.title(f"Transaction")
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

    Label(main_frame, text=filename, bg="white", font=("Arial", 10, "bold")).pack(
        anchor="w"
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

    Label(
        main_frame,
        text=f"TOTAL: {total}",
        bg="white",
        font=("Arial", 12, "bold"),
        fg="black",
    ).pack(anchor="w", pady=(20, 0))

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


def check_unread_notifications(customer_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM customer_transaction 
            WHERE customer_id = %s 
            AND status IN ('completed', 'read', 'declined') 
            AND (is_read IS NULL OR is_read = FALSE)
        """,
            (customer_id,),
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error checking unread notifications: {e}")
        return False


def mark_notifications_as_read(customer_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE customer_transaction 
            SET is_read = TRUE 
            WHERE customer_id = %s 
            AND status IN ('completed', 'read', 'declined')
            AND (is_read IS NULL OR is_read = FALSE)
        """,
            (customer_id,),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error marking notifications as read: {e}")


def create_notification_icon_with_dot(icon_path, has_unread=False, size=(20, 20)):
    try:
        img = Image.open(icon_path)
        img = img.resize(size, Image.Resampling.LANCZOS)

        if has_unread:
            img = img.convert("RGBA")
            draw = ImageDraw.Draw(img)
            dot_size = 6
            x = size[0] - dot_size - 2
            y = 2
            draw.ellipse(
                [x, y, x + dot_size, y + dot_size], fill="red", outline="darkred"
            )

        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error creating notification icon: {e}")
        img = Image.open(icon_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)


def show_txn(parent):
    for widget in parent.winfo_children():
        if widget != fab:
            widget.destroy()

    scroll_frame = Frame(parent, bg="#f8f8f8")
    scroll_frame.pack(fill="both", expand=True)

    canvas = Canvas(scroll_frame, bg="#f8f8f8")
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scroll_content = Frame(canvas, bg="#f8f8f8")

    scroll_content.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scroll_content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def configure_scroll_content(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", configure_scroll_content)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", on_mousewheel)

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
            scroll_content,
            text="No transactions...",
            bg="#f8f8f8",
            fg="gray",
            font=("Arial", 10),
        ).pack(pady=50)
        return

    for txn in transactions:
        filename = os.path.basename(txn[1])

        status_lower = txn[6].lower()
        if status_lower == "completed":
            text_color = "white"
            bg_color = "#4CAF50"
        elif status_lower == "pending":
            text_color = "white"
            bg_color = "#FFA500"
        elif status_lower == "read":
            text_color = "white"
            bg_color = "#2196F3"
        else:
            text_color = "white"
            bg_color = "#F44336"

        frame = Frame(scroll_content, bg="white", bd=1, relief="solid", cursor="hand2")
        frame.pack(fill="x", padx=10, pady=5)
        frame.bind("<Button-1>", lambda e, txn=txn: open_details_window(txn, frame))

        filename_label = Label(frame, text=filename, bg="white", font=("Arial", 10))
        filename_label.pack(side="left", padx=10, pady=5)
        filename_label.bind(
            "<Button-1>", lambda e, txn=txn: open_details_window(txn, frame)
        )

        status_label = Label(
            frame,
            text=f"{txn[6].upper()}",
            bg=bg_color,
            fg=text_color,
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
            pady=2,
            width=12,
            anchor="center",
        )
        status_label.pack(side="right", padx=10, pady=5)
        status_label.bind(
            "<Button-1>", lambda e, txn=txn: open_details_window(txn, frame)
        )


def initialize_main_window(customer_id):
    global CURRENT_CUSTOMER_ID, notif_btn_widget, icon_images
    CURRENT_CUSTOMER_ID = customer_id

    pages = {"Notification": notification, "Profile": profile}
    icon_images = {}

    def load_icon(path, size=(20, 20)):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def update_notification_icon():
        has_unread = check_unread_notifications(CURRENT_CUSTOMER_ID)
        new_icon = create_notification_icon_with_dot(
            asset("img/notification.png"), has_unread
        )
        icon_images["notif"] = new_icon
        if "notif_btn_widget" in globals():
            notif_btn_widget.configure(image=new_icon)

    def load(page):
        for widget in content.winfo_children():
            widget.destroy()
        if page in pages:
            if page == "Notification":
                mark_notifications_as_read(CURRENT_CUSTOMER_ID)
                update_notification_icon()
            pages[page](content, CURRENT_CUSTOMER_ID)

    def logout(window):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            window.destroy()
            import login

            login.open_login_window()

    def create_navbar(parent):
        global notif_btn_widget
        navbar = Frame(parent, bg="white", height=50)
        navbar.pack(side="top", fill="x")
        navbar.pack_propagate(False)

        brand_label = Label(
            navbar,
            text="Hera Printing",
            bg="white",
            fg="black",
            font=("Arial", 12, "bold"),
        )
        brand_label.pack(side="left", padx=10)
        brand_label.bind("<Button-1>", lambda e: show_txn(content))

        has_unread = check_unread_notifications(CURRENT_CUSTOMER_ID)
        notif_icon = create_notification_icon_with_dot(
            asset("img/notification.png"), has_unread
        )
        profile_icon = load_icon(asset("img/profile.png"))
        logout_icon = load_icon(asset("img/logout.png"))

        icon_images["notif"] = notif_icon
        icon_images["profile"] = profile_icon
        icon_images["logout"] = logout_icon

        logout_btn = Label(navbar, image=logout_icon, bg="white", cursor="hand2")
        logout_btn.pack(side="right", padx=10, pady=10)
        logout_btn.bind("<Button-1>", lambda e: logout(parent))

        profile_btn = Label(navbar, image=profile_icon, bg="white", cursor="hand2")
        profile_btn.pack(side="right", padx=10, pady=10)
        profile_btn.bind("<Button-1>", lambda e: load("Profile"))

        notif_btn_widget = Label(navbar, image=notif_icon, bg="white", cursor="hand2")
        notif_btn_widget.pack(side="right", padx=10, pady=10)
        notif_btn_widget.bind("<Button-1>", lambda e: load("Notification"))

    def create_main_content(parent):
        global content, fab
        content = Frame(parent, bg="#f8f8f8")
        content.pack(expand=True, fill="both")

        show_txn(content)

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
            command=lambda: transaction_open(CURRENT_CUSTOMER_ID, refresh_transactions),
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
    show_txn(content)
    fab.place(relx=0.95, rely=0.95, anchor="se")

    if "CURRENT_CUSTOMER_ID" in globals():
        has_unread = check_unread_notifications(CURRENT_CUSTOMER_ID)
        new_icon = create_notification_icon_with_dot(
            asset("img/notification.png"), has_unread
        )
        icon_images["notif"] = new_icon
        if "notif_btn_widget" in globals():
            notif_btn_widget.configure(image=new_icon)
