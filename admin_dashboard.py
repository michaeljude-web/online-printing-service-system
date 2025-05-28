from tkinter import *

def dashboard(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    container = Frame(parent, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=20)

    #--------------------------------------#
    left_frame = Frame(container, bg="#1e3a8a", width=200, bd=0)
    left_frame.pack(side="left", fill="y", padx=(0, 20))
    left_frame.pack_propagate(False)

    Label(left_frame, text="NEXT", bg="#1e3a8a", fg="white", font=("Arial", 10, "bold")).pack(pady=(10, 10))

    for _ in range(8):
        Label(left_frame, bg="white", height=2).pack(pady=5, padx=10, fill="x")

    #--------------------------------------#
    right_frame = Frame(container, bg="#f5f5f5")
    right_frame.pack(side="left", fill="both", expand=True)

    stats = [("PENDING", 0), ("COMPLETED", 0)]
    for i, (label, count) in enumerate(stats):
        box = Frame(right_frame, bg="white", highlightbackground="#1e3a8a", highlightthickness=1)
        box.grid(row=i//1, column=i%1, sticky="nsew", pady=10)
        box.grid_propagate(False)
        box.configure(width=150, height=100)

        Label(box, text=label, bg="white", fg="black", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        Label(box, text=str(count), bg="white", fg="black", font=("Arial", 16, "bold")).pack()

    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)
