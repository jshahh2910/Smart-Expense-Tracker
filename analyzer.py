import pandas as pd

def all_time_spending():
    spending = pd.read_csv("expenses.csv")
    total = spending["amount"].sum()
    return total

 
def ytd_spending():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"],format="mixed",dayfirst=True)    
    current_year = pd.Timestamp.now().year
    ytd_total = spending[spending["date"].dt.year == current_year]["amount"].sum()
    return ytd_total


def spending_by_category():
    spending = pd.read_csv("expenses.csv")
    category_totals = spending.groupby("category")["amount"].sum()
    category_totals.index.name = None
    return category_totals
    

def monthly_summary():
    summary = pd.read_csv("expenses.csv")
    summary["date"] = pd.to_datetime(summary["date"], format="mixed", dayfirst=True)
    summary["month"] = summary["date"].dt.to_period("M")
    monthly_totals = summary.groupby("month")["amount"].sum().sort_index()
    return monthly_totals

def average_daily_expense():
    spending = pd.read_csv("expenses.csv")
    total_spending = spending["amount"].sum()
    unique_days = spending["date"].nunique()

    if unique_days == 0:
        return 0

    average = total_spending / unique_days
    return average
