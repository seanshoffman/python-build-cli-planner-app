import pytest
import inspect
import re

import app
import database
from deadlined_reminders import DateReminder, DeadlinedReminder
from external_reminders import EveningReminder

from reminder import PoliteReminder

class DummyReminder:
    def __init__(self, *args, **kwargs):
        pass


@pytest.mark.task_4_correct_imports
def test_app_opening_correct_imports():
    assert not hasattr(database, 'PoliteReminder'),\
        'You should no longer import `PoliteReminder` in `database`'
    assert not hasattr(database, 'DateReminder'),\
        'You should no longer import `DateReminder` in `database`'

    assert hasattr(database, 'DeadlinedReminder'),\
        'You should import `DeadlinedReminder` in `database`'


@pytest.mark.task_4_add_reminder_third_parameter
def test_app_opening_add_reminder_third_parameter():
    signature = inspect.signature(database.add_reminder)
    params = list(signature.parameters)
    assert len(params) == 3,\
        'You should pass a third parameter to `add_reminder`'
    assert params[2] == 'ReminderClass',\
        'The third parameter should be `ReminderClass`'


@pytest.mark.task_4_add_reminder_date
def test_app_opening_add_reminder_date():
    database.add_reminder('test_reminder', '1/1/2020', DateReminder)

@pytest.mark.task_4_add_reminder_incorrect
def test_app_opening_add_reminder_incorrect():
    # NOTE: pytest.raises(TypeError) does not work here as we want custom message
    #       for the other exceptions, which would bubble up otherwise
    try:
        database.add_reminder('test_reminder', '1/1/2020', DummyReminder)
    except TypeError as e:
        pass
    except Exception:
        pytest.fail('You should only allow conforming classes in `add_reminder`.'
                    ' Did you forget `issubclass()`?')


@pytest.mark.task_4_subclasshook
def test_app_opening_subclasshook():
    assert '__subclasshook__' in DeadlinedReminder.__dict__,\
        'Could not find `__subclasshook__` onto `DeadlinedReminder`'

    # NOTE: we should not getattr, as that one is bound *to the class* and the check fails
    hook = DeadlinedReminder.__dict__['__subclasshook__']
    assert isinstance(hook, classmethod),\
        '`__subclasshook__` should be a classmethod'

    assert issubclass(EveningReminder, DeadlinedReminder),\
        '`__subclasshook__` gives wrong result for class that'\
            ' respects the protocol of `DeadlinedReminder`'

    assert not issubclass(DummyReminder, DeadlinedReminder),\
        '`__subclasshook__` gives wrong result for class that '\
            ' does not respect the protocol of `DeadlinedReminder`'

@pytest.mark.task_4_add_reminder_evening
def test_app_opening_add_reminder_evening():
    assert hasattr(app, 'EveningReminder'),\
        'You did not import/use `EveningReminder` in `app.py`'

    try:
        database.add_reminder('test_reminder', '1/1/2020', EveningReminder)
    except Exception as exc:
        pytest.fail('Could not pass an `EveningReminder` to `add_reminder`')


@pytest.mark.task_5_add_reminder_isinstance
def test_app_opening_add_reminder_isinstance():
    code_lines, starts_on = inspect.getsourcelines(database.add_reminder)
    EXISTS_LINE_WITH_issubclass = any('issubclass' in line for line in code_lines)
    assert not EXISTS_LINE_WITH_issubclass,\
        'You should remove the `issubclass` check'

    IDX_LINE_WITH_isinstance = None
    IDX_LINE_WITH_constructor = None
    for idx, line in enumerate(code_lines):
        if re.findall(r'ReminderClass\(.*\)', line):
            IDX_LINE_WITH_constructor = idx
            break

    for idx, line in enumerate(code_lines):
        if re.findall(r'isinstance\(.*\)', line):
            IDX_LINE_WITH_isinstance = idx
            assert 'ReminderClass' not in line,\
                'You should call `isinstance` with the instance, not the class'
            break

    assert IDX_LINE_WITH_isinstance is not None,\
        'You should add a check for `isinstance`'
    assert IDX_LINE_WITH_constructor is not None \
           and IDX_LINE_WITH_constructor < IDX_LINE_WITH_isinstance,\
        'You should construct the `reminder` before checking `isinstance()`'

@pytest.mark.task_6_polite_reminder_touchup
def test_registration_polite_reminder():
    assert hasattr(PoliteReminder, '__iter__'),\
        'You should add `__iter__` on PoliteReminder'

    init_params = inspect.signature(PoliteReminder.__init__).parameters
    assert init_params.keys() == {'self', 'text', 'date'},\
        'In the last task PoliteReminder init should also take `date` parameter'

    assert init_params['date'].default is None,\
        'The `date` parameter of PoliteReminder.__init__ should be `None`'

    pr = PoliteReminder('test', '1/1/2020')
    polite_reminder_iter = list(pr.__iter__())
    assert polite_reminder_iter[0] == pr.text,\
        '`PoliteReminder.__iter__()` should return the `text` as first element'

    assert len(polite_reminder_iter) == 1,\
        '`PoliteReminder.__iter__()` should return only one item in the list'


@pytest.mark.task_6_registration
def test_registration_works():
    assert hasattr(app, 'PoliteReminder'),\
        'You should import `PoliteReminder` in `app.py`'

    assert hasattr(app, 'DeadlinedReminder'),\
        'You should import `DeadlinedReminder` in `app.py`'

    assert issubclass(PoliteReminder, DeadlinedReminder),\
        'You should register `PoliteReminder` with `DeadlinedReminder`'
