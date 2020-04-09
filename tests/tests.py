import pytest
from regular_reminder import RegularReminder

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