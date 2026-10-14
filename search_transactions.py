
import sqlite3


def search_transactions():
    print("\n--- SEARCH TRANSACTIONS ---")
    print("Leave a field blank to ignore that filter.")

    transaction_type = input(
        "Type (Income/Expense): "
    ).strip().capitalize()

    if transaction_type and transaction_type not in ("Income", "Expense"):
        print("Enter Income, Expense, or leave blank.")
        return

    category = input("Category: ").strip()
    month = input("Month (YYYY-MM): ").strip()

    if month:
        if len(month) != 7 or month[4] != "-":
            print("Use YYYY-MM format, such as 2026-10.")
            return

        try:
            import datetime
            datetime.date.fromisoformat(month + "-01")
        except ValueError:
            print("Invalid month.")
            return

    query = """
        SELECT id, transaction_type, amount, category,
               description, transaction_date
        FROM transactions
        WHERE 1 = 1
    """
    parameters = []

    if transaction_type:
        query += " AND transaction_type = ?"
        parameters.append(transaction_type)

    if category:
        query += " AND category = ? COLLATE NOCASE"
        parameters.append(category)

    if month:
        query += " AND substr(transaction_date, 1, 7) = ?"
        parameters.append(month)

    query += " ORDER BY transaction_date DESC, id DESC"

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()

    if not results:
        print("No matching transactions found.")
        return

    print("\n--- SEARCH RESULTS ---")
    for item in results:
        print("-" * 35)
        print(f"ID: {item[0]} | {item[1]} | ₹{item[2]:,.2f}")
        print(f"Category: {item[3]}")
        print(f"Description: {item[4]}")
        print(f"Date: {item[5]}")


if __name__ == "__main__":
    search_transactions()
