import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from database.db_connection import db_connection
from PIL import Image, ImageTk, ImageDraw
import subprocess

from dashboard import dashboard
from transaction import transaction
from customer import customer
from inventory import inventory
from notification import notification
from profile import profile


def asset(path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", path)
    )


icon_images = {}


def load(page):
    for widget in content.winfo_children():
        widget.destroy()
    pages.get(page, lambda x: None)(content)


def logout_user():
    window.destroy()
    subprocess.Popen(["python", "login.py"])


def load_icon(path, size=(16, 16)):
    img = Image.open(asset(path))
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def create_notification_icon_with_dot(icon_path, has_unread=False, size=(16, 16)):
    try:
        img = Image.open(asset(icon_path))
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
        img = Image.open(asset(icon_path))
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)


pages = {
    "Dashboard": dashboard,
    "Transaction": transaction,
    "Customer": customer,
    "Inventory": inventory,
    "Notification": notification,
    "Profile": profile,
}


def create_sidebar(parent, on_select):
    sidebar = Frame(parent, bg="white", width=230)
    sidebar.pack(side="left", fill="y")

    Label(
        sidebar,
        text="Hera Printing",
        bg="white",
        fg="black",
        font=("Arial", 14, "bold"),
        anchor="w",
        padx=20,
    ).pack(pady=(20, 30), fill="x")

    menu_sidebar = [
        ("img/dashboard.png", "Dashboard"),
        ("img/transaction.png", "Transaction"),
        ("img/customer.png", "Customer"),
        ("img/inventory.png", "Inventory"),
    ]

    for icon_path, label in menu_sidebar:
        icon = load_icon(icon_path)
        icon_images[label] = icon

        item = Label(
            sidebar,
            text=f"{label}",
            image=icon,
            compound="left",
            bg="white",
            fg="black",
            font=("Arial", 10),
            anchor="w",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        item.pack(fill="x")
        item.bind("<Button-1>", lambda e, l=label: on_select(l))

    Label(sidebar, bg="white").pack(expand=True, fill="both")

    logout_icon = load_icon("img/logout.png")
    icon_images["Logout"] = logout_icon

    logout = Label(
        sidebar,
        text="Logout",
        image=logout_icon,
        compound="left",
        bg="white",
        fg="black",
        font=("Arial", 10),
        anchor="w",
        padx=20,
        pady=10,
        cursor="hand2",
    )
    logout.pack(fill="x", pady=(0, 20))
    logout.bind("<Button-1>", lambda e: logout_user())


def topbar(parent):
    global notif_btn_widget

    def has_unread_notifications():
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM customer_transaction WHERE status = 'pending'"
            )
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count > 0
        except:
            return False

    def mark_notifications_read():
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE customer_transaction SET status = 'read' WHERE status = 'pending'"
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error updating notification status:", e)

    def update_notification_icon():
        has_unread = has_unread_notifications()
        new_icon = create_notification_icon_with_dot("img/notification.png", has_unread)
        icon_images["Notification"] = new_icon
        if "notif_btn_widget" in globals():
            notif_btn_widget.configure(image=new_icon)

    topbar = Frame(parent, bg="#f5f5f5", height=50)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)

    prof_icon = load_icon("img/profile.png")
    icon_images["Profile"] = prof_icon

    profile_icon = Label(topbar, image=prof_icon, bg="#f5f5f5", cursor="hand2")
    profile_icon.pack(side="right", padx=25, pady=10)
    profile_icon.bind("<Button-1>", lambda e: load("Profile"))

    has_unread = has_unread_notifications()
    notif_icon = create_notification_icon_with_dot("img/notification.png", has_unread)
    icon_images["Notification"] = notif_icon

    notif_btn_widget = Label(topbar, image=notif_icon, bg="#f5f5f5", cursor="hand2")
    notif_btn_widget.pack(side="right", padx=10, pady=10)

    def on_notification_click(event):
        load("Notification")
        mark_notifications_read()
        update_notification_icon()

    notif_btn_widget.bind("<Button-1>", on_notification_click)

    def refresh_notification_icon():
        update_notification_icon()
        topbar.after(5000, refresh_notification_icon)

    refresh_notification_icon()


window = Tk()
window.title("Hera Printing Online")
window.geometry("900x500")
window.configure(bg="#f5f5f5")

create_sidebar(window, load)
topbar(window)

content = Frame(window)
content.pack(expand=True, fill="both", padx=(17, 17))

load("Dashboard")

window.mainloop()
