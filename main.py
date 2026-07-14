import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from database import create_database, save_record, get_records, get_bmi_data

# BMI calculate karne ka function
def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight aur height positive honi chahiye")
            return
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            color = "green"

        elif bmi < 30:
            category = "Overweight"
            color = "orange"

        else:
            category = "Obese"
            color = "red"

        result_label.config(
            text=f"{name}, Your BMI is {bmi:.2f}\nCategory: {category}",
            fg=color
        )
         # Save Data in Database
        save_record(
            name,
            weight,
            height,
            bmi,
            category
        )
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height"
        )

def show_history():

    records = get_records()

    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("500x400")

    history_text = tk.Text(
        history_window,
        width=60,
        height=20
    )

    history_text.pack(pady=20)

    if records:
        for record in records:
            history_text.insert(
                tk.END,
                f"Name: {record[1]}\n"
                f"Weight: {record[2]} kg\n"
                f"Height: {record[3]} m\n"
                f"BMI: {record[4]:.2f}\n"
                f"Category: {record[5]}\n"
                f"Date: {record[6]}\n"
                "----------------------\n"
            )
    else:
        history_text.insert(
            tk.END,
            "No records found"
        )

def show_graph():

    data = get_bmi_data()

    if not data:
        messagebox.showinfo(
            "No Data",
            "No BMI records available"
        )
        return

    dates = []
    bmi_values = []

    for item in data:
        dates.append(item[0])
        bmi_values.append(item[1])


    plt.figure(figsize=(8, 4))

    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.title("BMI Trend")

    plt.xlabel("Date")

    plt.ylabel("BMI")

    plt.xticks(
        rotation=45
    )

    plt.grid()

    plt.tight_layout()

    plt.show()

# Database start
create_database()

# Main Window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x400")
window.config(bg="white")

# Heading
title = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 20, "bold"),
    bg="white"
)
title.pack(pady=20)

# Name
tk.Label(window, text="Name", bg="white").pack()
name_entry = tk.Entry(window)
name_entry.pack()

# Weight
tk.Label(window, text="Weight (kg)", bg="white").pack()
weight_entry = tk.Entry(window)
weight_entry.pack()

# Height
tk.Label(window, text="Height (meter)", bg="white").pack()
height_entry = tk.Entry(window)
height_entry.pack()

# Button
calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="black",
    fg="white"
)
calculate_button.pack(pady=20)

history_button = tk.Button(
    window,
    text="View History",
    command=show_history,
    bg="gray",
    fg="white"
)
history_button.pack(pady=10)

graph_button = tk.Button(
    window,
    text="Show BMI Graph",
    command=show_graph,
    bg="green",
    fg="white"
)
graph_button.pack(pady=10)

# Result
result_label = tk.Label(
    window,
    text="",
    font=("Arial", 12, "bold"),
    bg="white"
)

result_label.pack()

# Run app
window.mainloop()