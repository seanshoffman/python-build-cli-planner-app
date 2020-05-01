import pytest
import inspect

from abc import ABCMeta
from collections.abc import Iterable
from dateutil.parser import parse

import deadlined_reminders as dr

CONCRETE_CLASS_NAME = 'DateReminder'

@pytest.mark.task_three_class_exists_concrete
def test_task_three_classe_exists_concrete():
    assert hasattr(dr, CONCRETE_CLASS_NAME), \
        f'Could not find class `{CONCRETE_CLASS_NAME}` in `deadlined_reminders.py`'

    cls = getattr(dr, CONCRETE_CLASS_NAME)
    assert inspect.isclass(cls), f'`{CONCRETE_CLASS_NAME}` is not a class'

    assert issubclass(cls, dr.DeadlinedReminder), \
        f'{CONCRETE_CLASS_NAME} should subclass `DeadlinedReminder`'

    assert not cls.__abstractmethods__,\
        f'{CONCRETE_CLASS_NAME} should implement all virtual methods'


@pytest.mark.task_three_methods
@pytest.mark.parametrize('method_name', [
    '__iter__',
    'is_due'
])
def test_task_three_methods(method_name):
    cls = getattr(dr, CONCRETE_CLASS_NAME)
    assert hasattr(cls, method_name), f'Could not find `{method_name}` in `{CONCRETE_CLASS_NAME}`'

    reminder = cls('test_string', '01/01/2020')
    method = getattr(reminder, method_name)
    assert inspect.ismethod(method),\
        f'{method_name} is not a method on {CONCRETE_CLASS_NAME}. Did you forget `self` ?'

@pytest.mark.task_three_init
def test_init():
    cls = getattr(dr, CONCRETE_CLASS_NAME)
    reminder = cls('test_string', '01/01/2020')
    assert reminder.text == 'test_string', f'Incorrect text set in {CONCRETE_CLASS_NAME}.__init__()'
    assert reminder.date == parse('01/01/2020'), f'Incorrect date set in {CONCRETE_CLASS_NAME}.__init__()'

@pytest.mark.task_three_iter
def test_iter():
    cls = getattr(dr, CONCRETE_CLASS_NAME)
    reminder = cls('test_string', '01/01/2020')
    assert list(reminder) == ['test_string', '01/01/2020T00:00:00Z'],\
        f'Incorect iterable representation of {CONCRETE_CLASS_NAME}'

@pytest.mark.task_three_is_due
def test_is_due():
    cls = getattr(dr, CONCRETE_CLASS_NAME)
    reminder = cls('test_string', '01/01/2020')
    assert     reminder.is_due(), f'{CONCRETE_CLASS_NAME}.is_due() returns False for a past date'

    reminder = cls('test_string', '01/01/2034')
    assert not reminder.is_due(), f'{CONCRETE_CLASS_NAME}.is_due() returns True for a future date'

# TODO: should we test add_reminder() ? To check that it doesn't throw error and it writes to disk?
