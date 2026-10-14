
import sqlite3


def show_summary():
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
    """)

    total_income, total_expenses = cursor.fetchone()
    connection.close()

    balance = total_income - total_expenses

    print("\n" + "=" * 35)
    print("       FINANCIAL SUMMARY")
    print("=" * 35)
    print(f"Total Income:    ₹{total_income:,.2f}")
    print(f"Total Expenses:  ₹{total_expenses:,.2f}")
    print("-" * 35)
    print(f"Remaining Balance: ₹{balance:,.2f}")
    print("=" * 35)


if __name__ == "__main__":
    show_summary()
