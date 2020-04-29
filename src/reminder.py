class Reminder():
    def __init__(self, reminder):
        self.reminder = "Hey, don't forget to "

    def __iter__(self):
        return self.reminder
