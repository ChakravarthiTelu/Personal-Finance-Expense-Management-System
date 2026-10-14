
import sqlite3
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st


# Use the database stored beside this Python file
DB_PATH = Path(__file__).with_name("finance.db")

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
    /* Main application background */
    .stApp {
        background-color: #0B1220;
        color: #E5EDF7;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111C2F;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #F1F5F9 !important;
    }

    /* Normal text */
    p, label, .stMarkdown {
        color: #CBD5E1;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background-color: #16243A;
        border: 1px solid #263B55;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #2DD4BF !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        background-color: #0F766E;
        color: white;
        border: 1px solid #2DD4BF;
        border-radius: 8px;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #115E59;
        color: white;
        border-color: #5EEAD4;
    }

    /* Expanders and bordered sections */
    [data-testid="stExpander"] {
        background-color: #111C2F;
        border: 1px solid #263B55;
        border-radius: 10px;
    }

    /* Links */
    a {
        color: #5EEAD4 !important;
    }

    /* Dividers */
    hr {
        border-color: #263B55;
    }
</style>
""", unsafe_allow_html=True)



def load_transactions():
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(
            """
            SELECT id, transaction_type, amount, category,
                   description, transaction_date
            FROM transactions
            ORDER BY transaction_date DESC, id DESC
            """,
            connection
        )


st.title("💰 Personal Finance Dashboard")

with st.expander("➕ Add a new transaction", expanded=False):
    with st.form("add_transaction_form"):
        transaction_type = st.selectbox(
            "Transaction type",
            ["Income", "Expense"]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=500.0,
            step=100.0
        )

        category = st.text_input(
            "Category",
            placeholder="e.g. Salary, Food, Travel"
        )

        description = st.text_input(
            "Description",
            placeholder="e.g. Monthly salary"
        )

        transaction_date = st.date_input(
            "Transaction date",
            value=date.today()
        )

        submitted = st.form_submit_button("Save transaction")

        if submitted:
            if not category.strip():
                st.error("Please enter a category.")
            else:
                with sqlite3.connect(DB_PATH) as connection:
                    connection.execute(
                        """
                        INSERT INTO transactions
                        (transaction_type, amount, category,
                         description, transaction_date)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            transaction_type,
                            amount,
                            category.strip(),
                            description.strip(),
                            transaction_date.isoformat()
                        )
                    )

                st.success("Transaction saved successfully!")
                st.rerun()

st.caption("Track your income, expenses, and savings.")

if not DB_PATH.exists():
    st.error("Database not found. Check your project folder.")
    st.stop()

df = load_transactions()

if df.empty:
    st.info("No transactions yet. Add income or expenses first.")
    st.stop()

# Convert dates and amounts to usable data types
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"], errors="coerce"
)
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna(subset=["transaction_date", "amount"])

# Sidebar filters
st.sidebar.header("Filter Transactions")

months = sorted(
    df["transaction_date"].dt.strftime("%Y-%m").unique(),
    reverse=True
)

selected_month = st.sidebar.selectbox(
    "Select month",
    ["All months"] + months
)

categories = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)

selected_types = st.sidebar.multiselect(
    "Transaction type",
    ["Income", "Expense"],
    default=["Income", "Expense"]
)

st.sidebar.subheader("Date Range")

min_date = df["transaction_date"].min().date()
max_date = df["transaction_date"].max().date()

