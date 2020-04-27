# python-build-cli-planner-app

## Task one - Implementing an abstract base class as a regular Python class

One way to implement abstract base classes in Python is to use a regular class, and have each class method throw a `NotImplementedError` exception with the message `"Abstract method has no implementation."`. This ensures that subclasses override the abstract methods. This was the only way to implement abstract classes in Python prior to the introduction of Abstract Base Clases [PEP3119](https://www.python.org/dev/peps/pep-3119/).

The main disadvantage of this method is that the abstract base class can still be instantiated, and the error is only encountered upon calling an abstract method. We will fix this in later tasks.

In the file `src/regular_reminder.py`, create a class named `RegularReminder` with two class methods; `__iter__(self)`, which raises a `NotImplementedError` with the message `Abstract method '__iter__' should not be called`, and `is_due(self)`, which raises a `NotImplementedError` with the message `Abstract method 'is_due' should not be called`.

## Task two - Implementing an abstract base class using the ABCMeta Meta Class

The modern way of implementing Abstract Base Classes in Python is to use the `abc` package.

Create a new file under `src/abc_meta_reminder`. From the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract.

Create a class named `ABCMetaReminder` taking `ABCMeta` as its `metaclass` parameter. Add two methods, `__iter__` and `is_due`, and set the method bodies to `pass`. Mark the methods with the `@abstractmethod` decorator.