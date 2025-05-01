import mysql.connector  # type: ignore
import random
import os
import time

# ================================
# CONNECT TO MYSQL
# ================================
# Make sure to update your MySQL credentials if needed. 
# The database 'bank_user_info' should already exist, created by the 'initialize_db.py' script.

connection = mysql.connector.connect(
    host='localhost',  # Database host
    user='root',       # MySQL username
    password='K092509s',  # MySQL password (Change if necessary)
    database='bank_user_info'  # Database name (Ensure it's the correct one created by initialize_db.py)
)
cursor = connection.cursor()

# ================================
# MAIN FUNCTIONS
# ================================

def intro():
    """
    Displays the main menu and asks the user for their choice.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal for a clean interface
    print("Welcome to the Elite Bank! Please choose an option:")
    options = [
        'Create an account',
        'Delete an account',
        'Modify an account',
        'Check balance',
        'Withdraw',
        'Deposit'
    ]
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("-1. Exit")
    return input("Your choice: ")

def uniqueRandint():
    """
    Generates a unique PIN (random number) that doesn't already exist in the database.
    """
    sql = "SELECT PIN FROM user_info"
    cursor.execute(sql)
    existing_pins = {row[0] for row in cursor.fetchall()}  # Get all existing PINs from the database
    while True:
        temp = random.randint(123456, 999999)  # Generate a random 6-digit number
        if temp not in existing_pins:  # Ensure the generated PIN is unique
            return temp

def getRow(user_PIN):
    """
    Fetches a row from the database based on the user PIN.
    """
    sql = "SELECT * FROM user_info WHERE PIN = %s"
    cursor.execute(sql, (user_PIN,))
    return cursor.fetchone()

def confirm():
    """
    Asks the user to confirm an action (yes/no).
    """
    choice = input("Are you sure you want to do this? (yes/no): ").lower()
    if choice == 'yes':
        return True
    else:
        print("Returning to main menu...")
        time.sleep(2)
        main()  # If the user cancels, return to the main menu

def creating_acc():
    """
    Allows the user to create a new account with a unique PIN, full name, birthdate, SSN, and phone number.
    """
    user_name = input("Full name: ")
    user_birth_date = input("Birth date (mm/dd/yyyy): ")
    user_SSN = input("Social Security Number (#########): ")
    user_phone_number = input("Phone number (##########): ")
    randomNum = uniqueRandint()  # Generate a unique PIN

    # Validate the inputs
    if len(user_name) > 45:
        print("Name must be 45 characters or less.")
        return
    if len(user_birth_date) != 10:
        print("Please use the correct date format.")
        return
    if len(user_phone_number) != 10 or not user_phone_number.isdigit():
        print("Invalid phone number.")
        return

    if confirm():  # If user confirms, create the account
        sql = """INSERT INTO user_info (name, date, SSN, number, PIN, balance)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        val = (user_name, user_birth_date, user_SSN, user_phone_number, randomNum, 0)  # Default balance is 0
        cursor.execute(sql, val)
        connection.commit()

        user_acc = getRow(randomNum)
        attributes = ['\nAccount ID', 'Name', 'Date', 'SSN', 'Phone', 'PIN', 'Balance']
        for attr, val in zip(attributes, user_acc):
            print(f"{attr}: {val}")
        print("\nWARNING: You won't see this info again.")
        input("Press Enter to continue...")

def deleting_acc():
    """
    Deletes a user account based on the provided PIN.
    """
    user_PIN = input("Enter your PIN: ")
    if confirm():  # Ask for confirmation before deleting
        sql = "DELETE FROM user_info WHERE PIN = %s"
        cursor.execute(sql, (user_PIN,))
        connection.commit()
        if cursor.rowcount > 0:
            print("Account deleted successfully.")
        else:
            print("No account found with that PIN.")
        time.sleep(2)

def modify_acc():
    """
    Modify a user's account details such as name, date of birth, SSN, or phone number.
    """
    user_PIN = input("Enter your PIN: ")

    print("Which detail would you like to update?")
    options = ['name', 'date', 'SSN', 'number']  # Fields available for modification
    for o in options:
        print(o)

    choice = input("Attribute to update: ").lower()
    if choice not in options:
        print("Invalid choice.")
        return

    old_val = input(f"Current {choice}: ")
    new_val = input(f"New {choice}: ")

    if confirm():  # Ask for confirmation before modifying
        sql = f"UPDATE user_info SET {choice} = %s WHERE PIN = %s AND {choice} = %s"
        val = (new_val, user_PIN, old_val)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{choice} updated successfully.")
        else:
            print("No matching data found.")

def check_balance():
    """
    Checks the balance for the user based on their PIN.
    """
    try:
        user_PIN = int(input("Enter your PIN: "))  # Validate PIN input
    except ValueError:
        print("PIN must be a number.")
        return

    if confirm():  # Ask for confirmation before showing balance
        row = getRow(user_PIN)
        if row:
            print(f"Your balance is: ${row[-1]}")  # The balance is in the last column of the row
        else:
            print("No account found.")
        time.sleep(2)

def change_balance(user_input):
    """
    Handles both withdrawals and deposits.
    """
    user_PIN = input("Enter your PIN: ")
    row = getRow(user_PIN)

    if not row:
        print("No account found.")
        return

    try:
        amount = int(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    if confirm():  # Ask for confirmation before changing balance
        current_balance = row[-1]
        new_balance = current_balance - amount if user_input == '5' else current_balance + amount

        if new_balance < 0:
            print("Insufficient funds.")
            return

        sql = "UPDATE user_info SET balance = %s WHERE PIN = %s"
        cursor.execute(sql, (new_balance, user_PIN))
        connection.commit()
        print(f"New balance: ${new_balance}")
        time.sleep(2)

def main():
    """
    Main driver function that displays the menu and handles user input.
    """
    while True:
        choice = intro()
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == '1':
            creating_acc()
        elif choice == '2':
            deleting_acc()
        elif choice == '3':
            modify_acc()
        elif choice == '4':
            check_balance()
        elif choice in ['5', '6']:
            change_balance(choice)
        elif choice == '-1':
            print("Thanks for using Elite Bank!")
            break
        else:
            print("Invalid option. Try again.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
