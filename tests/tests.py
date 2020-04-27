import pytest
from regular_reminder import RegularReminder

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