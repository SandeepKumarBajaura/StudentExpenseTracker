# Student Expense Tracker
# Records daily expenses and calculates total spending

import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import date
import matplotlib.pyplot as plt

FILE = "expenses.csv"


class ExpenseTracker:
    def __init__(self, root):
        self.expenses = []          # list of dictionaries
        root.title("Student Expense Tracker")

        # Input widgets (grid geometry manager)
        tk.Label(root, text="Item").grid(row=0, column=0, padx=5, pady=5)
        self.item = tk.Entry(root)
        self.item.grid(row=0, column=1)

        tk.Label(root, text="Category").grid(row=1, column=0)
        self.category = tk.StringVar(value="Food")
        tk.OptionMenu(root, self.category, "Food", "Travel", "Books", "Fun", "Other").grid(row=1, column=1, sticky="w")

        tk.Label(root, text="Amount").grid(row=2, column=0)
        self.amount = tk.Entry(root)
        self.amount.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Delete Selected", command=self.delete_expense).grid(row=3, column=1)
        tk.Button(root, text="Show Pie Chart", command=self.show_chart).grid(row=3, column=2)

        # List of expenses and total
        self.listbox = tk.Listbox(root, width=55)
        self.listbox.grid(row=4, column=0, columnspan=3, padx=5)
        self.total_label = tk.Label(root, text="Total: Rs 0", font=("Arial", 12, "bold"))
        self.total_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.load_data()
        self.refresh()

    def add_expense(self):
        name = self.item.get().strip()
        try:
            amt = float(self.amount.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        if name == "" or amt <= 0:
            messagebox.showerror("Error", "Enter item name and amount greater than 0")
            return

        self.expenses.append({"date": str(date.today()), "item": name,
                              "category": self.category.get(), "amount": amt})
        self.save_data()
        self.refresh()
        self.item.delete(0, tk.END)
        self.amount.delete(0, tk.END)

    def delete_expense(self):
        selected = self.listbox.curselection()
        if selected:
            self.expenses.pop(selected[0])
            self.save_data()
            self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        total = 0
        for e in self.expenses:
            self.listbox.insert(tk.END, f"{e['date']} | {e['item']} | {e['category']} | Rs {e['amount']}")
            total += e["amount"]
        self.total_label.config(text=f"Total: Rs {total}")

    def show_chart(self):
        totals = {}                 # category -> total amount
        for e in self.expenses:
            totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
        if not totals:
            messagebox.showinfo("Info", "No expenses to show")
            return
        plt.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%")
        plt.title("Spending by Category")
        plt.show()

    def save_data(self):
        with open(FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "item", "category", "amount"])
            writer.writeheader()
            writer.writerows(self.expenses)

    def load_data(self):
        if os.path.exists(FILE):
            with open(FILE) as f:
                for row in csv.DictReader(f):
                    row["amount"] = float(row["amount"])
                    self.expenses.append(row)


root = tk.Tk()
ExpenseTracker(root)
root.mainloop()
