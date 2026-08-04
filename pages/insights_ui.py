import streamlit as st
import pandas as pd
import plotly.express as px

if "expenses" not in st.session_state:
    try:
        st.session_state["expenses"] = pd.read_csv("expenses.csv")
    except FileNotFoundError:
        st.session_state["expenses"] = pd.DataFrame(
            columns=["amount", "category", "description", "date", "payment method"]
        )

expenses_df = st.session_state["expenses"]

if expenses_df.empty:
    st.title("💡 Spending Insights")
    st.info("No expense data available. Add some expenses to view insights.")
    st.stop()
    
highest_category = (expenses_df.groupby("category")["amount"].sum().idxmax())

largest_expense = expenses_df["amount"].max()

most_frequent_category = (expenses_df["category"].value_counts().idxmax())

average_expense = expenses_df["amount"].mean()

st.title("💡 Spending Insights")
st.write("Discover patterns, trends, and useful insights from your spending habits.")

st.divider()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.metric("Highest Category", highest_category)

with col2:
    st.metric("Largest Expense", f"₹{largest_expense:,.2f}")

with col3:
    st.metric("Most Frequent Category", most_frequent_category)

with col4:
    st.metric("Average Expense", f"₹{average_expense:,.2f}")


st.divider()
st.subheader("💡 Key Insights")

category_totals = expenses_df.groupby("category")["amount"].sum().sort_values(ascending=False)

top_category = category_totals.idxmax()
top_amount = category_totals.max()

top_percentage = (top_amount / expenses_df["amount"].sum()) * 100

st.info(f"💰 **{top_category}** accounts for **{top_percentage:.1f}%** of your total spending.")
st.success(f"🧾 Your average transaction is **₹{average_expense:.2f}**.")
st.warning(f"🚨 Your largest expense was **₹{largest_expense:,.2f}**.")

st.divider()

st.subheader("📊 Category Breakdown")

category_chart = (expenses_df.groupby("category")["amount"].sum().reset_index())

fig = px.bar(
    category_chart,
    x="amount",
    y="category",
    orientation="h",
    title="Total Spending by Category",
    labels={"amount": "Amount (₹)", "category": "Category"},
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.divider()

st.subheader("🎯 Recommendations")

if top_percentage > 40:
    st.warning(f"Your spending is heavily concentrated in **{top_category}**. Consider setting a monthly budget for this category.")

if average_expense > 500:
    st.info("Your average transaction value is relatively high. Tracking smaller daily expenses could help reduce overall spending.")

if most_frequent_category == "Food & Drinks":
    st.success("Food & Drinks is your most frequent expense. Meal planning may help reduce recurring costs.")

if most_frequent_category == "Transport":
    st.success("Transport is your most frequent expense. Consider monthly passes or ride sharing to save money.")

st.caption("Recommendations are generated automatically from your spending history.")