from expense import Expense
from datetime import datetime, timedelta

def remaining_days_of_current_month():
    # Get the current date
    today = datetime.now()
    
    year = today.year
    month = today.month
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # First day of the next month
    first_day_next_month = datetime(next_year, next_month, 1)
    # Last day of the current month is one day before the first day of the next month
    last_day_current_month = first_day_next_month - timedelta(days=1)
    remaining_days = (last_day_current_month - today).days+1

    return remaining_days


def green(text):
    return  f"\033[92m{text}\033[0m"

def red(text):
    return  f"\033[91m{text}\033[0m"

def main():
    print(f"Running Expense Tracker!")
    expense_file_path="expenses.csv"
    budget=float(input("Enter your budget:"))

    while True:
        
        print("Enter your choice:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        choice=int(input())
        if choice==1:
            # Get user input for expense
            expense=get_user_expense()

            # Write expense to a csv file
            save_expense_to_file(expense, expense_file_path)

        elif choice==2:
            # Read file and summarize expense
            summarize_expense(expense_file_path,budget)

        elif choice==3:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
        
def get_user_expense():
    print(f"⌨️  Getting User Expense...")
    expense_name=input("Enter expense name:")
    expense_amount=float(input("Enter expense amount:"))

    expense_categories=[
        "🍕 Food", 
        "💸 Fees", 
        "📓 Stationary", 
        "🎈 Fun", 
        "✨ Other"
    ]

    while True:
        print(f"Select a category for your expense:")
        for i,category_name in enumerate(expense_categories):
            print(f"  {i+1}.{category_name}")

        value_range=f"[1-{len(expense_categories)}]"
        try:
           selected_index=int(input(f"Enter your category number {value_range}:"))-1

        except:
            print(f"Invalid category. Please enter a number {value_range}")
            continue

        if selected_index in range(0,len(expense_categories)):
            selected_category=expense_categories[selected_index]
            new_expense= Expense(name=expense_name,category=selected_category,amount=expense_amount)
            return new_expense

        else:
            print(f"Invalid category")


def save_expense_to_file(expense:Expense,expense_file_path):
    print(f"📁  Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path,'a',encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")


def summarize_expense(expense_file_path, budget):
    print(f"📝  Summarizing User Expense...")
    expenses: list[Expense] = []
    with open(expense_file_path,'r',encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            expense_name,expense_category,expense_amount=line.strip().split(",")
            #print(expense_name,expense_category,expense_amount)

            line_expense=Expense(name=expense_name,category=expense_category,amount=float(expense_amount))
            print(line_expense)
            expenses.append(line_expense)
    #print(expenses)

    amount_by_category={}
    for expense in expenses:
        key=expense.category
        if key in amount_by_category:
            amount_by_category[key]+=expense.amount
        else:
            amount_by_category[key]=expense.amount    
    print("Expenses by Category:")
    for key,amount in amount_by_category.items():
        print(f"  {key}: Rs.{amount:.2f}")

    total_spent=sum([x.amount for x in expenses])    
    print(f"Total spent: Rs.{total_spent:.2f}")

    remaining_budget=budget-total_spent

    if remaining_budget>=0:
        print(green(f"Budget remaining: Rs.{remaining_budget:.2f}"))
    else:
        print(red(f"You have exceeded your budget by Rs.{-remaining_budget:.2f}"))

    remaining_days=remaining_days_of_current_month()
    #print(f"Remaining days in the current month: {remaining_days}")

    daily_budget=remaining_budget/remaining_days

    if daily_budget>0:
        print(green(f"Budget per day: Rs.{daily_budget:.2f}"))
    else:
        print(red(f"No remaining budget for the current month"))    


if __name__ == "__main__":
    main()

