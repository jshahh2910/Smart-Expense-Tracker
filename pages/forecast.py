import streamlit as st
import pandas as pd
import plotly.express as px
import predictor

if "expenses" not in st.session_state:
    try:
        st.session_state["expenses"] = pd.read_csv("expenses.csv")
    except FileNotFoundError:
        st.session_state["expenses"] = pd.DataFrame(
            columns=["amount", "category", "description", "date", "payment method"]
        )

expenses_df = st.session_state["expenses"]

if not expenses_df.empty:
    expenses_df["date"] = pd.to_datetime(
        expenses_df["date"], format="mixed", dayfirst=True
    )


st.title ("📈 Expense Forecast")
st.write("Understand your future spending based on your historical expense data.")

st.divider()

col1, col2 = st.columns(2)

end_of_month_prediction = predictor.predict_monthly_expense()
next_month_prediction = predictor.predict_next_month()

with col1:
    if end_of_month_prediction is not None:
        st.metric(
            label="Predicted End of Month",
            value=f"₹{end_of_month_prediction['predicted_total']:,.2f}"
        )
    else:
        st.metric("Predicted End of Month", "N/A")

with col2:
    if next_month_prediction is not None:
        st.metric(
            label="Predicted Next Month",
            value=f"₹{next_month_prediction['prediction']:,.2f}"
        )
    else:
        st.metric("Predicted Next Month", "N/A")


st.divider()

st.subheader("📈 Monthly Spending Trend")

monthly_spending = (
    expenses_df.groupby(expenses_df["date"].dt.to_period("M"))["amount"].sum().reset_index()
)

monthly_spending["date"] = monthly_spending["date"].dt.to_timestamp()

predicted_row = pd.DataFrame({
    "date": [monthly_spending["date"].max() + pd.DateOffset(months=1)],
    "amount": [next_month_prediction["prediction"]]
})

forecast_df = pd.concat([monthly_spending, predicted_row], ignore_index=True)

fig = px.line(
    forecast_df,
    x="date",
    y="amount",
    markers=True,
    title="Monthly Spending with Next Month Forecast"
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.divider()
st.subheader("📅 Monthly Spending History")

history_df = forecast_df.copy()
history_df["date"] = history_df["date"].dt.strftime("%b %Y")
history_df.columns = ["Month", "Total Spending (₹)"]
history_df["Total Spending (₹)"] = history_df["Total Spending (₹)"].map(lambda x: f"₹{x:,.2f}")
history_df.loc[history_df.index[-1], "Month"] += " (Predicted)"

st.dataframe(history_df, use_container_width=True, hide_index=True)

st.divider()

if next_month_prediction["prediction"] > monthly_spending["amount"].iloc[-1]:
    st.info("📈 Spending is expected to increase next month.")
else:
    st.success("📉 Spending is expected to decrease next month.")


with st.expander("How is this prediction made?"):
    st.write("""
    This forecast is based on your historical monthly expenses.
    It uses a linear regression model to estimate future spending trends.
    The prediction becomes more accurate as more monthly data is added.
    """)



