from tkinter import *
from tkinter import messagebox
from db_connection import db_connection
import subprocess

def login(email, password, root):
    mydb = db_connection()
    if mydb:
        cursor = mydb.cursor()
        query = "SELECT * FROM admin WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        if result:
           # messagebox.showinfo("Login Success", "Welcome! shsh!")
            root.destroy()
            subprocess.Popen(["python", "admin_main.py"])
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
        cursor.close()
        mydb.close()


def login_screen():
    root = Tk()
    root.title("Hera Printing Login")
    root.geometry("900x500")
    root.configure(bg="white")

    container = Frame(root, bg="white",
                      highlightbackground="#1E3A8A",
                      highlightthickness=2)
    container.place(relx=0.5, rely=0.5, anchor="center", width=320, height=420)

    Label(container, text="Hera Online Printing",
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(pady=(20, 5))

    Label(container, text="Login",
          font=("Arial", 18), bg="white", fg="black").pack(pady=(0, 80))

    Label(container, text="Email address:",
          font=("Arial", 10), bg="white", fg="black").pack(anchor="w", padx=30)
    
    email_entry = Entry(container, font=("Arial", 10), bd=1,
                        fg="black", relief="solid", bg="white")
    email_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    Label(container, text="Password:",
          font=("Arial", 10), bg="white", fg="black").pack(anchor="w", padx=30)
    
    password_entry = Entry(container, font=("Arial", 10), bd=1,
                           relief="solid", bg="white", show="*")
    password_entry.pack(pady=5, ipady=6, fill="x", padx=30)

    login_btn = Button(container, text="Login",
                       bg="#1E3A8A", fg="white", font=("Arial", 10),
                       relief="flat", height=2,
                       command=lambda: login(email_entry.get(), password_entry.get(), root))
    login_btn.pack(fill="x", padx=30, pady=(15, 20))

    root.mainloop()

login_screen()
