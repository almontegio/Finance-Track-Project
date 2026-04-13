import csv
import os
from datetime import datetime
filename = "expenses.csv"

if not os.path.exists("expenses.csv"):
    print("No expenses file found. Log an expense first.")
    sys.exit()
date_totals = {}

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            amount = float(row["php_amount"])
        except ValueError:
            print(f"Skipping malformed row: {row}")
            continue
        dt = datetime.strptime(row["date"], "%Y-%m-%d")
        month_key = f"{dt.year}-{dt.month:02d}"  # "2026-04"
        if month_key not in date_totals:
            date_totals[month_key] = 0
        date_totals[month_key] += amount

for y in date_totals:
    print(f"Amount of {y}: {date_totals[y]} ")
print(f"Grand Total: {sum(date_totals.values())}")