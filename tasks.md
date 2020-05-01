# python-build-cli-planner-app

## Task one - Inheriting from a base class

We are not happy with the bland text of the reminders and we'd like them to have a prefix. Either some friendly text, or maybe some [text faces](textfac.es/).

In the file `src/reminder.py` you fill find the base class `PrefixedReminder`. Note its docstring.

In the same `src/reminder.py` file, create another class, `PoliteReminder`, which inherits from `PrefixedReminder`. Initiate its parent class by calling `super().__init__()` with a polite prefix (the prefix should contain the word *"please"*).

Now, in the file `src/database.py`, import your newly created `PoliteReminder` from `reminder` module.

Then find the function `add_reminder()`. It takes the string inputted by the user. Before opening the CSV file, create a `PoliteReminder` object from the `text` variable. Save it in a variable `reminder`. Then, in the call to `writerow()`, replace `text` with `reminder.text`.

### Intermediate test
Run `make` in the root directory and add some reminders. You should notice that all of them consist of your prefix string and some placeholder text, forgetting your input.

This is the disadvantage of inheriting from a normal class: although its docstring specified that children should override a property or a method, it cannot enforce them to do so. In the next module we will see how to fix this, but first, let's fix the app.

## Task two - Overriding properties from base class

In the file `src/reminder.py`, find the `__init__` method of your `PoliteReminder`. Set a property `text` on the objects equal to the concatenation of `self.prefix` and the `text` parameter. Now run the app again and you should see your reminders be prefixed with the polite string.

---

## Abstract base classes

Now we would like reminders to have a deadline. These can be of multiple types: on a day, at a given time, recurrent, etc. Each of these will represent their own python `class` but we want them to behave similarly, while avoiding the pitfalls of task 1. Therefore, they will inherit from an Abstract Base Class, which will enforce them to implement the required methods, namely `is_due()` and `__iter__()`, since they will need to serialize multiple fields.

The modern way of implementing Abstract Base Classes in Python is to use the `abc` package.

## Task three - Implementing an abstract base class using the `ABCMeta` Metaclass

Create a new file under `src` and name it `deadlined_reminders.py`. In there, from the package `abc`, import `ABCMeta` and `abstractmethod`. `ABCMeta` is the Meta Class which can be used to implement our Abstract Base Class, and `abstractmethod` is a decorator, which can be used to decorate methods as abstract. Note that not all methods on an Abstract Base Class need to be abstract. However, if *none* is abstract, then the class itself is no longer abstract.

Create a class named `DeadlinedMetaReminder` taking `ABCMeta` as its `metaclass` parameter. Add two methods, `__iter__()` and `is_due()`, and set the method bodies to `pass`. Mark the methods with the `@abstractmethod` decorator.

## Task four - Implementing an abstract base class by extending the `ABC` Class

