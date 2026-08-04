import pandas as pd

def weekly_spending():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)

    current_week = pd.Timestamp.now().isocalendar().week
    weekly_total = spending[spending["date"].dt.isocalendar().week == current_week]["amount"].sum()

    return weekly_total


def detect_spending_spike():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)
    current_week = pd.Timestamp.now().isocalendar().week
    current_week_total = spending[spending["date"].dt.isocalendar().week == current_week]["amount"].sum()
    last_week =  current_week - 1
    last_week_total = spending[spending["date"].dt.isocalendar().week == last_week]["amount"].sum()

    if last_week_total == 0:
        if current_week_total == 0:
            return {"current_week_total": 0, "last_week_total": 0, "spending_spike": None}
        return {
            "current_week_total": current_week_total,
            "last_week_total": 0,
            "spending_spike": None,
        }

    spending_spike = ((current_week_total - last_week_total) / last_week_total) * 100

    return {
        "current_week_total": current_week_total,
        "last_week_total": last_week_total,
        "spending_spike": spending_spike,
    }


def overspending_category():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)
    today = pd.Timestamp.today()
    current_month_data = spending[(spending["date"].dt.month == today.month) & (spending["date"].dt.year == today.year)]
    last_month = today.month - 1
    last_year = today.year
    if last_month == 0:
        last_month = 12
        last_year -= 1
    last_month_data = spending[(spending["date"].dt.month == last_month) & (spending["date"].dt.year == last_year)]
    current_totals = current_month_data.groupby("category")["amount"].sum()
    last_totals = last_month_data.groupby("category")["amount"].sum()
    if current_totals.empty:
        return None

    top_category = current_totals.idxmax()
    this_month = current_totals[top_category]
    last_month_amount = last_totals.get(top_category, 0)
    difference = this_month - last_month_amount
    return {
        "top_category": top_category,
        "this_month": this_month,
        "last_month": last_month_amount,
        "difference": difference,
    }


def frequent_purchases():
    spending = pd.read_csv("expenses.csv")
    spending["date"] = pd.to_datetime(spending["date"], format="mixed", dayfirst=True)
    today = pd.Timestamp.today()
    current_month_data = spending[
        (spending["date"].dt.month == today.month)
        & (spending["date"].dt.year == today.year)
    ]

    if current_month_data.empty:
        return {}

    category_totals = current_month_data["category"].value_counts()
    return category_totals.to_dict()
