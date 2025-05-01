import mysql.connector
import tkinter as tk
from tkinter import messagebox
from db_config import db_config
from gui import BankingApp

# === DATABASE CONNECTION ===
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
except mysql.connector.Error as err:
    print("Error connecting to the database:", err)
    exit()

# === MAIN GUI LAUNCH ===
# I struggled with importing the GUI the first time — forgot to actually implement mainloop()!
root = tk.Tk()
app = BankingApp(root, connection, cursor)
root.mainloop()

# Closing connection after the app is closed.
cursor.close()
connection.close()
