# python-build-cli-planner-app

## Task one - Inheriting from a base class

We are not happy with the bland text of the reminders and we'd like them to have a prefix. Either some friendly text, or maybe some [text faces](textfac.es/).

In the file `src/reminder.py` you fill find the base class `PrefixedReminder`. Note its docstring.

In the same `src/reminder.py` file, create another class, `PoliteReminder`, which inherits from `PrefixedReminder`. Its `__init__()` should accept a `text` parameter; for now you don't need to use it. Initiate the parent class by calling `super().__init__()` with a polite prefix (the prefix should contain the word *"please"*).

Now, in the file `src/database.py`, import your newly created `PoliteReminder` from `src.reminder` module.

Then find the function `add_reminder()`. It takes the string inputted by the user. Before opening the CSV file, create a `PoliteReminder` object from the `text` variable. Save it in a variable `reminder`. Then, in the call to `writerow()`, replace `text` with `reminder.text`.

### Intermediate test
Test your app (see Readme) and add some reminders. You should notice that all of them consist of your prefix string and some placeholder text, forgetting your input.

This is the *disadvantage* of inheriting from a normal class: although its docstring specified that children should override a property or a method, it cannot enforce them to do so. In the next task we will see how to fix this, but first, let's fix the app.

## Task two - Overriding properties from base class

In the file `src/reminder.py`, find the `__init__` method of your `PoliteReminder`. Set a property `text` on the objects equal to the concatenation of `self.prefix` and the `text` parameter. Now run the app again and you should see your reminders be prefixed with the polite string.

---

## Abstract base classes

Now we would like reminders to have a deadline. These can be of multiple types: on a day, at a given time, recurrent, etc. Each of these will represent their own python `class` but we want them to behave similarly, while avoiding the pitfalls of task 1. Therefore, they will inherit from an Abstract Base Class, which will enforce them to implement two required methods:
-  `is_due()`, which will indicate whether the deadline of a reminder has passed
-  `__iter__()` which will allow our reminder to be serialized into a CSV file.

The modern way of implementing customised Abstract Base Classes in Python is to use the `abc` module, whereas for implementing some standard interfaces it is recommended to use the `collections.abc` submodule. We will see how to employ both.

## Task three - Implementing an abstract base class using the `ABCMeta` Metaclass

Create a new file under `src` and name it `deadlined_reminders.py`. In there, from the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract. Note that not all methods on an Abstract Base Class need to be abstract. However, if *none* is abstract, then the class itself is no longer abstract.

Also import the `Iterable` abstract base class from `collections.abc`.

Create a class named `DeadlinedMetaReminder` that inherits from `Iterable` and takes `ABCMeta` as its `metaclass` parameter. Add method `is_due()`, set the body to `pass` and mark it with the `@abstractmethod` decorator.

## Task four - Implementing an abstract base class by extending the `ABC` Class

