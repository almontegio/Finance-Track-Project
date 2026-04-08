import csv
import os
filename = "expenses.csv"

cat_totals = {}

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        category = row["category"]
        amount = float(row["php_amount"])
        if category not in cat_totals:
            cat_totals[category] = 0
        cat_totals[category] += amount
        # add amount to totals[category]
        # hint: check if category already exists in totals first
        

for x in cat_totals:
    print(f"Amount of {x}: {cat_totals[x]} ")
print(f"Grand Total: {sum(cat_totals.values())}")
