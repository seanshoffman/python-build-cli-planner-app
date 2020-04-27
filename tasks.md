# python-build-cli-planner-app

## Task one - Implementing an abstract base class as a regular Python class

One way to implement abstract base classes in Python is to use a regular class, and have each class method throw a `NotImplementedError` exception with the message `"Method not implemented"`. This ensures that subclasses override the abstract methods. With this implementation, you are still able to instantiate the class, but will receive errors when attempting to call its methods. This is the only way to implement abstract classes in Python prior to version 3.0.

In the file `src/regular_reminder.py`, create a class named `RegularReminder` with two class methods; `__iter__(self)`, which raises a `NotImplementedError` with the message `Abstract method '__iter__' should not be called`, and `is_due(self)`, which raises a `NotImplementedError` with the message `Abstract method 'is_due' should not be called`.

## Task two - Implementing an abstract base class using the ABCMeta Meta Class

The modern way of implementing Abstract Base Classes in Python is to use the `abc` package.

From the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract.

Create a class named `ABCMetaReminder` taking `ABCMeta` as its `metaclass` parameter. Add two methods, `__iter__` and `is_due`, and set the method bodies to `pass`. Mark the methods with the `@abstractmethod` decorator.

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

## Task four - Implementing a class derived from an Abstract Base Class

Now that we have created our Abstract Base Class, we can create a class which implements it. An abstract base class cannot be instantiated, but when we derived a class from the ABC, it can be used to guide the implementation of the class.

### Implement the class

Create a new file under `src/basic_reminder.py`. From the package `abc_reminder`, import `ABCReminder`. Create a class named `BasicReminder` which derives from the `ABCReminder` ABC.

There are three methods to implement on `BasicReminder`:

1. `__init__`, which takes a `reminder` string parameter, and sets `self.reminder = reminder`
2. `__iter__` which returns `iter([self.reminder])`.
3. `is_due` which returns `False`

### Update src/database.py

In `src/database.py`, import the `BasicReminder` class from `basic_reminder`. In `add_reminder`, add a variable named `basic_reminder` and set it to a new instance of `BasicReminder` with the `reminder` variable passed to the constructor.

Within the filter writer on Line 20, change `writer.writerow([reminder])` to `writer.writerow([basic_reminder])`.