from abc_reminder import ABCReminder
from dateutil.parser import parse
from datetime import datetime

class DateReminder(ABCReminder):
    def __init__(self, reminder, date):
        self.reminder = reminder
        self.date = parse(date)
    
    def __iter__(self):
        return iter([self.reminder,self.date.strftime("%m/%d/%YT%H:%M:%SZ")])

    def is_due(self):
        return self.date <= datetime.now()