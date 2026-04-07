import csv
import os
import requests

def get_php_rate(currency):
    if currency =='PHP':
        return 1.0
    try:
        response = requests.get(
            "https://api.frankfurter.dev/v1/latest",
            params={"from": currency, "to": "PHP"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return data["rates"]["PHP"]
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except (KeyError, ValueError):
        print("Error: Could not parse exchange rate.")
        return None
    
def save_expense(date,category,description,amount,currency):
    filename = "expenses.csv"
    rate = get_php_rate(currency)
    if rate is None:
        print("Could not retrieve exchange rate. Expense not saved.")
        return

    php_amount = amount * rate

    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:

            writer.writerow(["date", "category", "description", "amount", "currency", "php_amount", "rate"])
        writer.writerow([date, category, description, amount, currency, round(php_amount, 2), rate])

    print(f"Saved: {description} — {amount} {currency} = ₱{php_amount:.2f}")
