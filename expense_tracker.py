# -*- coding: utf-8 -*-
"""
Simple Expense Tracker - Command Line Interface (CLI)
Allows adding expenses, saving them to a CSV file, and showing a simple summary by category.

Run: python expense_tracker.py
"""

import csv
import os
from datetime import datetime

CSV_FILE = os.path.join(os.path.dirname(__file__), 'expenses.csv')
FIELDNAMES = ['date', 'category', 'amount', 'description']


def normalize_number_str(s: str) -> str:
    """Normalize numbers entered with Arabic-Indic or Persian digits and common Arabic separators to ASCII/English form.
    Examples:
      '١٢٫٥٠' -> '12.50'
      '۱٬۲۰۰'  -> '1200'
    """
    if s is None:
        return s
    s = s.strip()
    trans = str.maketrans({
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
        '٫': '.', '٬': '', '،': '', ',': '.'
    })
    return s.translate(trans)


def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    ensure_csv_exists()
    expenses = []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                amt_str = normalize_number_str(r.get('amount', ''))
                r['amount'] = float(amt_str) if amt_str != '' else 0.0
            except Exception:
                r['amount'] = 0.0
            expenses.append(r)
    return expenses


def add_expense():
    print('\nAdd a new expense:')
    category = input('Category (e.g. Food, Transport, Bills): ').strip() or 'General'
    while True:
        amount_s = input('Amount (e.g. 12.50): ').strip()
        try:
            # Normalize Arabic/Persian digits and separators to ASCII before parsing
            amount_norm = normalize_number_str(amount_s)
            amount = float(amount_norm)
            break
        except Exception:
            print('Please enter a valid numeric amount (you can use 12.50 or ١٢٫٥٠).')
    description = input('Short description (optional): ').strip()
    date = input('Date (YYYY-MM-DD) press Enter for today: ').strip()
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    expense = {'date': date, 'category': category, 'amount': f"{amount:.2f}", 'description': description}

    ensure_csv_exists()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(expense)
    print('Expense added.')


def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print('\nNo saved expenses.')
        return
    print('\nExpenses list:')
    print('-' * 50)
    for i, e in enumerate(expenses, 1):
        # display amount in English numeric format with two decimals
        amount_display = f"{e['amount']:.2f}"
        print(f"{i}. {e['date']} | {e['category']} | {amount_display} | {e['description']}")
    print('-' * 50)


def report_summary():
    expenses = load_expenses()
    total = sum(e['amount'] for e in expenses)
    by_cat = {}
    for e in expenses:
        by_cat.setdefault(e['category'], 0.0)
        by_cat[e['category']] += e['amount']

    print('\nSummary report:')
    print(f"Number of entries: {len(expenses)}")
    print(f"Total amount: {total:.2f}")
    print('\nTotal by category:')
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f" - {cat}: {amt:.2f}")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    while True:
        print('\n=== Simple Expense Tracker ===')
        print('1) Add expense')
        print('2) View expenses')
        print('3) Summary report')
        print('4) Exit')
        choice = input('Choose a number: ').strip()
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            report_summary()
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            print('Invalid choice, try again.')


if __name__ == '__main__':
    main()
