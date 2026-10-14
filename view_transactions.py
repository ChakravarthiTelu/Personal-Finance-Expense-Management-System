
import sqlite3


def view_transactions():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, transaction_type, amount, category,
               description, transaction_date
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """)

    transactions = cursor.fetchall()
    connection.close()

    print("\n--- ALL TRANSACTIONS ---")

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print("-" * 40)
        print("ID:", transaction[0])
        print("Type:", transaction[1])
        print("Amount: ₹", transaction[2])
        print("Category:", transaction[3])
        print("Description:", transaction[4])
        print("Date:", transaction[5])


if __name__ == "__main__":
    view_transactions()
