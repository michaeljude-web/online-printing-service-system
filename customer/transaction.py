import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from database.db_connection import db_connection


def transaction_open(customer_id, callback=None):
    popup = Toplevel()
    popup.title("Hera Online Printing - New Transaction")
    popup.geometry("500x500")
    popup.configure(bg="#f9f9f9")
    popup.grab_set()

    form_frame = Frame(popup, bg="#faf9f6", bd=1, relief="solid", padx=20, pady=20)
    form_frame.pack(expand=True, fill="none", anchor="center", padx=20, pady=20)

    file_path_var = StringVar()
    total_value = DoubleVar(value=0.00)

    def upload_file():
        filepath = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf")]
        )
        if filepath:
            file_path_var.set(filepath)
            file_btn.config(text=os.path.basename(filepath))

    def compute_total(*args):
        try:
            copies = int(copies_entry.get())
        except ValueError:
            total_label.config(text="Total: ₱0.00")
            total_value.set(0.00)
            return

        size = size_combo.get()
        color = color_type.get()

        price_table = {
            "bw": {"A4 BOND PAPER": 2, "SHORT BOND PAPER": 1, "LONG BOND PAPER": 3},
            "colored": {
                "A4 BOND PAPER": 5,
                "SHORT BOND PAPER": 3,
                "LONG BOND PAPER": 5,
            },
        }

        if size in price_table[color]:
            rate = price_table[color][size]
            total = copies * rate
            total_value.set(total)
            total_label.config(text=f"Total: ₱{total:.2f}")
        else:
            total_value.set(0.00)
            total_label.config(text="Total: ₱0.00")

    def submit_transaction():
        file = file_path_var.get()
        size = size_combo.get()
        try:
            copies = int(copies_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of copies.")
            return
        color = color_type.get()
        total = total_value.get()

        if not file or not os.path.exists(file):
            messagebox.showerror("Error", "Please select a valid file.")
            return

        if size == "Select size":
            messagebox.showerror("Error", "Please select a valid paper size.")
            return

        try:
            conn = db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO customer_transaction 
                (customer_id, file_path, size, copies, print_type, total, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            """,
                (customer_id, file, size, copies, color, total),
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Transaction submitted successfully.")
            popup.destroy()

            if callback:
                callback()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    label_font = ("Arial", 10)
    input_width = 35

    Label(form_frame, text="File", font=label_font, bg="#faf9f6", anchor="w").grid(
        row=0, column=0, sticky="w", pady=(0, 2)
    )

    file_btn = Button(
        form_frame,
        text="Select file",
        width=input_width,
        relief="solid",
        command=upload_file,
    )

    file_btn.grid(row=1, column=0, columnspan=2, pady=5)

    Label(
        form_frame, text="Paper Size", font=label_font, bg="#faf9f6", anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=(10, 2))
    size_combo = ttk.Combobox(
        form_frame,
        values=["A4 BOND PAPER", "SHORT BOND PAPER", "LONG BOND PAPER"],
        state="readonly",
        width=input_width - 2,
    )
    size_combo.set("Select size")
    size_combo.grid(row=3, column=0, columnspan=2, pady=5)
    size_combo.bind("<<ComboboxSelected>>", compute_total)

    Label(
        form_frame, text="Number of Copies", font=label_font, bg="#faf9f6", anchor="w"
    ).grid(row=4, column=0, sticky="w", pady=(10, 2))
    copies_entry = Entry(form_frame, width=input_width, relief="solid")
    copies_entry.grid(row=5, column=0, columnspan=2, pady=5)
    copies_entry.bind("<KeyRelease>", compute_total)

    Label(
        form_frame, text="Color Type", font=label_font, bg="#faf9f6", anchor="w"
    ).grid(row=6, column=0, sticky="w", pady=(10, 2))
    color_type = StringVar(value="bw")
    Radiobutton(
        form_frame,
        text="Black & White",
        variable=color_type,
        value="bw",
        bg="#faf9f6",
        command=compute_total,
    ).grid(row=7, column=0, sticky="w", pady=2)
    Radiobutton(
        form_frame,
        text="Colored",
        variable=color_type,
        value="colored",
        bg="#faf9f6",
        command=compute_total,
    ).grid(row=7, column=1, sticky="w", pady=2)

    total_label = Label(
        form_frame,
        text="Total: ₱0.00",
        font=("Arial", 12, "bold"),
        bg="#faf9f6",
        fg="#123285",
    )
    total_label.grid(row=8, column=0, columnspan=2, pady=15)

    send_btn = Button(
        form_frame,
        text="Send",
        width=input_width,
        bg="#123285",
        fg="white",
        relief="flat",
        command=submit_transaction,
    )
    send_btn.grid(row=9, column=0, columnspan=2, pady=10)
