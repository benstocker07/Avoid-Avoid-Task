import tkinter as tk
from tkinter import messagebox
import hashlib

RESEARCHER_PASSWORD_HASH = "234cf664e88e4d71259b60319f4ee2104c9715f037d7d5ba69d014fabea0d321"

def check_password(event=None):
    entered = entry.get()
    entered_hash = hashlib.sha256(entered.encode()).hexdigest()
    if entered_hash == RESEARCHER_PASSWORD_HASH:
        root.destroy()
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")
        entry.delete(0, tk.END)

def on_closing():
    messagebox.showwarning("Action Denied", "You must login to access the task")
root = tk.Tk()
root.iconbitmap(default="")
root.title("Password Entry")
root.configure(bg="white")

window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

frame = tk.Frame(root, bg="white")
frame.pack(expand=True, fill="both")

tk.Label(frame, text="Enter Researcher Password:", bg="white", fg="#333", font=("Arial", 14)).pack(pady=20)
entry = tk.Entry(frame, show="*", font=("Arial", 14), justify="center")
entry.pack(pady=10)
entry.focus()

tk.Button(frame, text="Submit", command=check_password, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.bind("<Return>", check_password)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
