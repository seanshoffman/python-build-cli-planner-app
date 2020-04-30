import pytest
import inspect

from abc import ABCMeta, ABC
from collections.abc import Iterable

try:
    import deadlined_reminders as dr
    IMPORT_SUCCEDED = True
except ImportError:
    IMPORT_SUCCEDED = False

@pytest.mark.task_two_module_exists
def test_task_two_module_exists():
    assert IMPORT_SUCCEDED, \
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
