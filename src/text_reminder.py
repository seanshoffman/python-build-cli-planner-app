from reminder import Reminder

class TextReminder(Reminder):
    def __init__(self, reminder):
        self.reminder = "Hey, don't forget to " + reminder

    def __iter__(self):
        return self.reminder