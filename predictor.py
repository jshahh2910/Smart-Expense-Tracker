import pandas as pd
import calendar


def predict_monthly_expense():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)

    latest_date = spending["date"].max()
    current_month_data = spending[(spending["date"].dt.month == latest_date.month) & (spending["date"].dt.year == latest_date.year)]
    if current_month_data.empty:
        return None
        

    total_spent = current_month_data["amount"].sum()
    current_day = latest_date.day
    days_in_month = calendar.monthrange(latest_date.year, latest_date.month)[1]

    daily_average = total_spent / current_day
    predicted_total = daily_average * days_in_month

    days_left = days_in_month - current_day

    return {
        "total_spent": total_spent,
        "daily_average": daily_average,
        "days_left": days_left,
        "predicted_total": predicted_total,
    }
    


def predict_next_month():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)
    if spending.empty:
        return None

    spending["month"] = spending["date"].dt.to_period("M")
    monthly_totals = (spending.groupby("month")["amount"].sum().sort_index())
    if monthly_totals.empty:
        return None
    
    last_months = monthly_totals.tail(3)
    prediction = last_months.mean()

    return {
        "recent_months": last_months.to_dict(),
        "prediction": prediction,
    }