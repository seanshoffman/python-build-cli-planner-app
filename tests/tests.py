import pytest
import inspect
import re
import random

from abc import ABCMeta, ABC
from collections.abc import Iterable
from dateutil.parser import parse
from datetime import datetime, timedelta

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

# === TASK 1 ========================================================================

@pytest.mark.task_1_regular_class_exists
def test_task_1_regular_class_exists():
    assert hasattr(reminder, 'PoliteReminder'), \
        'You should implement class `PoliteReminder` in reminder.py'
    assert inspect.isclass(reminder.PoliteReminder), \
        '`PoliteReminder` is not a class'
    assert issubclass(reminder.PoliteReminder, reminder.PrefixedReminder), \
        '`PoliteReminder` should inherit from `PrefixedReminder`'

@pytest.mark.task_1_regular_class_implementation
def test_task_1_regular_class_implementation():
    polite_reminder = reminder.PoliteReminder('test_string')
    assert hasattr(polite_reminder, 'prefix'), \
        'No `prefix` property on `PoliteReminder`. Did you inherit from `PrefixedReminder`?'
    assert 'please' in polite_reminder.prefix.lower(),\
        '`PoliteReminder` should initiate its parent [super()] with a polite prefix containing "please"'

# === TASK 2 ========================================================================

@pytest.mark.task_2_overriding_text
def test_task_2_overriding_text():
    polite_reminder = reminder.PoliteReminder('test_string')
    assert polite_reminder.text != polite_reminder.prefix + '<placeholder_text>',\
        'You should override the `text` property with the concatenation'
    assert polite_reminder.text == polite_reminder.prefix + 'test_string',\
        '`PoliteReminder` should prefix the passed string with your prefix'

# === TASK 3-4 ======================================================================

@pytest.mark.task_3
@pytest.mark.task_4
def test_deadlined_module_exists():
    assert DEADLINED_REMINDERS_IMPORTED, \
        'Could not find module `deadlined_reminders`. Check the name is correct...'


@pytest.mark.abstract_classes_exist
@pytest.mark.parametrize('class_name', [
    pytest.param('DeadlinedMetaReminder', marks=pytest.mark.task_3),
    pytest.param('DeadlinedReminder'    , marks=pytest.mark.task_4)
])
def test_abstract_classes_exist(class_name):
    assert hasattr(dr, class_name), \
        f'Could not find class `{class_name}` in `deadlined_reminders.py`'

    cls = getattr(dr, class_name)
    assert inspect.isclass(cls), f'`{class_name}` is not a class'

    assert inspect.isabstract(cls), f'{class_name} should be abstract'
    assert type(cls) == ABCMeta, f'{class_name} should be an Abstract Base Class'
    assert issubclass(cls, Iterable), f'{class_name} should inherit from `collections.abc.Iterable`'

    if class_name == 'DeadlinedReminder':
        assert ABC in cls.__mro__, 'Class `DeadlinedReminder` should inherit from `ABC`'


@pytest.mark.abstract_isdue_exists
@pytest.mark.parametrize('class_name', [
    pytest.param('DeadlinedMetaReminder', marks=pytest.mark.task_3),
    pytest.param('DeadlinedReminder'    , marks=pytest.mark.task_4)
])
def test_abstract_isdue_exists(class_name, method_name='is_due'):
    cls = getattr(dr, class_name)
    assert hasattr(cls, method_name), f'Could not find `{method_name}` in `{class_name}`'
    assert method_name in cls.__abstractmethods__,\
        f'Method {method_name} is not abstract in class {class_name}'

    params = inspect.signature(cls.is_due).parameters
    assert 'self' in params, f'`{method_name}()` should be a method. Did you forget `self`?'


# === TASK 5 & 6 & 7 ================================================================