start_date = st.sidebar.date_input(
    "Start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)




filtered_df = df[
    df["category"].isin(selected_categories)
    & df["transaction_type"].isin(selected_types)
    & (df["transaction_date"].dt.date >= start_date)
    & (df["transaction_date"].dt.date <= end_date)
].copy()



if selected_month != "All months":
    filtered_df = filtered_df[
        filtered_df["transaction_date"].dt.strftime("%Y-%m")
        == selected_month
    ]

# Calculate summary
income = filtered_df.loc[
    filtered_df["transaction_type"] == "Income", "amount"
].sum()

expenses = filtered_df.loc[
    filtered_df["transaction_type"] == "Expense", "amount"
].sum()

balance = income - expenses

# KPI cards

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.metric(
        label="💰 Total Income",
        value=f"₹{income:,.2f}",
        border=True
    )

with col2:
    st.metric(
        label="💸 Total Expenses",
        value=f"₹{expenses:,.2f}",
        border=True
    )

with col3:
    st.metric(
        label="📈 Balance",
        value=f"₹{balance:,.2f}",
        border=True
    )

st.divider()

st.subheader("🎯 Monthly Budget Tracker")

with sqlite3.connect(DB_PATH) as connection:
    budgets_df = pd.read_sql_query(
        """
        SELECT category, monthly_limit, month
        FROM budgets
        ORDER BY month DESC, category
        """,
        connection
    )

if budgets_df.empty:
    st.info(
        "No budgets found. Use the main menu to set a monthly budget first."
    )
else:
    available_months = sorted(
        budgets_df["month"].unique(),
        reverse=True
    )

    budget_month = st.selectbox(
        "Select budget month",
        available_months
    )

    month_budgets = budgets_df[
        budgets_df["month"] == budget_month
    ]

    for _, budget in month_budgets.iterrows():
        category_name = budget["category"]
        budget_limit = float(budget["monthly_limit"])

        spent = filtered_df.loc[
            (filtered_df["transaction_type"] == "Expense")
            & (
                filtered_df["category"].str.lower()
                == category_name.lower()
            )
            & (
                filtered_df["transaction_date"].dt.strftime("%Y-%m")
                == budget_month
            ),
            "amount"
        ].sum()

        remaining = budget_limit - spent

        st.markdown(f"**{category_name}** — {budget_month}")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Budget", f"₹{budget_limit:,.2f}")
        col_b.metric("Spent", f"₹{spent:,.2f}")
        col_c.metric("Remaining", f"₹{remaining:,.2f}")

        progress = min(spent / budget_limit, 1.0)
        st.progress(progress)

        if remaining < 0:
            st.error(
                f"⚠️ Budget exceeded by ₹{abs(remaining):,.2f}!"
            )
        elif remaining == 0:
            st.warning("You've reached your budget limit.")
        else:
            st.success(
                f"You're within budget. ₹{remaining:,.2f} remaining."
            )

        st.divider()


# Charts

st.subheader("📈 Financial Analytics")

left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### Expenses by Category")

    expense_data = filtered_df[
        filtered_df["transaction_type"] == "Expense"
    ]

    if expense_data.empty:
        st.info("No expenses for these filters.")
    else:
        category_totals = (
            expense_data.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(
            category_totals,
            color="#2DD4BF",
            horizontal=True
        )

with right:
    st.markdown("#### Income vs Expenses")

    comparison = pd.Series({
        "Income": income,
        "Expenses": expenses
    })

    st.bar_chart(
        comparison,
        color="#2DD4BF"
    )

# Transaction table


st.subheader("📊 Monthly Financial Report")

monthly_report = df.copy()

monthly_report["Month"] = (
    monthly_report["transaction_date"].dt.strftime("%Y-%m")
)

monthly_income = (
    monthly_report[monthly_report["transaction_type"] == "Income"]
    .groupby("Month")["amount"]
    .sum()
)

monthly_expenses = (
    monthly_report[monthly_report["transaction_type"] == "Expense"]
    .groupby("Month")["amount"]
    .sum()
)

report = pd.DataFrame({
    "Income": monthly_income,
    "Expenses": monthly_expenses
}).fillna(0)

report["Balance"] = report["Income"] - report["Expenses"]
report = report.sort_index(ascending=False)

st.dataframe(
    report.style.format("₹{:,.2f}"),
    width="stretch"
)

report_csv = report.to_csv(index=True).encode("utf-8")

st.download_button(
    label="📥 Download Monthly Financial Report",
    data=report_csv,
    file_name="monthly_financial_report.csv",
    mime="text/csv"
)
st.subheader("Transaction History")

st.caption(
    f"Showing {len(filtered_df)} transactions for your current filters."
)


st.subheader("✏️ Manage Transactions")


with sqlite3.connect(DB_PATH) as connection:
    all_transactions = pd.read_sql_query(
        """
        SELECT id, transaction_type, amount, category,
               description, transaction_date
        FROM transactions
        ORDER BY id DESC
        """,
        connection
    )

if all_transactions.empty:
    st.info("There are no transactions to manage.")
else:
    transaction_ids = all_transactions["id"].tolist()

    selected_id = st.selectbox(
        "Select transaction ID",
        transaction_ids
    )

    selected_transaction = all_transactions[
        all_transactions["id"] == selected_id
    ].iloc[0]

    with st.form("edit_transaction_form"):
        edit_type = st.selectbox(
            "Transaction type",
            ["Income", "Expense"],
            index=["Income", "Expense"].index(
                selected_transaction["transaction_type"]
            )
        )

        edit_amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=float(selected_transaction["amount"]),
            step=100.0
        )

        edit_category = st.text_input(
            "Category",
            value=str(selected_transaction["category"])
        )

        edit_description = st.text_input(
            "Description",
            value=str(selected_transaction["description"] or "")
        )

        edit_date = st.date_input(
            "Transaction date",
            value=pd.to_datetime(
                selected_transaction["transaction_date"]
            ).date()
        )

        update_clicked = st.form_submit_button("Update transaction")

        if update_clicked:
            if not edit_category.strip():
                st.error("Category cannot be empty.")
            else:
                with sqlite3.connect(DB_PATH) as connection:
                    connection.execute(
                        """
                        UPDATE transactions
                        SET transaction_type = ?, amount = ?,
                            category = ?, description = ?,
                            transaction_date = ?
                        WHERE id = ?
                        """,
                        (
                            edit_type,
                            edit_amount,
                            edit_category.strip(),
                            edit_description.strip(),
                            edit_date.isoformat(),
                            int(selected_id)
                        )
                    )

                st.success("Transaction updated successfully!")
                st.rerun()

    confirm_delete = st.checkbox(
        f"I want to permanently delete transaction ID {selected_id}"
    )

    if st.button("🗑️ Delete transaction", disabled=not confirm_delete):
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                "DELETE FROM transactions WHERE id = ?",
                (int(selected_id),)
            )

        st.success("Transaction deleted.")
        st.rerun()


display_df = filtered_df.copy()
display_df["transaction_date"] = (
    display_df["transaction_date"].dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_df[
        ["id", "transaction_date", "transaction_type",
         "category", "description", "amount"]
    ],
    width="stretch",
    hide_index=True
)

# CSV export
csv_data = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download transactions as CSV",
    data=csv_data,
    file_name="finance_transactions.csv",
    mime="text/csv"
)
