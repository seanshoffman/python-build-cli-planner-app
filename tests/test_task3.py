import pytest
import inspect

from abc import ABCMeta
from collections.abc import Iterable
from dateutil.parser import parse

import deadlined_reminders as dr

class_name = 'DateReminder'

@pytest.mark.task_three_class_exists_concrete
def test_task_three_classe_exists_concrete():
    assert hasattr(dr, class_name), \
        f'Could not find class `{class_name}` in `deadlined_reminders.py`'

    cls = getattr(dr, class_name)
    assert inspect.isclass(cls), f'`{class_name}` is not a class'

    assert issubclass(cls, dr.DeadlinedReminder), \
        f'{class_name} should subclass `DeadlinedReminder`'

    assert not cls.__abstractmethods__,\
        f'{class_name} should implement all virtual methods'


@pytest.mark.task_three_methods
@pytest.mark.parametrize('method_name', [
    '__iter__',
    'is_due'
])
def test_task_three_methods(method_name):
    cls = getattr(dr, class_name)
    assert hasattr(cls, method_name), f'Could not find `{method_name}` in `{class_name}`'

    reminder = cls('test_string', '01/01/2020')
    method = getattr(reminder, method_name)
    assert inspect.ismethod(method),\
        f'{method_name} is not a method on {class_name}. Did you forget `self` ?'

@pytest.mark.task_three_init
def test_init():
    cls = getattr(dr, class_name)
    reminder = cls('test_string', '01/01/2020')
    assert reminder.text == 'test_string', f'Incorrect text set in {class_name}.__init__()'
    assert reminder.date == parse('01/01/2020'), f'Incorrect date set in {class_name}.__init__()'

@pytest.mark.task_three_iter
def test_iter():
    cls = getattr(dr, class_name)
    reminder = cls('test_string', '01/01/2020')
    assert list(reminder) == ['test_string', '01/01/2020T00:00:00Z'],\
        f'Incorect iterable representation of {class_name}'

@pytest.mark.task_three_is_due
def test_is_due():
    cls = getattr(dr, class_name)
    reminder = cls('test_string', '01/01/2020')
    assert     reminder.is_due(), f'{class_name}.is_due() returns False for a past date'

    reminder = cls('test_string', '01/01/2034')
    assert not reminder.is_due(), f'{class_name}.is_due() returns True for a future date'

# TODO: should we test add_reminder() ? To check that it doesn't throw error and it writes to disk?
