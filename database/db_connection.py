
import mysql.connector
from tkinter import messagebox

def db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hera_printing"
        )
        #messagebox.showinfo("Database Connection", "Connected successfullyy!")
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection", f"Error: {err}")
        return None
