import pytest
import inspect
import re

from abc import ABCMeta, ABC
from collections.abc import Iterable
from dateutil.parser import parse

from src import app
from src import database
from src import reminder
try:
    from src import deadlined_reminders as dr
    DEADLINED_REMINDERS_IMPORTED = True
except ImportError:
    DEADLINED_REMINDERS_IMPORTED = False

from src.external_reminders import EveningReminder

# This is for generality of task of implementation the concrete class
CONCRETE_CLASS_NAME = 'DateReminder'

class DummyReminder:
    def __init__(self, *args, **kwargs):
        pass

@pytest.mark.task_one_regular_class_exists
def test_task_one_class_exists():
    assert hasattr(reminder, 'PoliteReminder'), \
        'You should implement class `PoliteReminder` in reminder.py'
    assert inspect.isclass(reminder.PoliteReminder), \
        '`PoliteReminder` is not a class'
    assert issubclass(reminder.PoliteReminder, reminder.PrefixedReminder), \
        '`PoliteReminder` should inherit from `PrefixedReminder`'

@pytest.mark.task_one_regular_class_implementation
def test_task_one_regular_class_implementation():
    polite_reminder = reminder.PoliteReminder('test_string')
    assert hasattr(polite_reminder, 'prefix'), \
        'No `prefix` property on `PoliteReminder`. Did you inherit from `PrefixedReminder`?'
    assert 'please' in polite_reminder.prefix.lower(),\
        '`PoliteReminder` should initiate its parent [super()] with a polite prefix containing "please"'

@pytest.mark.task_two_overriding_text
def test_task_one_overriding_text():
    polite_reminder = reminder.PoliteReminder('test_string')
    assert polite_reminder.text != polite_reminder.prefix + '<placeholder_text>',\
        'You should override the `text` property with the concatenation'
    assert polite_reminder.text == polite_reminder.prefix + 'test_string',\
        '`PoliteReminder` should prefix the passed string with your prefix'


@pytest.mark.task_two_module_exists
def test_task_two_module_exists():
    assert DEADLINED_REMINDERS_IMPORTED, \
        'Could not find module `deadlined_reminders`. Check the name is correct...'


@pytest.mark.task_two_classes_exist_abstract
@pytest.mark.parametrize('class_name', [
    'DeadlinedMetaReminder',
    'DeadlinedReminder'
])
def test_task_two_classes_exist_abstract(class_name):
    assert hasattr(dr, class_name), \
        f'Could not find class `{class_name}` in `deadlined_reminders.py`'

    cls = getattr(dr, class_name)
    assert inspect.isclass(cls), f'`{class_name}` is not a class'

    assert type(cls) == ABCMeta, f'{class_name} should be an Abstract Base Class'
    if class_name == 'DeadlinedReminder':
        assert ABC in cls.__mro__, 'Class `DeadlinedReminder` should inherit from `ABC`'

@pytest.mark.task_two_methods_exist_abstract
@pytest.mark.parametrize('class_name, method_name', [
    ('DeadlinedMetaReminder', '__iter__'),
    ('DeadlinedMetaReminder', 'is_due'),
    ('DeadlinedReminder', '__iter__'),
    ('DeadlinedReminder', 'is_due')
])
def test_task_two_methods_exist_abstract(class_name, method_name):
    cls = getattr(dr, class_name)
    assert hasattr(cls, method_name), f'Could not find `{method_name}` in `{class_name}`'
    assert method_name in cls.__abstractmethods__,\
        f'Method {method_name} is not abstract in class {class_name}'


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
    database.add_reminder('test_reminder', '1/1/2020', dr.DateReminder)

@pytest.mark.task_4_add_reminder_incorrect
def test_app_opening_add_reminder_incorrect():
    # NOTE: pytest.raises(TypeError) does not work here as we want custom message
    #       for the other exceptions, which would bubble up otherwise
    error_message = 'You should only allow conforming classes in `add_reminder`.'\
                    ' Did you forget `issubclass()`?'
    try:
        database.add_reminder('test_reminder', '1/1/2020', DummyReminder)
        pytest.fail(error_message)
    except TypeError as e:
        assert str(e) == 'Invalid Reminder Class', error_message
    except Exception:
        pytest.fail(error_message)


@pytest.mark.task_4_subclasshook
def test_app_opening_subclasshook():
    DeadlinedReminder = dr.DeadlinedReminder
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
    PoliteReminder = reminder.PoliteReminder
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

    assert issubclass(reminder.PoliteReminder, dr.DeadlinedReminder),\
        'You should register `PoliteReminder` with `DeadlinedReminder`'
