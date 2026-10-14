# Personal Finance & Expense Management System

## Project Overview
A personal finance application built using Python, SQLite, Pandas, and Streamlit. It helps users track income and expenses, manage monthly budgets, analyze spending patterns, and generate financial reports through an interactive dashboard.

## Features
- Add, edit, and delete financial transactions
- Track income, expenses, and account balance
- Filter transactions by category, type, month, and date range
- Visualize expenses by category
- Compare monthly income and expenses
- Set monthly budgets and monitor spending
- Receive alerts when spending reaches or exceeds a budget
- View transaction history
- Export transaction data and monthly reports as CSV files
- Interactive dashboard with financial summary cards

## Technologies Used
- Python
- SQLite
- Streamlit
- Pandas
- Data Visualization
- CSV

## Project Structure
- `main.py` — Main program
- `database_setup.py` — Database setup
- `check_database.py` — Database checking utility
- `add_transaction.py` — Add transactions
- `view_transactions.py` — View transactions
- `financial_summary.py` — Financial summary
- `monthly_summary.py` — Monthly reports
- `budget_manager.py` — Budget management
- `search_transactions.py` — Search transactions
- `dashboard.py` — Interactive Streamlit dashboard
- `requirements.txt` — Python dependencies
- `.gitignore` — Files excluded from GitHub

## Installation and Usage

1. Install Python 3.13 or a compatible Python version.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install the required packages:

   `python -m pip install -r requirements.txt`

5. Set up the database by following the instructions in `database_setup.py`.
6. Start the dashboard:

   `python -m streamlit run dashboard.py`

7. Open the local URL displayed in the terminal.

## Learning Outcomes
- Python programming and database operations
- CRUD operations using SQLite
- Data analysis using Pandas
- Interactive dashboard development with Streamlit
- Budget tracking and financial reporting
- CSV data export

## Author
Telu Dheera Guru Chakravarthi
B.Tech Graduate | Python & Data Analytics Enthusiast