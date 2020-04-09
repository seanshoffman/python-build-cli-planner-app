from abc import ABC, abstractmethod

class ABCReminder(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def is_due(self):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is not ABCReminder:
            return NotImplemented

        if C == tuple:
            return True
        
        for attr in ('__iter__', 'is_due'):
            if not hasattr(C, attr):
                return False

        return True