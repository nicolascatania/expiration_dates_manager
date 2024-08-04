import json
import sys
import os
from datetime import datetime, timedelta, date

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_dir, 'expdates.json')

def check_and_create_json():
    if not os.path.isfile(json_file):
        with open(json_file, 'w') as file:
            json.dump([], file) 


def load_exp_dates():
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_exp_dates(data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def see_exp_dates():
    expiration_dates = load_exp_dates()
    if expiration_dates:
        for i, exp_date in enumerate(expiration_dates, 1):
            print(f"{i}. Description: {exp_date['description']}, Expiration Date: {exp_date['expiration_date']}")
    else:
        print("No expiration dates available.")

def input_date(prompt="Enter a date (YYYY-MM-DD): "):
    while True:
        user_input = input(prompt)
        try:
            # Intenta convertir la entrada del usuario en un objeto datetime
            user_date = datetime.strptime(user_input, '%Y-%m-%d').date()
            return user_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def add_exp_date():
    while True:
        try:
            option = int(input("1)Consumable (like medications pills)\n2)Item with fixed expiration date\nSelect an option: "))
            if option in [1, 2]:
                break
            else:
                print("Invalid option. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    expiration_dates = load_exp_dates()
    
    description = input("Enter description (e.g., medication name): ")
    
    if option == 1:
        quantity = int(input("Enter the quantity of consumables you have: "))
        daily_usage = int(input("Enter the number of consumables you take per day: "))
        days_to_expire = quantity // daily_usage
        expiration_date = date.today() + timedelta(days=days_to_expire)
    else:
        expiration_date = input_date("Enter the expiration date (YYYY-MM-DD): ")

    new_entry = {
        "description": description,
        "expiration_date": expiration_date.isoformat()
    }
    
    expiration_dates.append(new_entry)
    save_exp_dates(expiration_dates)
    print(f"New expiration date added: {description} will expire on {expiration_date.isoformat()}.")

def delete_exp_date():
    expiration_dates = load_exp_dates()
    see_exp_dates()
    index = int(input("Enter the number of the expiration date to delete: ")) - 1
    if 0 <= index < len(expiration_dates):
        deleted = expiration_dates.pop(index)
        save_exp_dates(expiration_dates)
        print(f"Deleted expiration date: {deleted['description']} on {deleted['expiration_date']}")
    else:
        print("Invalid index.")

def invalid_option():
    print('Invalid option.')

def show_menu():
    print('Welcome to EXPIRATION DATES MANAGER')
    print('1) See expiration dates')
    print('2) Add new expiration date')
    print('3) Delete expiration date')
    print('0) Exit')

def select_option():
    options = {
        1: see_exp_dates,
        2: add_exp_date,
        3: delete_exp_date,
        0: sys.exit
    }
    
    show_menu()
    while True:
        try:
            option = int(input("Select an option: "))
            options.get(option, invalid_option)()
        except ValueError:
            print("Invalid entry, please insert a number.")

if __name__ == "__main__":
    try:
        check_and_create_json() 
        select_option()
    except Exception as e:
        print("An unexpected error occurred:")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")