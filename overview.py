import analyzer
import insights
import streamlit as st
import pandas as pd
import expense_manager

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.markdown(
    """
    <style>
    /* Make future dates in the Streamlit date picker appear dimmer */
    [data-baseweb="calendar"] [aria-disabled="true"] {
        opacity: 0.35 !important;
        color: #666 !important;
    }

    /* Slightly reduce emphasis on non-selected calendar days */
    [data-baseweb="calendar"] td {
        transition: opacity 0.2s ease;
    }

    /* Keep the selected day clearly visible */
    [data-baseweb="calendar"] [aria-selected="true"] {
        opacity: 1 !important;
    }

    /* Make selectable (active) days brighter */
    [data-baseweb="calendar"] td button:not([disabled]) {
        color: #ffffff !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    /* Make today's date slightly more prominent */
    [data-baseweb="calendar"] [aria-current="date"] {
        border: 1px solid #ffffff !important;
        border-radius: 50% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Smart Expenses Tracker 📈")
st.write("Track, analyse, and forecast your personal expenses — all in one place.") 
st.caption("Use the sidebar on the left to navigate between Analytics, Insights, and Forecasting.")

if "expenses" not in st.session_state:
        try:
            st.session_state["expenses"] = pd.read_csv("expenses.csv")
        except FileNotFoundError:
            st.session_state["expenses"] = pd.DataFrame( columns=["amount", "category", "description", "date", "payment_method"])
        
        expenses = st.session_state["expenses"]



st.divider()

expenses_df = st.session_state["expenses"]

col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("Total Spending", analyzer.all_time_spending()),
    ("YTD Spending", analyzer.ytd_spending()),
    ("Daily Average", analyzer.average_daily_expense()),
    ("This Week", insights.weekly_spending())
]

for col, (title, value) in zip([col1, col2, col3, col4], metrics):
    col.markdown(
        f'''
        <div style="
            border:1px solid #333;
            border-radius:12px;
            padding:16px;
            background-color:#111827;
            text-align:center;
        ">
            <div style="font-size:14px;color:#9CA3AF;">{title}</div>
            <div style="font-size:28px;font-weight:bold;color:#22C55E;">
                ₹{value:,.2f}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

st.divider()

st.subheader("All Transactions")
st.caption("View and manage all recorded expenses.")
display_df = expenses_df.copy()

display_df["date"] = pd.to_datetime(display_df["date"],dayfirst=True,errors="coerce").dt.strftime("%d/%m/%Y")

st.dataframe(display_df, use_container_width=True)
st.divider()

add_tab, delete_tab = st.tabs(["Add Expense", "Delete Expense"])

with add_tab:
    with st.form("add_form", clear_on_submit=True):
        amount = st.text_input("Amount", placeholder="Enter amount", key="amount")
        category = st.selectbox("Category", [
            "Food & Drinks",
            "Shopping",
            "Entertainment",
            "Transport",
            "Services",
            "Other"
        ], key="category")
        description = st.text_input("Description", key="description")
        from datetime import date as dt_date

        date = st.date_input(
            "Date",
            value=dt_date.today(),
            max_value=dt_date.today(),
            key="date",
        )
        payment_method = st.selectbox("Payment Method", [
            "UPI",
            "Card",
            "Cash",
            "Net Banking"
        ], key="payment_method")

        submitted = st.form_submit_button("Add")

    if submitted:
        formatted_date = date.strftime("%d/%m/%Y")
        amount = float(amount) if amount else 0.0
        category = category.strip().title()
        expense_manager.add_expense(
            amount,
            category,
            description,
            formatted_date,
            payment_method
        )
        st.session_state["expenses"] = pd.read_csv("expenses.csv")
        st.success("Expense added successfully!")
        st.rerun()

with delete_tab:
    expense_options = [
        f"{idx + 1} | ₹{row['amount']} | {row['category']} | {row['description']}"
        for idx, row in expenses_df.iterrows()
    ]

    selected_expense = st.selectbox(
        "Select Expense",
        expense_options,
        key="delete_expense"
    )

    row_number = expense_options.index(selected_expense) + 1 if expense_options else None

    deleted = st.button("Delete")

    if deleted and row_number is not None:
        try:
            expense_manager.delete_expense(row_number)
            st.session_state["expenses"] = pd.read_csv("expenses.csv")
            st.success("Expense deleted successfully.")
            st.rerun()
        except ValueError as e:
            st.error(str(e))