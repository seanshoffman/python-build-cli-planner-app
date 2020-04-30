import pytest
import inspect

import app
import database
from deadlined_reminders import DateReminder, DeadlinedReminder
from external_reminders import EveningReminder

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
