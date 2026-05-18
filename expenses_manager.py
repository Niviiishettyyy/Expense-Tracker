# Define the Expense class
class Expense:
    def __init__(self, date, amount, category, note=None, mood=None):
        self.date = date          # string in YYYY-MM-DD format
        self.amount = float(amount)
        self.category = category
        self.note = note
        self.mood = mood

    def __repr__(self):
        return f"Expense(date={self.date}, amount={self.amount}, category='{self.category}', note='{self.note}', mood='{self.mood}')"


# Global list to store expenses
expenses = []


# Function to add an expense
def add_expense(expense):
    if not isinstance(expense, Expense):
        raise TypeError("Invalid input. The 'expense' parameter should be an instance of Expense.")
    expenses.append(expense)


# Function to list all expenses
def list_expenses():
    if not expenses:
        print("No expenses recorded yet.")
    else:
        for i, e in enumerate(expenses, start=1):
            print(f"{i}. {e.date} | {e.amount} | {e.category} | {e.note or '-'} | {e.mood or '-'}")


# Function to delete an expense by index
def delete_expense(index):
    if 0 <= index < len(expenses):
        removed = expenses.pop(index)
        print(f"Deleted: {removed}")
    else:
        print("Invalid index.")


# Function to calculate total spent
def total_spent():
    return sum(e.amount for e in expenses)


# Function to export expenses to CSV
def export_csv(filename="expenses.csv"):
    import csv
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Amount", "Category", "Note", "Mood"])
        for e in expenses:
            writer.writerow([e.date, e.amount, e.category, e.note or "-", e.mood or "-"])
    print(f"Expenses exported to {filename}")


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    # Add some expenses
    e1 = Expense("2025-11-21", 500, "Food", "Lunch", "😍 Treat")
    e2 = Expense("2025-11-20", 1200, "Clothes", "Shoes", "😤 Regret")

    add_expense(e1)
    add_expense(e2)

    # List expenses
    print("All Expenses:")
    list_expenses()

    # Show total
    print("Total Spent:", total_spent())

    # Delete first expense
    delete_expense(0)

    # List again
    print("After Deletion:")
    list_expenses()

    # Export to CSV
    export_csv()
