# python-build-cli-planner-app

## Task one - Implementing an abstract base class as a regular Python class

One way to implement abstract base classes in Python is to use a regular class, and have each class method throw a `NotImplementedError` exception with the message `"Abstract method has no implementation."`. This ensures that subclasses override the abstract methods. This was the only way to implement abstract classes in Python prior to the introduction of Abstract Base Clases [PEP3119](https://www.python.org/dev/peps/pep-3119/).

The main disadvantage of this method is that the abstract base class can still be instantiated, and the error is only encountered upon calling an abstract method. We will fix this in later tasks.

In the file `src/regular_reminder.py`, create a class named `RegularReminder` with two class methods; `__iter__(self)`, which raises a `NotImplementedError` with the message `Abstract method '__iter__' should not be called`, and `is_due(self)`, which raises a `NotImplementedError` with the message `Abstract method 'is_due' should not be called`.

## Task two - Implementing an abstract base class using the ABCMeta Meta Class

The modern way of implementing Abstract Base Classes in Python is to use the `abc` package.

Create a new file under `src/abc_meta_reminder`. From the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract. A metaclass is a esoteric Python feature which is essentially the class of a class. It defines how the class behaves; in this case as an abstract class!

Create a class named `ABCMetaReminder` taking `ABCMeta` as its `metaclass` parameter. Add two methods, `__iter__` and `is_due`, and set the method bodies to `pass`. Mark the methods with the `@abstractmethod` decorator.

## Task three - Implementing an abstract bsae class using the ABC Base Class

As an alternative to using the ABCMeta Meta Class, Python developers can use the ABC Class as a base class instead. It is quicker to type, and an easier way to add Abstract Base Classes to your Python code. By extending the ABC class, you'll just end up using the Metaclass underneath;

```python
class ABC(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    pass
```

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

Within the filter writer on Line 20, change `writer.writerow([reminder])` to `writer.writerow(basic_reminder)`.

## Task five - Adding dates to reminders and implementing `is_due`

Create a file under `src/date_reminder.py`. From the package `abc_reminder`, import ABCReminder again. You'll also need `parse` from `dateutil.parser`, which is a really useful third-party module for parsing dates in Python. You'll also need `datetime` from the `datetime` package.

Just like with `BasicReminder`, we need an `__init__` function, but this time taking both a `reminder` and `date` parameter, alongside the usual `self`. Set `self.reminder = reminder`, and `self.date = parse(date)`.

We also want to define a `__iter__` method. Here, we want to return an iteration of the reminder text, and the due date formatted to ISO8601. Set the body of the method to `return iter([self.reminder,self.date.strftime("%m/%d/%YT%H:%M:%SZ")])`

For the `is_due` method, we want to check whether `self.date` is less than or equal to `datetime.now()`

In `src/database.py`, below `reminder = input(...)`, add an input for the variable `date` asking `When is that due?:`. Replace the variable `basic_reminder = ...` with `date_reminder = DateReminder(reminder, date)`. You'll need to import `DateReminder` from `date_reminder` at the top.

Replace `writer.writerow(basic_reminder)` with `writer.writerow(date_reminder)`

## Task six - Opening the app up to future extension

Our reminders app is almost complete. One final feature we want to implement is to open it up to being extended to different types of reminders in the future. We can do this by modifing `src/database.py` to not import the reminder class itself, but instead to take a parameter containing the class to instantiate as a reminder.

In `src/database.py`, add a parameter to `add_reminder` of `ReminderClass`. Change the line `date_reminder = ...` to instantiate `ReminderClass` instead of `DateReminder`. In `src/app.py`, we want to import `DateReminder` class again, and pass it to the call to `add_reminder` within `handle_input`.

To guard against runtime errors and to prevent any class being passed as a reminder, we can implement subclass check on the class. To do this, wrap the body of the `add_reminder` method in `if issubclass(ReminderClass, ABCReminder):`. You'll need to import `ABCReminder`.

We need to implement the subclass check in our Abstract Base Class. Head over to `src/abc_reminder.py` and add a new method, `__subclasshook__` as follows;

```python
@classmethod
def __subclasshook__(cls, C):
    if cls is not ABCReminder:
        return NotImplemented

    if C == tuple:
        return True

    for attr in ('__iter__', 'is_due'):
        if not hasattr(C, attr):
            return False

    return True
```

This method checks that the given class contains the required `__iter__` and `is_due` methods. If they are prevent, the class is considered to be a subclass of ABCReminder.

## Task seven - Alternatively checking for instances of reminders

Alternatively, instead of using `issubclass` to check the class, we can check instances of the class instead using `isinstance`.

Update `src/database.py` and remove the `if issubclass(ReminderClass, ABCReminder)` wrapper.

After the creation of the `date_reminder` class, add the following statement;

```python
if isinstance(date_reminder, ABCReminder):
    raise Exception("Invalid reminder instance")
```

Here, we are checking whether an instance of a reminder class is valid, as oppose to the class itself.