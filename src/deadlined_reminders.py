from abc import ABC, ABCMeta, abstractmethod

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
