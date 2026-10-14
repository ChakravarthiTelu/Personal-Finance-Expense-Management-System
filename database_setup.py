
import sqlite3

# Connect to the database file
connection = sqlite3.connect("finance.db")

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Create the transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    transaction_date TEXT NOT NULL
)
""")

# Save changes and close the connection
connection.commit()
connection.close()

print("Database created successfully!")
print("Transactions table is ready.")
