from .abc_reminder import ABCReminder

class BasicReminder(ABCReminder):
    def __init__(self, reminder):
        self.reminder = reminder

    def __str__(self):
        return self.reminder