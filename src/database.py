import csv
from date_reminder import DateReminder
from abc_reminder import ABCReminder

def list_reminders():
    f = open("reminders.csv", "r")

    with f:
        reader = csv.reader(f)

        for row in reader:
            print()
            for e in row:
                print(e.ljust(32), end=' ')
        print()

def add_reminder(ReminderClass):
    if issubclass(ReminderClass, ABCReminder):
        print()
        reminder = input("What would you like to be reminded about?: ")
        date = input("When is that due?: ")
        date_reminder = ReminderClass(reminder, date)

        with open('reminders.csv', 'a+', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow(date_reminder)