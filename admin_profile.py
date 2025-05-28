from tkinter import *
from tkinter import messagebox
from db_connection import db_connection

current_admin_id = 1  

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
            cursor.execute("UPDATE admin SET email=%s, password=%s WHERE id=%s",
                           (email, password, current_admin_id))
            db.commit()
            messagebox.showinfo("Success", "Profile updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()

    wrapper = Frame(parent, bg="white", bd=2, relief="groove")
    wrapper.place(relx=0.5, rely=0.4, anchor="center", width=320, height=250)

    Label(wrapper, text="Update Profile", font=("Arial", 14, "bold"),
          bg="white", fg="#1E3A8A").pack(pady=(15, 5))


    Label(wrapper, text="Email", font=("Arial", 10), bg="white", fg="black", anchor="w").pack(fill="x", padx=30)
    email_entry = Entry(wrapper, font=("Arial", 11), bd=1,bg="white", fg="black", relief="solid")
    email_entry.pack(fill="x", padx=30, pady=(0, 10))

    Label(wrapper, text="Password", font=("Arial", 10), bg="white", fg="black", anchor="w").pack(fill="x", padx=30)
    password_entry = Entry(wrapper, font=("Arial", 11), bd=1, bg="white", fg="black", relief="solid", show="*")
    password_entry.pack(fill="x", padx=30, pady=(0, 15))

    Button(wrapper, text="Save Changes",
           bg="#1E3A8A", fg="white",
           font=("Arial", 10, "bold"),
           relief="flat", command=update_profile).pack(pady=5)


    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT email, password FROM admin WHERE id=%s", (current_admin_id,))
        row = cursor.fetchone()
        if row:
            email_entry.insert(0, row[0])
            password_entry.insert(0, row[1])
        cursor.close()
        db.close()
    except:
        pass
