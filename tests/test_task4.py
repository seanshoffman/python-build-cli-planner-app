import pytest
import inspect

import database
from deadlined_reminders import DateReminder
from external_reminders import EveningReminder

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
    class DummyReminder:
        def __init__(self, *args, **kwargs):
            pass

    # NOTE: pytest.raises(TypeError) does not work here as we want custom message
    #       for the other exceptions, which would bubble up otherwise
    try:
        database.add_reminder('test_reminder', '1/1/2020', DummyReminder)
    except TypeError as e:
        pass
    except Exception:
        pytest.fail('You should only allow conforming classes in `add_reminder`.'
                    ' Did you forget `issubclass()`?')


@pytest.mark.task_4_add_reminder_datetime
def test_app_opening_add_reminder_datetime():
    database.add_reminder('test_reminder', '1/1/2020', EveningReminder)
