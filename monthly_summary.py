
import sqlite3
from datetime import date


def show_monthly_summary():
    month = input(
        "Enter month (YYYY-MM), or press Enter for current month: "
    ).strip()

    if not month:
        month = date.today().strftime("%Y-%m")

    try:
        date.fromisoformat(month + "-01")
    except ValueError:
        print("Invalid month. Please use YYYY-MM, such as 2026-10.")
        return

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE
                WHEN transaction_type = 'Income' THEN amount
                ELSE 0
            END), 0),
            COALESCE(SUM(CASE
                WHEN transaction_type = 'Expense' THEN amount
                ELSE 0
            END), 0)
        FROM transactions
        WHERE substr(transaction_date, 1, 7) = ?
    """, (month,))

    total_income, total_expenses = cursor.fetchone()
    connection.close()

    balance = total_income - total_expenses

    print("\n" + "=" * 40)
    print(f"MONTHLY SUMMARY: {month}")
    print("=" * 40)
    print(f"Income:   ₹{total_income:,.2f}")
    print(f"Expenses: ₹{total_expenses:,.2f}")
    print("-" * 40)
    print(f"Balance:  ₹{balance:,.2f}")
    print("=" * 40)


if __name__ == "__main__":
    show_monthly_summary()
