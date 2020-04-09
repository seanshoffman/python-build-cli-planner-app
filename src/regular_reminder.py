class RegularReminder():

    def __iter__(self):
        raise NotImplementedError("Method not implemented")

    def is_due(self):
        raise NotImplementedError("Method not implemented")