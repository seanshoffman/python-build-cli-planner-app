from abc_reminder import ABCReminder

class BasicReminder(ABCReminder):
    def __init__(self, reminder):
        self.reminder = reminder

    def __iter__(self):
        return self.reminder

    def is_due(self):
        return False