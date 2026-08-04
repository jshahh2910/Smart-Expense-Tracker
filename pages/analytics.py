import streamlit as st
import pandas as pd
import analyzer
import plotly.express as px


if "expenses" not in st.session_state:
        try:
            st.session_state["expenses"] = pd.read_csv("expenses.csv")
        except FileNotFoundError:
            st.session_state["expenses"] = pd.DataFrame( columns=["amount", "category", "description", "date", "payment_method"])
        
expenses_df = st.session_state["expenses"]


if not expenses_df.empty:
    expenses_df["date"] = pd.to_datetime(
        expenses_df["date"], format="mixed", dayfirst=True)
    
st.title("📊 Spending Analytics")
st.write("A breakdown of where your money is going.")


col1, col2 = st.columns(2)


with col1:
    date_range = st.date_input("Date Range", value=(expenses_df["date"].min().date(), expenses_df["date"].max().date()))
with col2:
    categories = st.multiselect("Categories", options=sorted(expenses_df["category"].unique()), default=sorted(expenses_df["category"].unique()))

st.write("")

# KPI cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
st.markdown("<br>", unsafe_allow_html=True)



filtered_df = expenses_df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[(filtered_df["date"].dt.date >= start_date) & (filtered_df["date"].dt.date <= end_date)]

filtered_df = filtered_df[filtered_df["category"].isin(categories)]

# KPI metrics
transaction_count = len(filtered_df)
total_spent = filtered_df["amount"].sum()
average_expense = filtered_df["amount"].mean() if transaction_count else 0

top_category = (
    filtered_df.groupby("category")["amount"].sum().idxmax()
    if transaction_count else "N/A"
)

with kpi1:
    st.metric("Total Spent", f"₹{total_spent:,.2f}")
with kpi2:
    st.metric("Transactions", transaction_count)
with kpi3:
    st.metric("Average Expense", f"₹{average_expense:,.2f}")
with kpi4:
    st.metric("Top Category", top_category)

fig = px.pie(
    filtered_df,
    values="amount",
    names="category",
    title="Spending by Category"
)

fig.update_layout(
    height=450,
    legend=dict(
        orientation="h",
        y=-0.2,
        x=0.5,
        xanchor="center"
    )
)


monthly_spending = (filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["amount"].sum().reset_index())

monthly_spending["date"] = (monthly_spending["date"].dt.to_timestamp().dt.strftime("%b %Y"))

monthly_fig = px.line(
    monthly_spending,
    x="date",
    y="amount",
    title="Monthly Spending",
    markers=True
)

st.plotly_chart(
    monthly_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

category_totals = (
    filtered_df.groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

bar_fig = px.bar(
    category_totals,
    x="category",
    y="amount",
    title="Category Totals"
)

with col_right:
    st.plotly_chart(
        bar_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
