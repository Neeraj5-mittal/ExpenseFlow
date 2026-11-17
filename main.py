"""Command-line menu for the Personal Expense Tracker."""

from datetime import date

from expense_tracker import (
    CATEGORIES,
    add_expense,
    delete_expense,
    load_expenses,
    monthly_total,
    save_expenses,
    total_by_category
)


def show_menu():
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Delete an expense")
    print("4. Category summary")
    print("5. Monthly total")
    print("6. Exit")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<4}{'Date':<12}{'Category':<10}{'Amount':>10} Description")

    for item in expenses:
        print(
            f"{item['id']:<4}{item['date']:<12}"
            f"{item['category']:<10}"
            f"{item['amount']:>10.2f} {item['description']}"
        )

    print(
        f"Total spent: Rs.{sum(i['amount'] for i in expenses):.2f}"
    )


def add_flow(expenses):
    print("Categories:", ", ".join(CATEGORIES))

    amount = input("Amount (Rs.): ")
    category = input("Category: ").strip().title()
    description = input("Description: ")

    when = input(
        "Date (YYYY-MM-DD, blank for today): "
    ).strip() or None

    try:
        item = add_expense(
            expenses,
            amount,
            category,
            description,
            when
        )

    except ValueError as error:
        print("Error:", error)
        return

    save_expenses(expenses)

    print(
        f"Added expense #{item['id']} "
        f"of Rs.{item['amount']:.2f}."
    )


def delete_flow(expenses):
    try:
        expense_id = int(
            input("Enter expense ID to delete: ")
        )

    except ValueError:
        print("Error: ID must be a number.")
        return

    if delete_expense(expenses, expense_id):
        save_expenses(expenses)
        print("Expense deleted.")

    else:
        print("No expense found with that ID.")


def summary_flow(expenses):
    totals = total_by_category(expenses)

    if not totals:
        print("No expenses recorded yet.")
        return

    for category, amount in sorted(
        totals.items(),
        key=lambda pair: -pair[1]
    ):
        print(f"{category:<10} Rs.{amount:.2f}")


def monthly_flow(expenses):
    today = date.today()

    text = input(
        f"Month as YYYY-MM (blank for {today:%Y-%m}): "
    ).strip()

    try:
        year, month = (
            (int(x) for x in text.split("-"))
            if text
            else (today.year, today.month)
        )

        if not 1 <= month <= 12:
            raise ValueError

    except ValueError:
        print("Error: enter the month like 2026-03.")
        return

    print(
        f"Total for {year:04d}-{month:02d}: "
        f"Rs.{monthly_total(expenses, year, month):.2f}"
    )


def main():
    expenses = load_expenses()

    actions = {
        "1": add_flow,
        "2": view_expenses,
        "3": delete_flow,
        "4": summary_flow,
        "5": monthly_flow
    }

    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "6":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action:
            action(expenses)

        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()