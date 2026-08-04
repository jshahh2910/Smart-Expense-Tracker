import csv
import os
import pandas as pd
import analyzer
import insights
import predictor

def add_expense(amount, category, description, date, payment_method):

    file_exists = os.path.exists("expenses.csv")
    
    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["amount", "category", "description", "date", "payment_method"])
        writer.writerow([amount, category, description, date, payment_method])

    return "Expenses added successfully"

def read_expenses():
    read = pd.read_csv("expenses.csv")
    return read

def delete_expense(row_number):
    with open("expenses.csv", "r") as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        raise ValueError("No expenses to delete.")

    if row_number < 1 or row_number >= len(rows):
        raise ValueError("Invalid row number.")

    rows.pop(row_number)

    with open("expenses.csv", "w", newline="") as file:
        csv.writer(file).writerows(rows)

    return "Expense deleted successfully."

if __name__ == "__main__":
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")
        print("5. Analyze Expenese")
        print("6. Insights")
        print("7. Prediction")
        
        choice = input("Choose: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            read_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            break
        elif choice == "5":
            print("1. All-Time Spending")
            print("2. YTD Spending")
            print("3. Spending By Category")
            print("4. Monthly Summary")
            print("5. Daily Average")

            choice = input("Choose: ")

            if choice == "1":
                analyzer.all_time_spending()
            elif choice == "2":
                analyzer.ytd_spending()
            elif choice == "3":
                analyzer.spending_by_category()
            elif choice == "4":
                analyzer.monthly_summary()
            elif choice == "5":
                analyzer.average_daily_expense()
        
        elif choice == "6":
            print("1. Weekly Spendings.")
            print("2. Spending Spike")
            print("3. Overspending Category")
            print("4. Frequent Purchase")

            choice = input("Choose: ")

            if choice == "1":
                insights.weekly_spending()
            elif choice == "2":
                insights.detect_spending_spike()
            elif choice == "3":
                insights.overspending_category()
            elif choice == "4":
                insights.frequent_purchases()

        elif choice == "7":
            print("1. Predict Monthly Expenses.")
            print("2. Predict Next Month")

            choice = input("Choose: ")

            if choice == "1":
                predictor.predict_monthly_expense()
            elif choice == "2":
                predictor.predict_next_month()