# python-build-cli-planner-app

## Task one - Implementing an abstract base class as a regular Python class

One way to implement abstract base classes in Python is to use a regular class, and have each class method throw a `NotImplementedError` exception with the message `"Method not implemented"`. This ensures that subclasses override the abstract methods. This is the only way to implement abstract classes in Python prior to version 3.4.

In the file `src/regular_reminder.py`, create a class named `RegularReminder` with two class methods; `__iter__(self):`, and `is_due(self):`, both raising a `NotImplementedError` exception.

## Task two - Implementing an abstract base class using the ABCMeta Meta Class

The modern way of implementing Abstract Base Classes in Python is to use the `abc` package.

From the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract.

Create a class named `ABCMetaReminder` taking `ABCMeta` as its `metaclass` parameter. Add two methods, `__str__` and `is_due`, and set the method bodies to `pass`. Mark the methods with the `@abstractmethod` decorator.

## Task three - Implementing an abstract bsae class using the ABC Base Class

As an alternative to using the ABCMeta Meta Class, Python developers can use the ABC Class as a base class instead.

Create a new file under `src/abc_reminder.py`. From the package `abc`, import the `ABC` Class.

Create a class named `ABCReminder`, deriving from the `ABC` class. Set the body of the class to simply `pass`

### If it quacks like a duck

There's no task to complete here for the code below, but it's useful to know this. Did you know that in Python it's possible to have class behave as if it is a sub-class of a given class. For example, take this test written below to verify your code when implementing the previous task;

```python
def test_task_three_abc_class_1(self):
    ABCReminder.register(tuple)
    assert issubclass(tuple, ABCReminder)
    assert isinstance((), ABCReminder)
```

This test is checking whether you successfully implemented your `ABCReminder` class, derived from the `ABC` class. The test registers the class `tuple`, and then checks whether `tuple` is a subclass of `ABCReminder`, before checking whether an instance of a `tuple`, `()`, asserts True.