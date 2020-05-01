import pytest
import inspect

import reminder

@pytest.mark.task_one_regular_class_exists
def test_task_one_exists():
    assert 'PoliteReminder' in dir(reminder), \
        'You should implement class `PoliteReminder` in reminder.py'
    assert inspect.isclass(reminder.PoliteReminder), \
        '`PoliteReminder` is not a class'
    assert issubclass(reminder.PoliteReminder, reminder.PrefixedReminder), \
        '`PoliteReminder` should inherit from `PrefixedReminder`'

@pytest.mark.task_one_regular_class_implementation
def test_task_one_implementation():
    polite_reminder = reminder.PoliteReminder('test_string')
    assert 'prefix' in dir(polite_reminder), \
        'No `prefix` property on `PoliteReminder`. Did you inherit from `PrefixedReminder`?'
    assert 'please' in polite_reminder.prefix.lower(),\
        '`PoliteReminder` should initiate its parent [super()] with a polite prefix containing "please"'
    if polite_reminder.text == polite_reminder.prefix + '<placeholder_text>':
        assert False, "Don't forget to fix your `PoliteReminder` after the intermediate test"
    else:
        assert polite_reminder.text == polite_reminder.prefix + 'test_string',\
            '`PoliteReminder` should prefix the passed string with your prefix'
