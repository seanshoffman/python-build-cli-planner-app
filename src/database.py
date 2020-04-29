import csv

def list_reminders():
    f = open("reminders.csv", "r")

    with f:
        reader = csv.reader(f)

        for row in reader:
            print()
            for e in row:
                print(e.ljust(32), end=' ')
        print()

<<<<<<< HEAD
def add_reminder():
=======
def add_reminder(reminder):
>>>>>>> 953bcebd1437acfa83993b25cca4faf463989db8
    print()
    reminder = input("What would you like to be reminded about?: ")
    
    with open('reminders.csv', 'a+', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([reminder])