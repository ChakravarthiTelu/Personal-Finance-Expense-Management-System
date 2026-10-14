
import sqlite3
from datetime import date


def create_budget_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            monthly_limit REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(category, month)
        )
    """)


def set_budget():
    month = input(
        "Enter month (YYYY-MM), or press Enter for current month: "
    ).strip()

    if not month:
        month = date.today().strftime("%Y-%m")

    try:
        date.fromisoformat(month + "-01")
    except ValueError:
        print("Invalid month. Use YYYY-MM, such as 2026-10.")
        return

    category = input("Budget category (e.g. Food): ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    try:
        limit = float(input("Monthly budget limit (₹): "))
        if limit <= 0:
            print("Budget must be greater than zero.")
            return
    except ValueError:
        print("Enter a valid number.")
        return

    connection = sqlite3.connect("finance.db")
    create_budget_table(connection)

    connection.execute("""
        INSERT INTO budgets (category, monthly_limit, month)
        VALUES (?, ?, ?)
        ON CONFLICT(category, month)
        DO UPDATE SET monthly_limit = excluded.monthly_limit
    """, (category, limit, month))

    connection.commit()
    connection.close()

    print("Budget saved successfully!")
    check_budget(category, month)


def check_budget(category, month):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT monthly_limit
        FROM budgets
        WHERE category = ? COLLATE NOCASE AND month = ?
    """, (category, month))
    result = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE transaction_type = 'Expense'
          AND category = ? COLLATE NOCASE
          AND substr(transaction_date, 1, 7) = ?
    """, (category, month))
    spent = cursor.fetchone()[0]

    connection.close()

    if result is None:
        print("No budget found for this category and month.")
        return

    limit = result[0]
    remaining = limit - spent

    print(f"\nBudget for {category} ({month})")
    print(f"Budget limit: ₹{limit:,.2f}")
    print(f"Amount spent: ₹{spent:,.2f}")
    print(f"Remaining: ₹{remaining:,.2f}")

    if remaining < 0:
        print("ALERT: You have exceeded your budget!")
    elif remaining == 0:
        print("ALERT: You have reached your budget limit.")
    else:
        print("You are within your budget.")


if __name__ == "__main__":
    set_budget()
