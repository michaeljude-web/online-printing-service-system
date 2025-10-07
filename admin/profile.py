import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
from database.db_connection import db_connection
from PIL import Image, ImageTk

current_admin_id = 1


def asset(path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", path)
    )


def profile(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    def update_profile():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        try:
            db = db_connection()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE admin SET email=%s, password=%s WHERE id=%s",
                (email, password, current_admin_id),
            )
            db.commit()
            messagebox.showinfo("Success", "Profile updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()

    container = Frame(parent, bg="white", bd=1, relief="solid", borderwidth=1)
    container.place(relx=0.5, rely=0.5, anchor="center", width=320, height=400)

    try:
        profile_image = Image.open(asset("img/profile.png"))
        profile_image = profile_image.resize((60, 60))
        profile_image_photo = ImageTk.PhotoImage(profile_image)
    except Exception as e:
        profile_image_photo = None

    profile_image_label = Label(container, image=profile_image_photo, bg="white")
    profile_image_label.image = profile_image_photo
    profile_image_label.pack(pady=(10, 10))

    greeting_label = Label(
        container,
        text="Hello, Admin",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#333",
    )
    greeting_label.pack(pady=(0, 15))

    change_info_label = Label(
        container,
        text="Do you want to change your email or password?",
        font=("Arial", 8),
        bg="white",
        fg="#333",
    )
    change_info_label.pack(pady=(10, 15))

    Label(
        container, text="Email", font=("Arial", 10), bg="white", fg="black", anchor="w"
    ).pack(fill="x", padx=30)
    email_entry = Entry(
        container, font=("Arial", 11), bd=1, bg="white", fg="black", relief="solid"
    )
    email_entry.pack(fill="x", padx=30, pady=(0, 10))

    Label(
        container,
        text="Password",
        font=("Arial", 10),
        bg="white",
        fg="black",
        anchor="w",
    ).pack(fill="x", padx=30)
    password_entry = Entry(
        container,
        font=("Arial", 11),
        bd=1,
        bg="white",
        fg="black",
        relief="solid",
        show="*",
    )
    password_entry.pack(fill="x", padx=30, pady=(0, 15))

    save_button = Button(
        container,
        text="Save Changes",
        bg="#1E3A8A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        command=update_profile,
    )
    save_button.pack(fill="x", padx=30, pady=5)

    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT email, password FROM admin WHERE id=%s", (current_admin_id,)
        )
        row = cursor.fetchone()
        if row:
            email_entry.insert(0, row[0])
            password_entry.insert(0, row[1])
        cursor.close()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")
