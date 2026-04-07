from expenses import save_expense

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid amount. Enter a number.")

def get_date_input(prompt):
    while True:
        value = input(prompt)
        if len(value) == 10 and value[4] == "-" and value[7] == "-":
            return value
        print("Invalid date. Use YYYY-MM-DD format.")

def main():
    print("=== Finance Tracker ===")

    date = get_date_input("Date (YYYY-MM-DD): ")
    category = input("Category: ")
    description = input("Description: ")
    amount = get_float_input("Amount: ")
    currency = input("Currency (e.g. USD, PHP, EUR): ").upper()

    save_expense(date, category, description, amount, currency)

if __name__ == "__main__":
    main()