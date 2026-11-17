from datetime import date, datetime
from typing import Any

import pandas as pd
import streamlit as st

from expense_tracker import (
    add_expense,
    delete_expense,
    load_expenses,
    monthly_total,
    save_expenses,
    total_by_category,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ExpenseFlow | Personal Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CONSTANTS
# =========================================================

CATEGORIES: list[str] = [
    "Food",
    "Travel",
    "Study",
    "Shopping",
    "Bills",
    "Other",
]

CURRENCY = "₹"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #0b1120;
            color: #f1f5f9;
        }

        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #263247;
        }

        [data-testid="stSidebar"] * {
            color: #e2e8f0;
        }

        .hero {
            padding: 32px;
            border-radius: 20px;
            background: linear-gradient(
                120deg,
                #172554,
                #312e81,
                #4c1d95
            );
            border: 1px solid #4338ca;
            margin-bottom: 28px;
        }

        .hero h1 {
            color: white;
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .hero p {
            color: #c7d2fe;
            font-size: 15px;
            margin-bottom: 0;
        }

        .section-title {
            color: #f8fafc;
            font-size: 21px;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 16px;
        }

        .metric-card {
            background: #151f32;
            border: 1px solid #29364d;
            border-radius: 16px;
            padding: 22px;
            min-height: 135px;
        }

        .metric-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 500;
        }

        .metric-value {
            color: #f8fafc;
            font-size: 27px;
            font-weight: 800;
            margin-top: 12px;
        }

        .metric-icon {
            font-size: 23px;
        }

        .info-card {
            background: #151f32;
            border: 1px solid #29364d;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
        }

        .info-card h3 {
            color: #f8fafc;
            font-size: 16px;
        }

        .info-card p {
            color: #94a3b8;
            font-size: 13px;
        }

        .success-text {
            color: #34d399;
            font-weight: 600;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 42px;
        }

        div[data-testid="stForm"] {
            background: #151f32;
            padding: 24px;
            border: 1px solid #29364d;
            border-radius: 16px;
        }

        div[data-testid="stMetric"] {
            background: #151f32;
            border: 1px solid #29364d;
            padding: 18px;
            border-radius: 14px;
        }

        div[data-testid="stMetricLabel"] {
            color: #94a3b8;
        }

        div[data-testid="stMetricValue"] {
            color: #f8fafc;
        }

        .footer {
            text-align: center;
            color: #64748b;
            font-size: 12px;
            padding: 30px 0 10px 0;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_expenses() -> list[dict[str, Any]]:
    """Load expense records from JSON storage."""
    records = load_expenses()
    return records


def money(amount: float) -> str:
    """Format amount as Indian Rupees."""
    return f"{CURRENCY}{amount:,.2f}"


def get_category_totals(
    expenses: list[dict[str, Any]]
) -> dict[str, float]:
    """Return category totals with explicit types."""

    raw_totals = total_by_category(expenses)

    category_totals: dict[str, float] = {
        str(category): float(amount)
        for category, amount in raw_totals.items()
    }

    return category_totals


def get_monthly_expenses(
    expenses: list[dict[str, Any]],
    year: int,
    month: int,
) -> float:
    """Calculate total expenses for a selected month."""

    return float(monthly_total(expenses, year, month))


def create_dataframe(
    expenses: list[dict[str, Any]]
) -> pd.DataFrame:
    """Convert expense records into a DataFrame."""

    if not expenses:
        return pd.DataFrame(
            columns=[
                "ID",
                "Date",
                "Category",
                "Amount",
                "Description",
            ]
        )

    df = pd.DataFrame(expenses)

    df = df.rename(
        columns={
            "id": "ID",
            "date": "Date",
            "category": "Category",
            "amount": "Amount",
            "description": "Description",
        }
    )

    return df


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"


if "expenses" not in st.session_state:
    st.session_state.expenses = get_expenses()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 💸 ExpenseFlow")

    st.caption("PERSONAL FINANCE MANAGER")

    st.divider()

    st.markdown("### Navigation")

    selected_page = st.radio(
        "Navigate",
        [
            "Overview",
            "Add Expense",
            "Manage Expenses",
            "Reports",
        ],
        label_visibility="collapsed",
        key="navigation",
    )

    st.session_state.page = selected_page

    st.divider()

    st.markdown("### Your Finance")

    st.caption("Track your money. Control your spending.")

    st.markdown(
        """
        <div class="info-card">
            <h3>💡 Smart Spending</h3>
            <p>
                Keep track of your expenses and understand
                where your money goes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Built with Python & Streamlit")


# =========================================================
# LOAD CURRENT DATA
# =========================================================

expenses: list[dict[str, Any]] = st.session_state.expenses

category_totals: dict[str, float] = get_category_totals(expenses)

total_spending: float = sum(category_totals.values())

today = date.today()

current_month_total = get_monthly_expenses(
    expenses,
    today.year,
    today.month,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>Personal Expense Tracker 💸</h1>
        <p>
            Manage your daily expenses, analyze your spending
            and make smarter financial decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# OVERVIEW PAGE
# =========================================================

if st.session_state.page == "Overview":

    st.markdown(
        '<div class="section-title">Financial Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Spending",
            value=money(total_spending),
        )

    with col2:
        st.metric(
            label="This Month",
            value=money(current_month_total),
        )

    with col3:
        st.metric(
            label="Transactions",
            value=len(expenses),
        )

    with col4:
        st.metric(
            label="Categories Used",
            value=len(category_totals),
        )

    st.markdown(
        '<div class="section-title">Spending Analytics</div>',
        unsafe_allow_html=True,
    )

    chart_col, insight_col = st.columns(
        [1.6, 1],
        gap="large",
    )

    with chart_col:

        st.markdown("#### Category-wise Spending")

        if category_totals:

            chart_data = pd.DataFrame(
                {
                    "Category": list(category_totals.keys()),
                    "Amount": list(category_totals.values()),
                }
            )

            chart_data = chart_data.set_index("Category")

            st.bar_chart(
                chart_data,
                y="Amount",
                height=330,
            )

        else:
            st.info("Add your first expense to see spending analytics.")

    with insight_col:

        st.markdown("#### Quick Insights")

        if category_totals:

            # Explicit dictionary typing fixes Pylance max() errors.
            top_category: str = max(
                category_totals,
                key=lambda category: category_totals[category],
            )

            top_amount: float = category_totals[top_category]

            st.markdown(
                f"""
                <div class="info-card">
                    <h3>🏆 Highest Spending</h3>
                    <h2>{top_category}</h2>
                    <p>{money(top_amount)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            average_expense = total_spending / len(expenses)

            st.markdown(
                f"""
                <div class="info-card">
                    <h3>📊 Average Transaction</h3>
                    <h2>{money(average_expense)}</h2>
                    <p>Average amount per transaction</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.info("Insights will appear after adding expenses.")

    st.markdown(
        '<div class="section-title">Recent Transactions</div>',
        unsafe_allow_html=True,
    )

    if expenses:

        recent_expenses = sorted(
            expenses,
            key=lambda item: str(item.get("date", "")),
            reverse=True,
        )[:5]

        recent_df = create_dataframe(recent_expenses)

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No transactions available. Start by adding an expense.")


# =========================================================
# ADD EXPENSE PAGE
# =========================================================

elif st.session_state.page == "Add Expense":

    st.markdown(
        '<div class="section-title">Add a New Expense</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Enter your transaction details below to record a new expense."
    )

    with st.form("add_expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=10.0,
                format="%.2f",
            )

            category = st.selectbox(
                "Category",
                CATEGORIES,
            )

        with col2:

            expense_date = st.date_input(
                "Expense Date",
                value=date.today(),
                max_value=date.today(),
            )

            description = st.text_input(
                "Description",
                placeholder="Example: Lunch, Bus ticket, Books...",
            )

        st.write("")

        submitted = st.form_submit_button(
            "➕ Add Expense",
            use_container_width=True,
            type="primary",
        )

        if submitted:

            if amount <= 0:

                st.error("Please enter an amount greater than zero.")

            else:

                try:

                    add_expense(
                        expenses,
                        amount,
                        category,
                        description,
                        expense_date.isoformat(),
                    )

                    save_expenses(expenses)

                    st.session_state.expenses = expenses

                    st.success("Expense added successfully! 🎉")

                    st.rerun()

                except (ValueError, TypeError) as error:

                    st.error(f"Unable to add expense: {error}")


# =========================================================
# MANAGE EXPENSES PAGE
# =========================================================

elif st.session_state.page == "Manage Expenses":

    st.markdown(
        '<div class="section-title">Manage Your Expenses</div>',
        unsafe_allow_html=True,
    )

    if expenses:

        st.write(f"Total transactions: **{len(expenses)}**")

        df = create_dataframe(expenses)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.markdown("### Delete a Transaction")

        expense_ids = [
            int(item["id"])
            for item in expenses
        ]

        selected_id = st.selectbox(
            "Select Expense ID",
            expense_ids,
        )

        selected_expense = next(
            (
                item
                for item in expenses
                if int(item["id"]) == selected_id
            ),
            None,
        )

        if selected_expense:

            st.info(
                f"Selected: {selected_expense.get('category', 'Unknown')} | "
                f"{money(float(selected_expense.get('amount', 0)))} | "
                f"{selected_expense.get('date', '')}"
            )

        if st.button(
            "🗑️ Delete Selected Expense",
            type="primary",
        ):

            deleted = delete_expense(
                expenses,
                selected_id,
            )

            if deleted:

                save_expenses(expenses)

                st.session_state.expenses = expenses

                st.success("Expense deleted successfully.")

                st.rerun()

            else:

                st.error("Unable to delete the selected expense.")

    else:

        st.info("No expenses available to manage.")


# =========================================================
# REPORTS PAGE
# =========================================================

elif st.session_state.page == "Reports":

    st.markdown(
        '<div class="section-title">Financial Reports</div>',
        unsafe_allow_html=True,
    )

    report_col1, report_col2 = st.columns(2)

    with report_col1:

        selected_year = st.number_input(
            "Select Year",
            min_value=2000,
            max_value=2100,
            value=today.year,
            step=1,
        )

    with report_col2:

        selected_month = st.selectbox(
            "Select Month",
            options=list(range(1, 13)),
            format_func=lambda month: datetime(
                2000,
                month,
                1,
            ).strftime("%B"),
            index=today.month - 1,
        )

    selected_month_total = get_monthly_expenses(
        expenses,
        int(selected_year),
        int(selected_month),
    )

    st.metric(
        "Selected Month Spending",
        money(selected_month_total),
    )

    st.divider()

    st.markdown("### Category Summary")

    if category_totals:

        summary_df = pd.DataFrame(
            [
                {
                    "Category": category,
                    "Total Spending": amount,
                }
                for category, amount in category_totals.items()
            ]
        )

        summary_df = summary_df.sort_values(
            by="Total Spending",
            ascending=False,
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Category Distribution")

        pie_data = summary_df.set_index("Category")

        st.bar_chart(
            pie_data,
            y="Total Spending",
            height=300,
        )

    else:

        st.info("No category data available yet.")

    st.divider()

    st.markdown("### Export Your Data")

    if expenses:

        export_df = create_dataframe(expenses)

        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Expense Report (CSV)",
            data=csv_data,
            file_name="expense_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:

        st.info("Add expenses before exporting your report.")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ExpenseFlow | Personal Expense Tracker
        <br>
        Built with Python, Streamlit and Pandas
    </div>
    """,
    unsafe_allow_html=True,
)