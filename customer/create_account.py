import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
from database.db_connection import db_connection
import subprocess


def open_login():
    subprocess.Popen(["python", "login.py"])


def save_account(name, email, password, window):
    if not name or not email or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        mydb = db_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already registered")
            return

        query = (
            "INSERT INTO customer (full_name, email, password, status) "
            "VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(query, (name, email, password, "Pending"))
        mydb.commit()

        messagebox.showinfo(
            "Success", "Account created successfully! Please wait for admin approval."
        )
        window.destroy()
        open_login()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()


def create_account_screen():
    window = Tk()
    window.title("Hera Online Printing")
    window.geometry("900x500")
    window.configure(bg="white")

    container = Frame(
        window, bg="white", highlightbackground="#1E3A8A", highlightthickness=2
    )
    container.place(relx=0.5, rely=0.5, anchor="center", width=320, height=470)

    label1 = Label(
        container,
        text="Hera Online Printing",
        font=("Arial", 15, "bold"),
        bg="white",
        fg="black",
    )
    label1.pack(pady=(18, 5))
    label1.pack(anchor="center")

    label2 = Label(
        container, text="Create Account", font=("Arial", 18), bg="white", fg="black"
    )
    label2.pack(pady=(10, 35))
    label1.pack(anchor="center")

    label3 = Label(
        container, text="Full Name:", font=("Arial", 10), bg="white", fg="black"
    )
    label3.pack(anchor="w", padx=30)

    name_entry = Entry(
        container, font=("Arial", 10), bd=1, fg="black", relief="solid", bg="white"
    )
    name_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    label4 = Label(
        container, text="Email address:", font=("Arial", 10), bg="white", fg="black"
    )
    label4.pack(anchor="w", padx=30)

    email_entry = Entry(
        container, font=("Arial", 10), bd=1, fg="black", relief="solid", bg="white"
    )
    email_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    label5 = Label(
        container, text="Password:", font=("Arial", 10), bg="white", fg="black"
    )
    label5.pack(anchor="w", padx=30)

    password_entry = Entry(
        container, font=("Arial", 10), bd=1, relief="solid", bg="white", show="*"
    )
    password_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    create_btn = Button(
        container,
        text="Create Account",
        bg="#1E3A8A",
        fg="white",
        font=("Arial", 10),
        relief="flat",
        height=2,
        command=lambda: save_account(
            name_entry.get(), email_entry.get(), password_entry.get(), window
        ),
    )
    create_btn.pack(fill="x", padx=30, pady=(15, 10))

    center_frame = Frame(container, bg="white")
    center_frame.pack(pady=10)

    label_text = Label(
        center_frame,
        text="Already have an account?",
        fg="black",
        bg="white",
        font=("Arial", 9),
    )
    label_text.pack()

    login_label = Label(
        center_frame,
        text="Login here",
        fg="blue",
        bg="white",
        cursor="hand2",
        font=("Arial", 9, "underline"),
    )
    login_label.pack(anchor="center")

    login_label.bind("<Button-1>", lambda e: [window.destroy(), open_login()])

    window.mainloop()


create_account_screen()
