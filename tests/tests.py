import pytest
from src.regular_reminder import RegularReminder
from src.abc_meta_reminder import ABCMetaReminder

class TestApp():
    @pytest.mark.task_one_regular_class_1
    def test_task_one_regular_class_1(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.__str__(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented' for method __str__"
        
    @pytest.mark.task_one_regular_class_2
    def test_task_one_regular_class_2(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.__iter__(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented' for method __iter__"

    @pytest.mark.task_two_abc_meta_class_1
    def test_task_two_abc_meta_class_1(self):
        ABCMetaReminder.register(tuple)
        assert issubclass(tuple, ABCMetaReminder)
        assert isinstance((), ABCMetaReminder)

    @pytest.mark.task_two_abc_meta_class_2
    def test_task_two_abc_meta_class_2(self):
        with pytest.raises(TypeError) as e:
            abc_meta = ABCMetaReminder()
        assert str(e.value) == "Can't instantiate abstract class ABCMetaReminder with abstract methods __iter__, __str__", "The Abstract Base Class has not been correctly implemented with abstractmethods __iter__ and __str__"