"""Core logic for the Personal Expense Tracker."""

import json
import math
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")

CATEGORIES = ["Food", "Travel", "Study", "Shopping", "Bills", "Other"]


def load_expenses(path=DATA_FILE):
    """Return saved expenses, or an empty list if nothing is saved."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses, path=DATA_FILE):
    """Write all expenses to the JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)


def add_expense(expenses, amount, category, description="", expense_date=None):
    """Validate input and add a new expense."""
    try:
        amount = round(float(amount), 2)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.")

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if category not in CATEGORIES:
        raise ValueError(
            "Category must be one of: " + ", ".join(CATEGORIES)
        )

    if expense_date is None:
        expense_date = date.today().isoformat()
    else:
        try:
            expense_date = datetime.strptime(
                expense_date, "%Y-%m-%d"
            ).date().isoformat()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    new_id = max((item["id"] for item in expenses), default=0) + 1

    expense = {
        "id": new_id,
        "date": expense_date,
        "category": category,
        "amount": amount,
        "description": description.strip()
    }

    expenses.append(expense)
    return expense


def delete_expense(expenses, expense_id):
    """Remove an expense by ID."""
    for item in expenses:
        if item["id"] == expense_id:
            expenses.remove(item)
            return True

    return False


def total_by_category(expenses):
    """Return total spending for each category."""
    totals = {}

    for item in expenses:
        totals[item["category"]] = round(
            totals.get(item["category"], 0) + item["amount"], 2
        )

    return totals


def monthly_total(expenses, year, month):
    """Return total spending for one month."""
    prefix = f"{year:04d}-{month:02d}"

    return round(
        sum(
            i["amount"]
            for i in expenses
            if i["date"].startswith(prefix)
        ), 2
    )