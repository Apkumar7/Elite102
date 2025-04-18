import tkinter as tk
from tkinter import messagebox, simpledialog
from db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

def login(user_id, pin):
    cursor.execute("SELECT user_id, name, is_admin FROM users WHERE user_id = %s AND pin = %s", (user_id, pin))
    return cursor.fetchone()

def check_balance(user_id):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def deposit(user_id, amount):
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()

def withdraw(user_id, amount):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]
    if amount > balance:
        return False
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    return True

def create_account(name, pin):
    cursor.execute("INSERT INTO users (name, pin, is_admin) VALUES (%s, %s, FALSE)", (name, pin))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, 0.00)", (user_id,))
    conn.commit()
    return user_id

def delete_account(user_id):
    cursor.execute("DELETE FROM accounts WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()

def modify_account(user_id, new_name, new_pin):
    cursor.execute("UPDATE users SET name = %s, pin = %s WHERE user_id = %s", (new_name, new_pin, user_id))
    conn.commit()

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elite Bank Login")
        self.user_id = None
        self.is_admin = False
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="User ID").grid(row=0, column=0)
        tk.Label(self.root, text="PIN").grid(row=1, column=0)

        self.user_entry = tk.Entry(self.root)
        self.pin_entry = tk.Entry(self.root, show="*")

        self.user_entry.grid(row=0, column=1)
        self.pin_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login_action).grid(row=2, column=0, columnspan=2)

    def login_action(self):
        uid = self.user_entry.get()
        pin = self.pin_entry.get()
        result = login(uid, pin)
        if result:
            self.user_id = int(result[0])
            self.is_admin = result[2]
            self.root.title(f"Elite Bank - Welcome, {result[1]}")
            if self.is_admin:
                self.admin_menu()
            else:
                self.user_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or PIN")

    def user_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="User Menu", font=("Helvetica", 14)).pack()
        tk.Button(self.root, text="Check Balance", command=self.gui_check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit", command=self.gui_deposit).pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=self.gui_withdraw).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def admin_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Menu", font=("Helvetica", 14)).pack()
        tk.Button(self.root, text="Create Account", command=self.gui_create_account).pack(pady=5)
        tk.Button(self.root, text="Delete Account", command=self.gui_delete_account).pack(pady=5)
        tk.Button(self.root, text="Modify Account", command=self.gui_modify_account).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def gui_check_balance(self):
        balance = check_balance(self.user_id)
        messagebox.showinfo("Balance", f"Your balance is ${balance:.2f}")

    def gui_deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount:
            deposit(self.user_id, amount)
            messagebox.showinfo("Success", "Deposit completed.")

    def gui_withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount:
            if withdraw(self.user_id, amount):
                messagebox.showinfo("Success", "Withdrawal successful.")
            else:
                messagebox.showwarning("Failed", "Insufficient funds.")

    def gui_create_account(self):
        name = simpledialog.askstring("Create", "Enter name:")
        pin = simpledialog.askstring("Create", "Enter PIN:")
        if name and pin:
            new_id = create_account(name, pin)
            messagebox.showinfo("Created", f"Account created. User ID: {new_id}")

    def gui_delete_account(self):
        uid = simpledialog.askinteger("Delete", "Enter User ID to delete:")
        if uid:
            delete_account(uid)
            messagebox.showinfo("Deleted", "Account deleted.")

    def gui_modify_account(self):
        uid = simpledialog.askinteger("Modify", "Enter User ID:")
        name = simpledialog.askstring("Modify", "Enter new name:")
        pin = simpledialog.askstring("Modify", "Enter new PIN:")
        if uid and name and pin:
            modify_account(uid, name, pin)
            messagebox.showinfo("Modified", "Account updated.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
