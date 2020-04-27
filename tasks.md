# python-build-cli-planner-app

## Task one - Implementing an abstract base class as a regular Python class

One way to implement abstract base classes in Python is to use a regular class, and have each class method throw a `NotImplementedError` exception with the message `"Method not implemented"`. This ensures that subclasses override the abstract methods. With this implementation, you are still able to instantiate the class, but will receive errors when attempting to call its methods. This is the only way to implement abstract classes in Python prior to version 3.0.

In the file `src/regular_reminder.py`, create a class named `RegularReminder` with two class methods; `__iter__(self)`, which raises a `NotImplementedError` with the message `Abstract method '__iter__' should not be called`, and `is_due(self)`, which raises a `NotImplementedError` with the message `Abstract method 'is_due' should not be called`.
