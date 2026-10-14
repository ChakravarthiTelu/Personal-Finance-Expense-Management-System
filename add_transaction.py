
import sqlite3
from datetime import date


def add_transaction():
    print("\n--- Add Income or Expense ---")

    transaction_type = input("Type (Income/Expense): ").strip().capitalize()

    if transaction_type not in ("Income", "Expense"):
        print("Invalid type. Enter Income or Expense.")
        return

    try:
        amount = float(input("Amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    category = input("Category: ").strip()
    description = input("Description: ").strip()
    transaction_date = input(
        f"Date (YYYY-MM-DD, press Enter for {date.today()}): "
    ).strip()

    if not category:
        print("Category cannot be empty.")
        return

    if not transaction_date:
        transaction_date = date.today().isoformat()

    try:
        date.fromisoformat(transaction_date)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (transaction_type, amount, category, description, transaction_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        amount,
        category,
        description,
        transaction_date
    ))

    connection.commit()
    connection.close()

    print("Transaction saved successfully!")


if __name__ == "__main__":
    add_transaction()
