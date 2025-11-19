import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

# Create the CSV file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Note"])


def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    note = note_var.get()

    if category == "" or amount == "":
        messagebox.showerror("Error", "Category and Amount are required!")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount, note])

    messagebox.showinfo("Success", "Expense added successfully!")
    
    amount_var.set("")
    note_var.set("")
    load_expenses()


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    total = 0

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)
            total += float(row[2])

    total_label.config(text=f"Total Expense: ₹{total}")


def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select an item to delete")
        return

    confirm = messagebox.askyesno("Delete", "Are you sure?")
    if not confirm:
        return

    selected_item = tree.item(selected)["values"]

    rows = []
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row != selected_item:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    load_expenses()


# GUI Window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")

tk.Label(root, text="Expense Tracker", font=("Arial", 18, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

# Input Fields
tk.Label(frame, text="Category:").grid(row=0, column=0)
category_var = tk.StringVar()
tk.Entry(frame, textvariable=category_var).grid(row=0, column=1)

tk.Label(frame, text="Amount:").grid(row=1, column=0)
amount_var = tk.StringVar()
tk.Entry(frame, textvariable=amount_var).grid(row=1, column=1)

tk.Label(frame, text="Note:").grid(row=2, column=0)
note_var = tk.StringVar()
tk.Entry(frame, textvariable=note_var).grid(row=2, column=1)

tk.Button(frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
tk.Button(frame, text="Delete Selected", command=delete_expense, bg="red", fg="white").grid(row=3, column=1, pady=10)

# Table
columns = ["Date", "Category", "Amount", "Note"]
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(pady=10)

# Total Label
total_label = tk.Label(root, text="Total Expense: ₹0", font=("Arial", 14))
total_label.pack(pady=10)

# Load expenses on start
load_expenses()

root.mainloop()
