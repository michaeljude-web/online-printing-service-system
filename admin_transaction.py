from tkinter import *

def transaction(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="white")

    Label(parent, text="Transaction List", font=("Arial", 12, "bold"), bg="white", fg="black").pack(anchor="w", padx=20, pady=10)

    name = "Ariana Grande"

    def open_transaction(name):
        for widget in parent.winfo_children():
            widget.destroy()

        parent.configure(bg="white")

        box = Frame(parent,
                    bg="white",
                    bd=1,
                    relief="solid")
        box.pack(padx=40,
                 pady=30,
                 fill="both",
                 expand=True)

        Label(box,
              text=name.upper(),
              font=("Arial", 10, "bold"),
              bg="white", fg="black").pack(anchor="w", padx=20, pady=(10, 5))

        Label(box,
              text="APP DEV PAPERS.pdf",
              bg="white", fg="black").pack(anchor="w", padx=30)
        Label(box,
              text="LONG BOND PAPER",
              bg="white", fg="black").pack(anchor="w", padx=30)
        Label(box, text="3 COPIES",
              bg="white", fg="black").pack(anchor="w", padx=30)
        Label(box, text="COLORED",
              bg="white", fg="black").pack(anchor="w", padx=30)

        Label(box, text="Total bill",
              bg="white",
              fg="black").pack(anchor="e",
                               padx=40, pady=(10, 0))
        Label(box, text="₱125",
              font=("Arial", 10, "bold"),
              bg="white",
              fg="black").pack(anchor="e", padx=40)

        button_frame = Frame(box,
                             bg="white")
        button_frame.pack(pady=20)
        Button(button_frame, text="Decline",
               bg="white",
               fg="black",
               width=10).pack(side="left", padx=10)
        Button(button_frame, text="Accept",
               bg="white", fg="black", width=10).pack(side="left", padx=10)


    name_label = Label(parent,
                       text=name,
                       font=("Arial", 11),
                       fg="black", bg="white",
                       cursor="hand2")
    name_label.pack(anchor="w", padx=30, pady=5)
    
   # <hr>
    Frame(parent, height=1, bg="gray").pack(fill="x", padx=30, pady=(0, 5))

    name_label.bind("<Button-1>", lambda e, n=name: open_transaction(n))
