from abc import ABC, abstractmethod

class ABCReminder(ABC):

    @abstractmethod
    def __str__(self):
        pass