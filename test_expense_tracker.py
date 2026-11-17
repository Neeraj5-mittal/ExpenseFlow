"""Unit tests for expense_tracker.py."""

import tempfile
import unittest
from pathlib import Path

from expense_tracker import (
    add_expense,
    delete_expense,
    load_expenses,
    monthly_total,
    save_expenses,
    total_by_category
)


class ExpenseTrackerTests(unittest.TestCase):

    def setUp(self):
        self.expenses = []

    def test_add_valid_expense(self):
        item = add_expense(
            self.expenses,
            "250.50",
            "Food",
            "Lunch",
            "2026-03-05"
        )

        self.assertEqual(item["id"], 1)
        self.assertEqual(item["amount"], 250.5)
        self.assertEqual(len(self.expenses), 1)

    def test_ids_increase(self):
        add_expense(self.expenses, 10, "Food")

        second = add_expense(
            self.expenses,
            20,
            "Travel"
        )

        self.assertEqual(second["id"], 2)

    def test_invalid_amount(self):
        for bad in ("abc", -5, 0, "nan"):
            with self.assertRaises(ValueError):
                add_expense(self.expenses, bad, "Food")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            add_expense(self.expenses, 50, "Gaming")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            add_expense(
                self.expenses,
                50,
                "Food",
                "",
                "05-03-2026"
            )

    def test_delete_expense(self):
        add_expense(self.expenses, 40, "Study")

        self.assertTrue(
            delete_expense(self.expenses, 1)
        )

        self.assertFalse(
            delete_expense(self.expenses, 1)
        )

    def test_category_and_monthly_totals(self):
        add_expense(
            self.expenses,
            100,
            "Food",
            "",
            "2026-03-01"
        )

        add_expense(
            self.expenses,
            50.5,
            "Food",
            "",
            "2026-03-10"
        )

        add_expense(
            self.expenses,
            200,
            "Travel",
            "",
            "2026-04-02"
        )

        self.assertEqual(
            total_by_category(self.expenses),
            {"Food": 150.5, "Travel": 200}
        )

        self.assertEqual(
            monthly_total(self.expenses, 2026, 3),
            150.5
        )

    def test_save_and_load(self):
        add_expense(
            self.expenses,
            75,
            "Bills",
            "Internet",
            "2026-03-03"
        )

        with tempfile.TemporaryDirectory() as folder:

            path = Path(folder) / "data.json"

            save_expenses(self.expenses, path)

            self.assertEqual(
                load_expenses(path),
                self.expenses
            )

            missing_path = Path(folder) / "missing.json"

            self.assertEqual(
                load_expenses(missing_path),
                []
            )


if __name__ == "__main__":
    unittest.main()