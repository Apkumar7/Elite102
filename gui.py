import tkinter as tk
from tkinter import messagebox

class BankingApp:
    def __init__(self, master, connection, cursor):
        self.master = master
        self.connection = connection
        self.cursor = cursor
        master.title("Elite Bank System")

        # I originally used `.grid()` and `.pack()` together — caused layout bugs!
        self.label = tk.Label(master, text="Welcome to Elite Bank!")
        self.label.pack()

        self.create_btn = tk.Button(master, text="Create Account", command=self.create_account)
        self.create_btn.pack()

        self.delete_btn = tk.Button(master, text="Delete Account", command=self.delete_account)
        self.delete_btn.pack()

        self.check_btn = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.check_btn.pack()

    def create_account(self):
        # Simple input window — I had a bug here where I forgot to .commit() the insert.
        def submit():
            name = name_entry.get()
            date = dob_entry.get()
            ssn = ssn_entry.get()
            phone = phone_entry.get()
            pin = pin_entry.get()
            sql = "INSERT INTO user_info (name, date, SSN, number, PIN, balance) VALUES (%s, %s, %s, %s, %s, 0)"
            self.cursor.execute(sql, (name, date, ssn, phone, pin))
            self.connection.commit()
            messagebox.showinfo("Success", "Account created successfully.")
            popup.destroy()

        popup = tk.Toplevel(self.master)
        tk.Label(popup, text="Full Name").pack()
        name_entry = tk.Entry(popup)
        name_entry.pack()

        tk.Label(popup, text="DOB (mm/dd/yyyy)").pack()
        dob_entry = tk.Entry(popup)
        dob_entry.pack()

        tk.Label(popup, text="SSN").pack()
        ssn_entry = tk.Entry(popup)
        ssn_entry.pack()

        tk.Label(popup, text="Phone Number").pack()
        phone_entry = tk.Entry(popup)
        phone_entry.pack()

        tk.Label(popup, text="PIN").pack()
        pin_entry = tk.Entry(popup, show="*")
        pin_entry.pack()

        tk.Button(popup, text="Submit", command=submit).pack()

    def delete_account(self):
        def submit():
            pin = pin_entry.get()
            self.cursor.execute("DELETE FROM user_info WHERE PIN = %s", (pin,))
            self.connection.commit()
            messagebox.showinfo("Deleted", "Account deleted if it existed.")
            popup.destroy()

        popup = tk.Toplevel(self.master)
        tk.Label(popup, text="Enter PIN").pack()
        pin_entry = tk.Entry(popup, show="*")
        pin_entry.pack()
        tk.Button(popup, text="Delete", command=submit).pack()

    def check_balance(self):
        def submit():
            pin = pin_entry.get()
            self.cursor.execute("SELECT balance FROM user_info WHERE PIN = %s", (pin,))
            result = self.cursor.fetchone()
            if result:
                messagebox.showinfo("Balance", f"Your balance is ${result[0]}")
            else:
                messagebox.showerror("Error", "Account not found.")
            popup.destroy()

        popup = tk.Toplevel(self.master)
        tk.Label(popup, text="Enter PIN").pack()
        pin_entry = tk.Entry(popup, show="*")
        pin_entry.pack()
        tk.Button(popup, text="Check", command=submit).pack()
