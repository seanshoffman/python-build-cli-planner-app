from database import add_reminder, list_reminders

def handle_input(input):
    if(input == "1"):
        list_reminders()
        print_menu()
    elif(input == "2"):
        add_reminder("reminder")
        list_reminders()
        print_menu()
    else:
        print("Invalid menu option")
        print_menu()

def print_menu():
    print()
    print('|--------------|')
    print('|   Reminders  |')
    print('|     App      |')
    print('|--------------|')
    print('* * * * * * * * *')
    print('Please select an option:')
    print()
    print('1) List reminders')
    print('2) Add a reminder')
    choice = input("Choice: ")
    handle_input(choice)

def main():
    print_menu()

main()