import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pkg_resources
import threading
import pygame
import time

import Authentication

def update_status(message, percent_value):
    global percent
    percent = percent_value
    status_label.config(text=message)
    progress_bar['value'] = percent
    percent_label.config(text=f"{percent}%")
    root.update_idletasks()

def installation_and_joystick_check():
    packages_to_install = [
        "pygame", "pandas", "pymysql", "statsmodels",
        "seaborn", "numpy", "matplotlib", "scipy", "joystick"
    ]

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    package_to_find = None

    update_status(f"Checking dependencies...", 10)
    time.sleep(1)
    
    if package_to_find not in installed_packages:
        progress = 20
        increment = int(80 / len(packages_to_install))

        for package in packages_to_install:
            progress = min(progress + increment, 80)
            update_status(f"Importing {package}...", progress)
            try:
                subprocess.check_call(["pip", "install", package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}")
            except FileNotFoundError as e:
                    subprocess.check_call(["pip3", "install", package])
                    print(f"Successfully installed {package}")
                    
    else:
        print("Pygame is already installed.")
        update_status("All packages already installed.", 80)
        time.sleep(1)

    update_status("Initialising Dependencies...", 80)
    pygame.init()
    time.sleep(0.3)

    update_status("Initialising joystick module...", 90)
    pygame.joystick.init()
    time.sleep(0.3)

    update_status("Checking for joysticks...", 95)
    joystick_count = pygame.joystick.get_count()
    time.sleep(0.3)

    if joystick_count < 1:
        messagebox.showerror("Joystick Error", "Joystick not connected.")
        root.destroy()
        exit()

    try:
        update_status("Connecting to joystick...", 97)
        update_status(f"Joystick connected", 100)
    except pygame.error as e:
        messagebox.showerror("Joystick Error", f"Could not initialize joystick: {e}")
        root.destroy()
        exit()

    root.after(2000, root.destroy)

def start_thread():
    thread = threading.Thread(target=installation_and_joystick_check)
    thread.start()

root = tk.Tk()
root.title("rJORT Setup")
root.geometry("400x120")
root.resizable(False, False)
root.configure(bg="white")
root.attributes("-topmost", True)

root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

status_label = tk.Label(root, bg="white", text="Preparing installation...", font=("Arial", 12))
status_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)
progress_bar['maximum'] = 100

percent_label = tk.Label(root, bg="white", text="0%", font=("Arial", 10))
percent_label.pack()

percent = 0
root.after(99, start_thread)
update_status("Welcome to the task!\n\n It is now loading the required files.", 0)
time.sleep(5)
root.mainloop()
