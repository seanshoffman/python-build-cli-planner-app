class RegularReminder():
    def __iter__(self):
        raise NotImplementedError("Abstract method has no implementation")

    def is_due(self):
        raise NotImplementedError("Abstract method has no implementation")