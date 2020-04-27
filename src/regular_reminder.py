class RegularReminder():
    def __iter__(self):
        raise NotImplementedError("Abstract method '__iter__' should not be called")

    def is_due(self):
        raise NotImplementedError("Abstract method 'is_due' should not be called")