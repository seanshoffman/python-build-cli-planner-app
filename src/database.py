import csv
from basic_reminder import BasicReminder

def list_reminders():
    f = open("reminders.csv", "r")

    with f:
        reader = csv.reader(f)

        for row in reader:
            print()
            for e in row:
                print(e.ljust(32), end=' ')
        print()

def add_reminder():
    print()
    reminder = input("What would you like to be reminded about?: ")
    basic_reminder = BasicReminder(reminder)
    
    with open('reminders.csv', 'a+', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([basic_reminder])