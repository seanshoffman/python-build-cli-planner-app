from abc import ABC, abstractmethod

class ABCReminder(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_due(self):
        pass