import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import messagebox
import subprocess
from database.db_connection import db_connection
import dashboard


def open_dashboard(customer_id):
    dashboard.initialize_main_window(customer_id)


def open_create_account():
    subprocess.Popen(["python", "create_account.py"])


def login(email, password, window):
    try:
        mydb = db_connection()
        if mydb:
            cursor = mydb.cursor()
            query = "SELECT * FROM customer WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()

            if result:
                customer_id = result[0]
                status = result[5]
                if status == "Pending":
                    messagebox.showinfo(
                        "Account Pending", "Please wait for admin approval."
                    )
                elif status == "Approved":
                    window.destroy()
                    open_dashboard(customer_id)
                else:
                    messagebox.showerror("Login Failed", f"Account status: {status}")
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")

            cursor.close()
            mydb.close()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def login_screen():
    window = Tk()
    window.title("Hera Printing Login")
    window.geometry("900x500")
    window.configure(bg="white")

    container = Frame(
        window, bg="white", highlightbackground="#1E3A8A", highlightthickness=2
    )
    container.place(relx=0.5, rely=0.5, anchor="center", width=320, height=420)

    Label(
        container,
        text="Hera Online Printing",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black",
    ).pack(pady=(20, 5))

    Label(container, text="Login", font=("Arial", 18), bg="white", fg="black").pack(
        pady=(0, 80)
    )

    Label(
        container, text="Email address:", font=("Arial", 10), bg="white", fg="black"
    ).pack(anchor="w", padx=30)
    email_entry = Entry(
        container, font=("Arial", 10), bd=1, fg="black", relief="solid", bg="white"
    )
    email_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    Label(container, text="Password:", font=("Arial", 10), bg="white", fg="black").pack(
        anchor="w", padx=30
    )
    password_entry = Entry(
        container,
        font=("Arial", 10),
        fg="black",
        bd=1,
        relief="solid",
        bg="white",
        show="*",
    )
    password_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    login_btn = Button(
        container,
        text="Login",
        bg="#1E3A8A",
        fg="white",
        font=("Arial", 10),
        relief="flat",
        height=2,
        command=lambda: login(email_entry.get(), password_entry.get(), window),
    )
    login_btn.pack(fill="x", padx=30, pady=(15, 10))

    account_label_frame = Frame(container, bg="white")
    account_label_frame.pack()

    label_text = Label(
        account_label_frame,
        text="Does not have account? ",
        fg="black",
        bg="white",
        font=("Arial", 9),
    )
    label_text.pack()

    create_account_label = Label(
        account_label_frame,
        text="Create here",
        fg="#1E3A8A",
        bg="white",
        cursor="hand2",
        font=("Arial", 9, "underline"),
    )
    create_account_label.pack(anchor="center")

    create_account_label.bind(
        "<Button-1>", lambda e: [window.destroy(), open_create_account()]
    )

    window.mainloop()


def open_login_window():
    login_screen()


if __name__ == "__main__":
    open_login_window()
