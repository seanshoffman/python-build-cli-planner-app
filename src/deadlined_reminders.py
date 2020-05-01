from abc import ABC, ABCMeta, abstractmethod
from dateutil.parser import parse
from datetime import datetime

class DeadlinedMetaReminder(metaclass=ABCMeta):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def is_due(self):
        pass

class DeadlinedReminder(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def is_due(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is not DeadlinedReminder:
            return NotImplemented

        def attr_in_hierarchy(attr):
            return any(attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)

        if not all(attr_in_hierarchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented

        return True


class DateReminder(DeadlinedReminder):
    def __init__(self, text, date):
        self.text = text
        self.date = parse(date)

    def __iter__(self):
        return iter([self.text, self.date.strftime("%m/%d/%YT%H:%M:%SZ")])

    def is_due(self):
        return self.date < datetime.now()
