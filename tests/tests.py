import pytest
from regular_reminder import RegularReminder
from abc_meta_reminder import ABCMetaReminder
from abc_reminder import ABCReminder

class TestApp():
    @pytest.mark.task_one_regular_class_1
    def test_task_one_regular_class_1(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.__iter__(), "Failed to raise the correct error type"
        assert str(e.value) == "Abstract method '__iter__' should not be called", "Error message does not match \"Abstract method '__iter__' should not be called\" for method __iter__"

    @pytest.mark.task_one_regular_class_2
    def test_task_one_regular_class_2(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.is_due(), "Failed to raise the correct error type"
        assert str(e.value) == "Abstract method 'is_due' should not be called", "Error message does not match \"Abstract method 'is_due' should not be called\" for method is_due"

    @pytest.mark.task_two_abc_meta_class_1
    def test_task_two_abc_meta_class_1(self):
        ABCMetaReminder.register(tuple)
        assert issubclass(tuple, ABCMetaReminder)
        assert isinstance((), ABCMetaReminder)

    @pytest.mark.task_two_abc_meta_class_2
    def test_task_two_abc_meta_class_2(self):
        with pytest.raises(TypeError) as e:
            abc_meta = ABCMetaReminder()
            assert str(e.value) == "Can't instantiate abstract class ABCMetaReminder with abstract methods __str__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __str__, is_due"

    @pytest.mark.task_three_abc_class_1
    def test_task_three_abc_class_1(self):
        ABCReminder.register(tuple)
        assert issubclass(tuple, ABCReminder)
        assert isinstance((), ABCReminder)

    @pytest.mark.task_three_abc_class_2
    def test_task_three_abc_class_2(self):
        with pytest.raises(TypeError) as e:
            abc = ABCReminder()
        assert str(e.value) == "Can't instantiate abstract class ABCReminder with abstract methods __str__, is_due", "The Abstract Base Class has not been correctly implemented with abstractmethods __str__, is_due"