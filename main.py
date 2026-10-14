
import sqlite3
import add_transaction
import view_transactions
import financial_summary
import monthly_summary
import budget_manager
import search_transactions


def initialize_database():
    connection = sqlite3.connect("finance.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def main():
    initialize_database()

    while True:
        print("\n" + "=" * 45)
        print(" PERSONAL FINANCE & EXPENSE MANAGEMENT")
        print("=" * 45)
        print("1. Add income or expense")
        print("2. View all transactions")
        print("3. View financial summary")
        print("4. View monthly summary")
        print("5. Set monthly budget")
        print("6. Search Transactions")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            add_transaction.add_transaction()
        elif choice == "2":
            view_transactions.view_transactions()
        elif choice == "3":
            financial_summary.show_summary()
        elif choice == "4":
            monthly_summary.show_monthly_summary()
        elif choice == "5":
            budget_manager.set_budget()
        elif choice == "6":
            search_transactions.search_transactions()
        elif choice == "7":
            print("Thank you for using the Finance System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