@pytest.mark.task_5_concrete_subclass_stub
def test_task_5_concrete_subclass_stub():
    assert hasattr(dr, CONCRETE_CLASS_NAME), \
        f'Could not find class `{CONCRETE_CLASS_NAME}` in `deadlined_reminders.py`'

    cls = getattr(dr, CONCRETE_CLASS_NAME)
    assert inspect.isclass(cls), f'`{CONCRETE_CLASS_NAME}` is not a class'

    assert issubclass(cls, dr.DeadlinedReminder), \
        f'{CONCRETE_CLASS_NAME} should subclass `DeadlinedReminder`'

    implemented_fcts = inspect.getmembers(cls, inspect.isfunction)
    implemented_fct_names = [name for name, fct in implemented_fcts]
    assert '__init__' in implemented_fct_names,\
        f'You should implement `__init__` on {CONCRETE_CLASS_NAME}'

    init_params = inspect.signature(cls.__init__).parameters
    assert 'text' in init_params,\
        f'`{CONCRETE_CLASS_NAME}.__init__()` should receive `text` as a parameter'
    assert 'date' in init_params,\
        f'`{CONCRETE_CLASS_NAME}.__init__()` should receive `date` as a parameter'

    class DateReminder(cls):
        def __iter__(self): pass
        def is_due(self): pass

    reminder = DateReminder('test_string', '01/01/2020')
    assert reminder.text == 'test_string',\
        f'Incorrect text set in {CONCRETE_CLASS_NAME}.__init__()'
    assert reminder.date == parse('01/01/2020'),\
        f'Incorrect date set in {CONCRETE_CLASS_NAME}.__init__(). Did you `parse()` it?'


@pytest.mark.task_6_is_due
def test_task_6_is_due():
    method_name = 'is_due'

    cls = getattr(dr, CONCRETE_CLASS_NAME)
    assert method_name not in cls.__abstractmethods__,\
        f'You should implement `{method_name}()` on {CONCRETE_CLASS_NAME}'

    class DateReminder(cls):
        def __iter__(self): pass

    offset = random.randint(2, 100)

    date = datetime.now().date() + timedelta(days=offset)
    reminder = DateReminder('test_string', f'{date:%d/%m/%Y}')
    method = getattr(reminder, method_name)
    assert inspect.ismethod(method),\
        f'`{method_name}()` is not a method on {CONCRETE_CLASS_NAME}. Did you forget `self` ?'

    passed_date = datetime.now().date() - timedelta(days=offset)
    passed_reminder = DateReminder('test_string', f'{passed_date:%d/%m/%Y}')
    assert passed_reminder.is_due() is True,\
        f'`{CONCRETE_CLASS_NAME}.is_due()` should return True for a past date'

    future_date = datetime.now().date() + timedelta(days=offset)
    future_reminder = DateReminder('test_string', f'{future_date:%d/%m/%Y}')
    assert future_reminder.is_due() is False,\
        f'`{CONCRETE_CLASS_NAME}.is_due()` should return False for a future date ({future_date:%d/%m/%Y})'


@pytest.mark.task_7_iter
def test_task_7_iter():
    method_name = '__iter__'

    cls = getattr(dr, CONCRETE_CLASS_NAME)
    assert method_name not in cls.__abstractmethods__,\
        f'You should implement `{method_name}()` on {CONCRETE_CLASS_NAME}'

    # at this point we no longer need to mock it, we should be able to instantiate directly
    assert not cls.__abstractmethods__,\
        f'{CONCRETE_CLASS_NAME} should implement all virtual methods'
    DateReminder = cls

    offset = random.randint(2, 100)
    date = datetime.now().date() + timedelta(days=offset)
    date_str = f'{date:%d/%m/%Y}'
    formatted_date = date.strftime("%m/%d/%YT%H:%M:%SZ")

    reminder = DateReminder('test_string', date_str)
    method = getattr(reminder, method_name)
    assert inspect.ismethod(method),\
        f'`{method_name}()` is not a method on {CONCRETE_CLASS_NAME}. Did you forget `self` ?'

    serialized_reminder = list(reminder)
    assert len(serialized_reminder) == 2,\
        f'{CONCRETE_CLASS_NAME} should be serialized into an iterable of 2 elements'

    assert serialized_reminder[0] == 'test_string',\
        f'First element of your serialized {CONCRETE_CLASS_NAME} should be its `text`.'

    assert serialized_reminder[1] == formatted_date,\
        f'Second element of your serialized {CONCRETE_CLASS_NAME} should be _formatted_ date.'



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
