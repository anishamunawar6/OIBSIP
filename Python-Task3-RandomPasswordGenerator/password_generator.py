import tkinter as tk
from tkinter import messagebox, ttk
import string
import secrets
import random
import pyperclip

history = []

def check_strength(password):

    strength = 0

    if len(password) >= 8:
        strength += 1

    if any(c.isupper() for c in password):
        strength += 1

    if any(c.islower() for c in password):
        strength += 1

    if any(c.isdigit() for c in password):
        strength += 1

    if any(c in string.punctuation for c in password):
        strength += 1

    if strength <= 2:
        strength_label.config(text="Strength: Weak", fg="red")

    elif strength <= 4:
        strength_label.config(text="Strength: Medium", fg="orange")

    else:
        strength_label.config(text="Strength: Strong", fg="green")

def copy_password():

    password = password_box.get()

    if password == "":
        messagebox.showwarning(
            "Warning",
            "Generate a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Success",
        "Password copied to clipboard!"
    )


# ------------------ Function ------------------ #
def generate_password():

    password_box.delete(0, tk.END)

    progress["value"] = 0
    progress.pack(pady=10)

    progress.start(15)

    root.after(1200, create_password)

def create_password():

    progress.stop()
    progress.pack_forget()

    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid password length.")
        return

    if length < 8:
        messagebox.showwarning("Warning", "Password length should be at least 8.")
        return

    selected_sets = []

    if upper_var.get():
        selected_sets.append(string.ascii_uppercase)

    if lower_var.get():
        selected_sets.append(string.ascii_lowercase)

    if number_var.get():
        selected_sets.append(string.digits)

    if symbol_var.get():
        selected_sets.append(string.punctuation)

    if not selected_sets:
        messagebox.showwarning("Warning", "Select at least one character type.")
        return

    if exclude_var.get():

        ambiguous = "0O1l"

        new_sets = []

        for chars in selected_sets:
            filtered = "".join(c for c in chars if c not in ambiguous)

            if filtered:
                new_sets.append(filtered)

        selected_sets = new_sets

    password = []

    for chars in selected_sets:
        password.append(secrets.choice(chars))

    all_characters = "".join(selected_sets)

    while len(password) < length:
        password.append(secrets.choice(all_characters))

    random.shuffle(password)

    final_password = "".join(password)

    password_box.insert(0, final_password)

    history.insert(0, final_password)

    if len(history) > 5:
        history.pop()

    history_box.delete(0, tk.END)

    for item in history:
        history_box.insert(tk.END, item)

    check_strength(final_password)

    progress["value"] = 0
    progress.pack_forget()
    progress.stop()
    progress.pack_forget()

# ------------------ Main Window ------------------ #

root = tk.Tk()
root.title("Random Password Generator")
root.geometry("580x690")
root.resizable(False, False)

# ------------------ Title ------------------ #

title = tk.Label(
    root,
    text="Random Password Generator 🔐",
    font=("Arial", 19, "bold")
)
title.pack(pady=15)

# ------------------ Password Length ------------------ #

length_label = tk.Label(root, text="Password Length:", font=("Arial", 14,"bold"))
length_label.pack()

length_entry = tk.Entry(root, font=("Arial", 11), width=15)
length_entry.pack(pady=5)

# ------------------ Checkboxes ------------------ #

upper_var = tk.BooleanVar()
lower_var = tk.BooleanVar()
number_var = tk.BooleanVar()
symbol_var = tk.BooleanVar()
exclude_var = tk.BooleanVar()

tk.Checkbutton(root, text="Uppercase Letters", variable=upper_var, font=("Arial", 12)).pack(anchor="w", padx=125)
tk.Checkbutton(root, text="Lowercase Letters", variable=lower_var, font=("Arial", 12)).pack(anchor="w", padx=125)
tk.Checkbutton(root, text="Numbers", variable=number_var, font=("Arial", 12)).pack(anchor="w", padx=125)
tk.Checkbutton(root, text="Symbols", variable=symbol_var, font=("Arial", 12)).pack(anchor="w", padx=125)
tk.Checkbutton(root, text="Exclude Ambiguous Characters(0,O,l,1)",variable=exclude_var,font=("Arial", 12)).pack(anchor="w", padx=125)

# ------------------ Button ------------------ #

generate_btn = tk.Button(
    root,
    text=" Generate Password",
    command=generate_password,
    font=("Arial", 14, "bold"),
    bg="green",
    fg="white",
    width=20
)
generate_btn.pack(pady=20)

copy_btn = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    bg="blue",
    fg="white",
    font=("Arial",14,"bold"),
    width=20
)

copy_btn.pack(pady=5)

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Black.Horizontal.TProgressbar",
    background="black",
    troughcolor="#D8CCFF"
)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=250,
    mode="indeterminate",
    style="Black.Horizontal.TProgressbar"
)

# ------------------ Output ------------------ #

password_box = tk.Entry(
    root,
    font=("Arial", 14),
    width=38,
    justify="center"
)
password_box.pack(pady=10)

strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 14, "bold")
)
strength_label.pack(pady=5)

history_label = tk.Label(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 14, "bold")
)
history_label.pack()

history_box = tk.Listbox(
    root,
    width=40,
    height=5,
    font=("Arial", 12)
)
history_box.pack(pady=5)



# ------------------ Run ------------------ #

root.mainloop()