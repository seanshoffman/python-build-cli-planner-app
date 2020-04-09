from abc import ABCMeta, abstractmethod

class ABCMetaReminder(metaclass=ABCMeta):

    @abstractmethod
    def __str__(self):
        pass
