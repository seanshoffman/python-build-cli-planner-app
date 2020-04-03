import pytest
from src.regular_reminder import RegularReminder

@pytest.mark.task_one_regular_class
class TestApp():
    def test_task_one_regular_class(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularReminder()
            assert regular.__str__(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented'"

