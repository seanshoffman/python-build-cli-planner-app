"""This module implements some Reminder classes that we should
consider as "external", whose source we do not control.
"""
from dateutil.parser import parse
from collections.abc import Iterable
from datetime import datetime

class DateTimeReminder(Iterable):
    """A reminder which has a specific date and time for being due"""
    def __init__(self, text: str, date: str, time: str = '9am'):
        self.text = text
        self.date = parse(f'{date} {time}')
        self.time = self.date.time()

    def __iter__(self):
        return iter([self.text,
                     self.date.strftime("%m/%d/%YT%H:%M:%SZ"),
                     self.time.strftime('%I:%M %p')])

    def is_due(self):
        return self.date < datetime.now()


class MorningReminder(DateTimeReminder):
    """A reminder that is due at 9am"""
    def __init__(self, text: str, date: str):
        super().__init__(text, date, '9am')

class EveningReminder(DateTimeReminder):
    """A reminder that is due at 8pm"""
    def __init__(self, text: str, date: str):
        super().__init__(text, date, '8pm')
