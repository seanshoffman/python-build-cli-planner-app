import pytest
from regular_reminder import RegularReminder
from abc_meta_reminder import ABCMetaReminder
from abc_reminder import ABCReminder
from basic_reminder import BasicReminder

class TestApp():
    @pytest.mark.task_one_regular_class_1
    def test_task_one_regular_class_1(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.__iter__(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented' for method __iter__"

    @pytest.mark.task_one_regular_class_2
    def test_task_one_regular_class_2(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.is_due(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented' for method is_due"

    @pytest.mark.task_two_abc_meta_class_1
    def test_task_two_abc_meta_class_1(self):
        ABCMetaReminder.register(tuple)
        assert issubclass(tuple, ABCMetaReminder)
        assert isinstance((), ABCMetaReminder)

    @pytest.mark.task_two_abc_meta_class_2
    def test_task_two_abc_meta_class_2(self):
        with pytest.raises(TypeError) as e:
            abc_meta = ABCMetaReminder()
            assert str(e.value) == "Can't instantiate abstract class ABCMetaReminder with abstract methods __iter__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __iter__, is_due"

    @pytest.mark.task_three_abc_class_1
    def test_task_three_abc_class_1(self):
        ABCReminder.register(tuple)
        assert issubclass(tuple, ABCReminder)
        assert isinstance((), ABCReminder)

    @pytest.mark.task_three_abc_class_2
    def test_task_three_abc_class_2(self):
        with pytest.raises(TypeError) as e:
            abc = ABCReminder()
        assert str(e.value) == "Can't instantiate abstract class ABCReminder with abstract methods __iter__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __iter__, is_due"

    @pytest.mark.task_four_basic_reminder_class_1
    def test_task_four_basic_reminder_class_1(self):
        basic = BasicReminder("Buy 6 eggs")
        assert issubclass(BasicReminder, ABCReminder), "BasicReminder is not not a subclass of ABCReminder"
        assert isinstance(basic, ABCReminder), "BasicReminder is not not a subclass of ABCReminder"
        assert hasattr(basic, "reminder"), "BasicReminder is missing the property 'reminder'"
        assert basic.reminder == "Buy 6 eggs", "BasicReminder is not taking a single constructor parameter and setting the class property 'reminder'"