Note that since python 3.4 you can also [create an Abstract Base Class by inheriting](https://docs.python.org/3/whatsnew/3.4.html#abc) from the `ABC` class of the `abc` module. This has the same effect as using the metaclass, with the small caveat that metaclass conflicts may be now hidden.

In the same `src/deadlined_reminders.py` file also import the `ABC` class from the `abc` module. Then create another abstract base class named `DeadlinedReminder`. This one should *inherit* from `ABC`.

Add the same two methods as `@abstractmethod`, namely `__iter__()` and `is_due()`.

For convenience, in the following tasks we will use the `DeadlinedReminder` as a base class.

## Task three - Implementing a class derived from an Abstract Base Class

Now that we have created our Abstract Base Class, we can create a class which implements it. An abstract base class cannot be instantiated, but when we derived a class from the ABC, it can be used to guide the implementation of the class.

### Implement the class

In the file under `src/deadlined_reminders.py` import `parse` from `dateutil.parser`, which is a really useful third-party module for parsing dates in Python. You'll also need `datetime` from the `datetime` package.

Then, create a class named `DateReminder` which derives from the `DeadlinedReminder` ABC.
There are three methods to implement on `DateReminder`: `__init__()`, `__iter__()` and `is_due()`.

`__init__()` takes a `text` and `date` parameter, alongside the usual `self`. Set `self.text = text`, and `self.date = parse(date)`. As your base class' `__init__()` is empty, there is no need to call it here.

The reminder will be serialized into CSV file, with each property on a column. The CSV writer expects an iterable for each row, so you should implement the `__iter__()` method to return an iterator. The iterator, in turn, would return first the reminder's `text`, then and the due date formatted to ISO8601. The easiest way to create this iterator is to use the builtin `iter([text, formatted_date])`. You can format the date using `self.date.strftime("%m/%d/%YT%H:%M:%SZ")`.

For the `is_due()` method, we want to check whether `self.date` is less than or equal to `datetime.now()`.

### Update the interface and database

You will have to ask the user for a date to go into your new reminder. In the file `src/app.py`, find the line `reminder = input(...)` under the case `"2"` of `handle_input()` function. Below it, add another input for the variable `date` asking `When is that due?:`. Then pass the `date` as a second parameter to the `add_reminder()` function.

In `src/database.py`, import the `DateReminder` class from `deadlined_reminders`.


In the same file, add a second argument to the function `add_reminder()`, naming it `date`.

In the same function, change the `reminder` variable to be a new instance of `DateReminder`, instead of `PoliteReminder`. You should construct this with the `text` and `date` received as parameters.

Since your reminders are now iterables, you can pass them directly to `writer.writerow()`, without the need for a list, i.e. `writer.writerow(reminder)`.

### Test your app

Run `make test` to ensure you have correctly followed the task. If all the tests pass, feel free to play with your app until you're ready for the next task.

## Module four - Opening the app up to future extension

Our reminders app is almost complete. As you have worked hard on it, you would like to push one step forward in order to benefit from cool reminders that other people have implemented. However, as you like to keep organized, you want to accept only those reminders which support a due date and, of course, which can be serialized to your database. Let's see how we can do this.

### Task 4.1 - Make `add_reminder()` accept a conforming reminder class

A reminder class conforms to the protocol if it subclasses our Abstract Base Class, namely `DeadlinedReminder`. In `src/database.py`, remove the imports for `DateReminder` and `PoliteReminder` and instead import `DeadlinedReminder`.

In the same file, add a third argument to `add_reminder` named `ReminderClass`. This will receive the desired *type* of reminder, which can be one of the previous two you have implemented, or a totally new one.

Then, check for compliance. Before instantiating the `reminder = ...`, check `if issubclass(ReminderClass, DeadlinedReminder)` and raise a `TypeError` if this is not the case, with the message `'Invalid Reminder Class'`.

Now, just below, change the variable `reminder = ...` to instantiate `ReminderClass` instead of `DateReminder`. We will assume that `ReminderClass()` constructor takes at least the same `text` and `date` parameters, and has sane defaults for the others.

In `src/app.py`, we want to import `DateReminder` class again, and pass it to the call to `add_reminder()` within `handle_input()`.

Check that your app still works.

### Task 4.2 - Accept any virtual subclass

In the file `src/external_reminders.py` you fill find a few reminder classes that are very similar to yours. Notably, there is `EveningReminder` which is always due at `8pm` on its given date. You would like to be able to add such a reminder to your database.

In the file `src/app.py` import `EveningReminder` from `external_reminders`. Then, change the call to `add_reminder()` to pass `EveningReminder` instead of `DateReminder`. Don't forget that you are passing the class, not an object.

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

This class method is called as part of `issublcass(ReminderClass, DeadlinedReminder)`. It checks that the given `subclass` contains the required methods `__iter__()` and `is_due()` anywhere in its hierarchy. If they are present, the class is considered to be a virtual subclass of `DeadlinedReminder`.

If you have implemented this correctly, you will see that when you run your app now the reminders that you add will have a third column indicating their time, and this should be `8pm`. The AbstractBaseClass is now recognizing `EveningReminder` as a subclass of its own because it implements the required methods.

## Task five - Alternatively checking for instances of reminders

Alternatively, instead of using `issubclass` to check the class, we can check instances of the class using `isinstance`.

In `src/database.py` move the creation of the `reminder` object above the class check. Then, since you have already instantiated the object, replace the call to `issubclass()` with `isinstance(reminder, DeadlinedReminder)`, still raising the `TypeError` when this fails.

Now we are checking whether an instance of a reminder class is valid, as opposed to the class itself. What could be the advantages of this ? Think back to task 4.1 (TODO: Adapt number), where we had to make an assumption about the parameters taken by the  constructor `ReminderClass()`. Using `isinstance()` would allow our `add_reminder()` function to receive the instance directly, thus delegating its construction to a code that knows how to do it better.

## Task six - One-time registration of a virtual subclass

> **If it quaks like a duck**

Before you finish off this project, you realize that back in task one you did some work that you can no longer use. Since `PoliteReminder` class it *not* implementing the prototype of `DeadlinedReminder`, passing it to `add_reminder()` would result in an error. However, the `is_due()` method of your protocol is not used anywhere yet, so you would be willing to give up the requirement of having a deadline on a reminder, as long as it asks you nicely not to remember the item.

Let's see how you can make `PoliteReminder` play nicely with `add_reminder()`, without downgrading the protocol. For this, we will benefit from Python's duck-typing, which allows you to use an object as long as it has the methods you need. (*If it quacks like a duck, and it walks like a duck, then it is a duck*)

Of the two methods of our protocol, the only method we use so far is `__iter__()`. So, in the file `src/reminder.py`, add the `__iter()__` method on `PoliteReminder` class, making it return an iterator through a list of 1 element, `[self.text]`.

Modify also the `__init__()` method to take a `date` parameter, with a default value `None`. This makes it compatible with other constructors. You do not have to use `date` in the body.

In `src/app.py` import the class `PoliteReminder` and add the base class `DeadlinedReminder` to the imports from `deadlined_reminders`. Then, at module level, you need instruct `DeadlinedReminder` to consider `PoliterReminder` as a subclass. You can do this through the `register()` method, which is available thanks to the inheritance from `ABC`/`ABCMeta`:
```python
DeadlinedReminder.register(PoliteReminder)
```

In the same file, in function `handle_input()` change the call to `add_reminder()` and pass `PoliteReminder` as the third parameter.

You can now use your app and note that `PoliteReminder`s without a date can now be added.
