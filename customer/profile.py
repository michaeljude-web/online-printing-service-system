import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
from database.db_connection import db_connection
from PIL import Image, ImageTk


def asset(path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", path)
    )


def update_password(customer_id, new_password, old_password):
    conn = db_connection()
    try:
        cursor = conn.cursor()
        query = """
        SELECT password FROM customer WHERE customer_id = %s
        """
        cursor.execute(query, (customer_id,))
        current_password = cursor.fetchone()

        if current_password and current_password[0] == old_password:
            update_query = """
            UPDATE customer
            SET password = %s
            WHERE customer_id = %s
            """
            cursor.execute(update_query, (new_password, customer_id))
            conn.commit()
            return True
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def get_full_name(customer_id):
    conn = db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT full_name FROM customer WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        return result[0] if result else "User"
    except Exception as e:
        print("Error fetching full name:", e)
        return "User"
    finally:
        cursor.close()
        conn.close()


def profile(parent, customer_id):
    for widget in parent.winfo_children():
        widget.destroy()

    full_name = get_full_name(customer_id)

    form_frame = Frame(parent, bg="white", padx=20, pady=20, bd=1, relief="solid")
    form_frame.pack(padx=20, pady=20)

    form_frame.grid_rowconfigure(0, weight=1)
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=3)

    user_icon = Image.open(asset("img/profile.png"))
    user_icon = user_icon.resize((50, 50))
    user_icon_photo = ImageTk.PhotoImage(user_icon)

    user_icon_label = Label(form_frame, image=user_icon_photo, bg="white")
    user_icon_label.image = user_icon_photo
    user_icon_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    greeting_label = Label(
        form_frame,
        text=f"Hello, {full_name}",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#333",
    )
    greeting_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

    change_password_label = Label(
        form_frame,
        text="Do you want to change your password?",
        font=("Arial", 12),
        bg="white",
        fg="#333",
    )
    change_password_label.grid(row=2, columnspan=2, pady=(10, 10))

    Label(
        form_frame,
        text="Old Password:",
        bg="white",
        fg="black",
        anchor="w",
        font=("Arial", 12),
    ).grid(row=3, column=0, sticky="w", pady=5)
    old_password_entry = Entry(
        form_frame,
        font=("Arial", 12),
        show="*",
        width=30,
        bd=1,
        relief="solid",
        borderwidth=1,
    )
    old_password_entry.grid(row=3, column=1, pady=5)

    Label(
        form_frame,
        text="New Password:",
        bg="white",
        fg="black",
        anchor="w",
        font=("Arial", 12),
    ).grid(row=4, column=0, sticky="w", pady=5)
    new_password_entry = Entry(
        form_frame,
        font=("Arial", 12),
        show="*",
        width=30,
        bd=1,
        relief="solid",
        borderwidth=1,
    )
    new_password_entry.grid(row=4, column=1, pady=5)

    def save_changes():
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()

        if not old_password or not new_password:
            messagebox.showwarning("Input Error", "Both fields are required.")
            return

        success = update_password(customer_id, new_password, old_password)

        if success:
            messagebox.showinfo("Success", "Password updated successfully!")
            old_password_entry.delete(0, END)
            new_password_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Old password is incorrect.")

    save_button = Button(
        form_frame,
        text="Save Changes",
        font=("Arial", 12),
        bg="darkblue",
        fg="white",
        command=save_changes,
    )
    save_button.grid(row=5, columnspan=2, pady=20, sticky="ew")
