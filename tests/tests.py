import pytest
import inspect

@pytest.mark.task_one_regular_class_1
def test_task_one_exists():
    import regular_reminder
    assert 'RegularReminder' in dir(regular_reminder), 'Could not find class `RegularReminder` in regular_reminder.py'
    assert inspect.isclass(regular_reminder.RegularReminder), '`RegularReminder` is not a class'

@pytest.mark.task_one_regular_class_2
@pytest.mark.parametrize('abstract_method_name', [
    "__iter__",
    "is_due"
])
def test_task_one_abstract_method(abstract_method_name):
    from regular_reminder import RegularReminder
    assert hasattr(RegularReminder, abstract_method_name), f'Could not find `{abstract_method_name}` in `RegularReminder`'

    reminder = RegularReminder()
    abstract_method = getattr(reminder, abstract_method_name)
    assert inspect.ismethod(abstract_method), 'f`{abstract_method_name}` is not a method. Have you forgotten `self`?'

    with pytest.raises(NotImplementedError) as e:
        assert abstract_method(), "Failed to raise the correct error type"

    assert str(e.value) == "Abstract method has no implementation", \
           f"Error message does not match 'Abstract method has no implementation' for method `{abstract_method_name}`"

@pytest.mark.task_two_abc_meta_class_1
def test_task_two_exists():
    import abc_meta_reminder
    assert 'ABCMetaReminder' in dir(abc_meta_reminder), 'Could not find class `ABCMetaReminder` in abc_meta_reminder.py'
    assert inspect.isclass(abc_meta_reminder.ABCMetaReminder), '`ABCMetaReminder` is not a class'

@pytest.mark.task_two_abc_meta_class_2
def test_task_two_abc_meta_class_1():
    from abc_meta_reminder import ABCMetaReminder
    from typing import Iterable
    assert issubclass(ABCMetaReminder, Iterable), "Could not find ABCMetaReminder to be Iterable"

@pytest.mark.task_two_abc_meta_class_3
@pytest.mark.parametrize('abstract_method_name', [
    "__iter__",
    "is_due"
])
@pytest.mark.xfail(raises=TypeError, reason='You did not add the @abstractmethod decorator to ABCMetaReminder\'s methods')
def test_task_two_abc_meta_class_2(abstract_method_name):
    from abc_meta_reminder import ABCMetaReminder
    assert hasattr(ABCMetaReminder, abstract_method_name), f'Could not find `{abstract_method_name}` in `RegularReminder`'
    with pytest.raises(TypeError) as e:
        abc_meta = ABCMetaReminder()

    assert str(e.value) == "Can't instantiate abstract class ABCMetaReminder with abstract methods __iter__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __iter__, is_due"

@pytest.mark.task_three_abc_class_1
def test_task_three_abc_class_1():
    from abc_reminder import ABCReminder
    ABCReminder.register(tuple)
    assert issubclass(tuple, ABCReminder)
    assert isinstance((), ABCReminder)

@pytest.mark.task_three_abc_class_2
def test_task_three_abc_class_2():
    from abc_reminder import ABCReminder
    with pytest.raises(TypeError) as e:
        abc = ABCReminder()
    assert str(e.value) == "Can't instantiate abstract class ABCReminder with abstract methods __iter__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __iter__, is_due"

@pytest.mark.task_four_basic_reminder_class_1
def test_task_four_basic_reminder_class_1():
    from basic_reminder import BasicReminder
    from abc_reminder import ABCReminder
    basic = BasicReminder("Buy 6 eggs")
    assert issubclass(BasicReminder, ABCReminder), "BasicReminder is not not a subclass of ABCReminder"
    assert isinstance(basic, ABCReminder), "BasicReminder is not not a subclass of ABCReminder"
    assert hasattr(basic, "reminder"), "BasicReminder is missing the property 'reminder'"
    assert basic.reminder == "Buy 6 eggs", "BasicReminder is not taking a single constructor parameter and setting the class property 'reminder'"

@pytest.mark.task_five_date_reminder_class_1
def test_task_five_date_reminder_class_1():
    from date_reminder import DateReminder
    from datetime import datetime
    date = DateReminder("Buy 6 eggs", "2020-01-31 15:00:00")
    assert date.is_due() == True, "The is_due method was not implemented correctly to compare the date property against the current time"
    assert date.reminder == "Buy 6 eggs", "DateReminder is not taking a reminder constructor parameter and setting the class property 'reminder'"
    assert date.date == datetime(2020, 1, 31, 15, 0), "DateReminder is not taking a date constructor parameter and setting the class property `parse(date)`"

@pytest.mark.task_six_issubclass_1
def test_task_six_issubclass_1():
    from abc_reminder import ABCReminder
    class FakeReminder():
        def __iter__(self):
            pass

        def is_due(self):
            pass

    assert issubclass(FakeReminder, ABCReminder), "__subclasshook__ is not checking for the presence of __iter__ and is_due methods"

@pytest.mark.task_seven_isinstance_1
def test_task_seven_isinstance_1():
    from abc_reminder import ABCReminder
    class FakeReminder():
        def __iter__(self):
            pass

        def is_due(self):
            pass

    fake = FakeReminder()

    assert isinstance(fake, ABCReminder), "__subclasshook__ is not checking for the presence of __iter__ and is_due methods"