Note that since python 3.4 you can also [create an Abstract Base Class by inheriting](https://docs.python.org/3/whatsnew/3.4.html#abc) from the `ABC` class of the `abc` module. This has the same effect as using the metaclass, with the small caveat that metaclass conflicts may be now hidden.

In the same `src/deadlined_reminders.py` file also import the `ABC` class from the `abc` module. Then create another abstract base class named `DeadlinedReminder`. Make it *inherit* from `ABC` instead of passing the `metaclass` parameter. Like above, it should also inherit from `Iterable`.

Then add the same `@abstractmethod` method as before, namely `is_due()`, with the body `pass`.

For convenience, in the following tasks we will use the `DeadlinedReminder` as a base class.

**NOTE:** Both `DeadlinedMetaReminder` and `DeadlinedReminder` have the two abstract methods we need: `__iter__()` comes from `Iterable` while `is_due()` was defined by us. Any class that extends any of them will have to implement both methods in order to be concrete.


## Implementing a class derived from an Abstract Base Class

Now that we have created our Abstract Base Class, we can create a class which implements it. An abstract base class cannot be instantiated, but when we derived a class from the ABC, it can be used to guide the implementation of the class.

## Task five - Implement the `DateReminder` class

In the file under `src/deadlined_reminders.py` import `parse` from `dateutil.parser`, which is a really useful third-party module for parsing dates in Python.

Then, create a class named `DateReminder` which derives from the `DeadlinedReminder` ABC. Its `__init__()` method takes a `text` and `date` parameter, alongside the usual `self`. Use the `parse()` function that you imported to store the `date` parameter onto `self`, and pass it the `dayfirst=True` keyword argument to avoid confusion for dates like `02/02/09`. Then store the `text` as it is onto the `self` object.

**NOTE:** As your base class' `__init__()` is empty, there is no need to call it here.

## Task six - Implement `is_due()` on `DateReminder`

In the same file, import `datetime` from the `datetime` package.

Your `DateReminder` is still abstract, as it does not implement all the abstract methods of the `DeadlinedReminder` ABC.

Therefore, you should create the `is_due()` method on the class, thus overriding the abstract one of the base class. Inside it, you should check whether `self.date` is less than or equal to `datetime.now()`.

## Task seven - Prepare `DateReminder` for serialization

As we mentioned when creating the `DeadlinedReminder` metaclass, we want our subclasses to implement the `Iterable` interface which allows the serialization to CSV to be implementation-agnostic.

The CSV writer expects an iterable for each row, so you should implement the `__iter__()` method to return an iterator. The iterator, in turn, would return first the reminder's `text`, then and the due date formatted to ISO8601. The easiest way to create this iterator is to use the builtin `iter([text, formatted_date])`. You can format the date using `self.date.isoformat()`.

## Task eight - Update the database and the interface

Now that you have reminders with multiple attributes, you need to create them and add them to the database.

In `src/database.py`, import the `DateReminder` class from `src.deadlined_reminders`.

In the same file, add a second argument to the function `add_reminder()`, naming it `date`.

In the same function, change the `reminder` variable to be a new instance of `DateReminder`, instead of `PoliteReminder`. You should construct this with the `text` and `date` received as parameters.

Since your reminders are now iterables, you can pass them directly to `writer.writerow()` below, without the need for a list, i.e. `writer.writerow(reminder)`.

You will also have to ask the user for a date to go into your new reminder. In the file `app.py`, find the line `reminder = input(...)` under the case `"2"` of `handle_input()` function. Below it, add another `input()` call for the variable `date` asking `When is that due?:`. Then pass the `date` as a second parameter to the `add_reminder()` function.


### Test your app

At this point, your app should be able to handle reminders with text and date. If the test for this task, together with the tests for all previous tasks, pass, feel free to play with the app until you're ready for the next task.

## Opening the app up to future extension

Our reminders app is almost complete. As you have worked hard on it, you would like to push one step forward in order to benefit from cool reminders that other people have implemented. However, as you like to keep organized, you want to accept only those reminders which support a due date and, of course, which can be serialized to your database. Let's see how we can do this.

## Task nine - Make `add_reminder()` accept a conforming reminder class

A reminder class conforms to the protocol if it subclasses our Abstract Base Class, namely `DeadlinedReminder`. In `src/database.py`, remove the imports for `DateReminder` and `PoliteReminder` and instead import `DeadlinedReminder`.

In the same file, add a third argument to `add_reminder` named `ReminderClass`. This will receive the desired *type* of reminder, which can be one of the previous two you have implemented, or a totally new one.

Then, check for compliance. Before instantiating the `reminder = ...`, check `if not issubclass(ReminderClass, DeadlinedReminder)` and raise a `TypeError` when this happens, with the message `'Invalid Reminder Class'`.

Now, just below, change the variable `reminder = ...` to instantiate `ReminderClass` instead of `DateReminder`. <a id='constructor-assumptions'></a>
We will assume that `ReminderClass()` constructor takes at least the same `text` and `date` parameters, and has sane defaults for the others.

In `app.py`, we want to import `DateReminder` class, and pass it as the 3rd argument to `add_reminder()` call within `handle_input()`.

Check that your app still works.

## Task ten - Accept any virtual subclass

In the file `src/external_reminders.py` you fill find a few reminder classes that are very similar to yours. Notably, there is `EveningReminder` which is always due at `8pm` on its given date. You would like to be able to add such a reminder to your database.

In the file `app.py` import `EveningReminder` from `external_reminders`. Then, change the call to `add_reminder()` to pass `EveningReminder` instead of `DateReminder`. Don't forget that you are passing the class, not an object.

If you play with your app at this point and try to add a reminder, you will notice that it no longer works. The protocol check that you have implemented above is not recognizing `EveningReminder` as a subclass of `DeadlinedReminder`. And, since it is external, you cannot make it inherit from your Abstract Base Class `DeadlinedReminder`. However, you notice that it *does* implement your protocol, defining the `__iter__()` and `is_due()` methods, which makes it a *virtual* subclass. Let's make `DeadlinedReminder` detect this.

Head over to `src/deadlined_reminders.py` and in the class `DeadlinedReminder` define a class method `__subclasshook__(cls, subclass)`, as follows:

```python
@classmethod
def __subclasshook__(cls, subclass):
    if cls is not DeadlinedReminder:
        return NotImplemented

    def attr_in_hierarchy(attr):
        return any (attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)

    if not all(attr_in_hierarchy(attr) for attr in ('__iter__', 'is_due')):
        return NotImplemented

    return True
```

This class method is called as part of `issubclass(ReminderClass, DeadlinedReminder)`. It checks that the given `subclass` contains the required methods `__iter__()` and `is_due()` anywhere in its hierarchy. If they are present, the class is considered to be a virtual subclass of `DeadlinedReminder`.

If you have implemented this correctly, you will see that when you run your app now the reminders that you add will have a third column indicating their time, and this should be `8pm`. The AbstractBaseClass is now recognizing `EveningReminder` as a subclass of its own because it implements the required methods.

## Task eleven - Alternatively checking for instances of reminders

Alternatively, instead of using `issubclass` to check the class, we can check instances of the class using `isinstance`.

In `src/database.py` move the creation of the `reminder` object above the class check. Then, since you have already instantiated the object, replace the call to `issubclass()` with `isinstance(reminder, DeadlinedReminder)`, still raising the `TypeError` when this fails. Note that now you are checking `reminder` rather than `ReminderClass`.

Now we are checking whether an *instance* of a `ReminderClass` class is valid, as opposed to the class itself. What could be the advantages of this ? Think back to task nine, where we had to [make an assumption](#constructor-assumptions) about the parameters taken by the constructor `ReminderClass()`. Using `isinstance()` would allow our `add_reminder()` function to receive the instance directly, thus delegating its construction to a code that knows how to do it better.

## Task twelve - One-time registration of a virtual subclass

> **If it quacks like a duck**

Before you finish off this project, you realize that back in task one you did some work that you can no longer use. Since `PoliteReminder` class it *not* implementing the prototype of `DeadlinedReminder`, passing it to `add_reminder()` would result in an error. However, the `is_due()` method of your protocol is not used anywhere yet, so you would be willing to give up the requirement of having a deadline on a reminder, as long as it asks you nicely to remember the item.

Let's see how you can make `PoliteReminder` play together with `add_reminder()`, without downgrading the protocol. For this, we will benefit from Python's duck-typing, which allows you to use an object as long as it has the methods you need. (*If it quacks like a duck, and it walks like a duck, then it is a duck*)

Of the two methods of our protocol, the only method we use so far is `__iter__()`. So, in the file `src/reminder.py`, add the `__iter()__` method on `PoliteReminder` class, making it return an iterator through a list of 1 element, `[self.text]`.

**NOTE:** We do not necessarily have to inherit from `collections.abc.Iterable` in order to make our `PoliteReminder` class behave like one. It suffices to implement the interface, namely the `__iter__()` method, for the class to be recognised as an `Iterable`. Behind the scenes, `Iterable` uses the same mechanism of `__subclasshook__()` like you have implemented in task ten, but it is only checking for this one method.

Now modify also the `__init__()` method to take a `date` parameter, with a default value `None`. This makes it compatible with other constructors. You do not have to use `date` in the body.

In `app.py` import the class `PoliteReminder` and add the base class `DeadlinedReminder` to the imports from `deadlined_reminders`. Then, at module level, you need instruct `DeadlinedReminder` to consider `PoliteReminder` as a subclass. You can do this through the `register()` method, which is available thanks to the inheritance from `ABC`/`ABCMeta`:
```python
DeadlinedReminder.register(PoliteReminder)
```

In the same file, in function `handle_input()` change the call to `add_reminder()` and pass `PoliteReminder` as the third parameter.

You can now use your app and note that `PoliteReminder`s without a date can now be added.
