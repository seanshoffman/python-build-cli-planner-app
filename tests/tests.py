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