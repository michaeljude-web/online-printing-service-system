from tkinter import *
from PIL import Image, ImageTk 
import subprocess

from admin_dashboard import dashboard
from admin_transaction import transaction
from admin_customer import customer
from admin_inventory import inventory
from admin_notification import notification
from admin_profile import profile

pages = {
    "Dashboard": dashboard,
    "Transaction": transaction,
    "Customer": customer,
    "Inventory": inventory,
    "Notification": notification,
    "Profile": profile
}

icon_images = {}

def load(page):
    for widget in content.winfo_children():
        widget.destroy()
    pages.get(page, lambda x: None)(content)


def logout_user():
    window.destroy()
    subprocess.Popen(["python", "admin_login.py"])

def load_icon(path, size=(16, 16)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)  
    icon = ImageTk.PhotoImage(img)
    return icon

def create_sidebar(parent, on_select):
    sidebar = Frame(parent, bg="white", width=230)
    sidebar.pack(side="left", fill="y")

    Label(sidebar,
          text="Hera Printing",
          bg="white",
          fg="black",
          font=("Arial", 14, "bold"),
          anchor="w",
          padx=20).pack(pady=(20, 30), fill="x")

    menu_sidebar = [
        ("assets/img/dashboard.png", "Dashboard"),
        ("assets/img/transaction.png", "Transaction"),
        ("assets/img/customer.png", "Customer"),
        ("assets/img/inventory.png", "Inventory")
    ]

    for icon_path, label in menu_sidebar:
        icon = load_icon(icon_path)
        icon_images[label] = icon  

        item = Label(sidebar,
                     text=f"{label}",
                     image=icon,
                     compound="left",
                     bg="white",
                     fg="black",
                     font=("Arial", 10),
                     anchor="w",
                     padx=20,
                     pady=10,
                     cursor="hand2")
        item.pack(fill="x")
        item.bind("<Button-1>", lambda e, l=label: on_select(l))

    Label(sidebar, bg="white").pack(expand=True, fill="both")

    logout_icon = load_icon("assets/img/logout.png") 
    icon_images["Logout"] = logout_icon

    logout = Label(sidebar,
                   text="Logout",
                   image=logout_icon,
                   compound="left",
                   bg="white",
                   fg="black",
                   font=("Arial", 10),
                   anchor="w",
                   padx=20,
                   pady=10,
                   cursor="hand2")
    logout.pack(fill="x", pady=(0, 20))
    logout.bind("<Button-1>", lambda e: logout_user())

def topbar(parent):
    topbar = Frame(parent,
                   bg="#f5f5f5",
                   height=50)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)

    notif_icon = load_icon("assets/img/notification.png")
    prof_icon = load_icon("assets/img/profile.png")
    icon_images["Notification"] = notif_icon
    icon_images["Profile"] = prof_icon
    
    profile_icon = Label(topbar,
                         image=prof_icon,
                         bg="#f5f5f5",
                         cursor="hand2")
    profile_icon.pack(side="right", padx=25, pady=10)
    profile_icon.bind("<Button-1>", lambda e: load("Profile"))

    notification_icon = Label(topbar,
                              image=notif_icon,
                              bg="#f5f5f5",
                              cursor="hand2")
    notification_icon.pack(side="right", padx=0, pady=10)
    notification_icon.bind("<Button-1>", lambda e: load("Notification"))


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
