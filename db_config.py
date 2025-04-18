import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",        # Replace with your MySQL username
        password="your_mysql_password",# Replace with your MySQL password
        database="bank_system"
    )
