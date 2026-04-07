import csv
import os

filename = "expenses.csv"

totals = {}

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        category = row["category"]
        amount = float(row["php_amount"])
        if category not in totals:
            totals[category] = 0
        totals[category] += amount
        # add amount to totals[category]
        # hint: check if category already exists in totals first
for x in totals:
    print(f"Amount of {x}: {totals[x]} ")
print(f"Grand Total: {sum(totals.values())}")
# print each category and its total
# print grand total at the end