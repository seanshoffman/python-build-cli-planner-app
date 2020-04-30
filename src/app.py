from database import add_reminder, list_reminders
from deadlined_reminders import DateReminder

def handle_input():
    choice = input("Choice: ")
    if choice == "3":
        return False

    if(choice == "1"):
        list_reminders()

    elif(choice == "2"):
        print()
        reminder = input("What would you like to be reminded about?: ")
        date = input('When is that due?:')

        add_reminder(reminder, date, DateReminder)
        list_reminders()
    else:
        print("Invalid menu option")

    return True

def print_menu():
    print()
    print('|--------------|')
    print('|  Pluralsight |')
    print('|   Reminders  |')
    print('|     App      |')
    print('|--------------|')
    print('* * * * * * * * *')
    print('Please select an option:')
    print()
    print('1) List reminders')
    print('2) Add a reminder')
    print('3) Exit')

def main():
    print_menu()
    while handle_input():
        print_menu()

main()
