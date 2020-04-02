import pytest
from src.regular_class import RegularClass

class TestApp():
    def test_task_one(self):
        with pytest.raises(NotImplementedError) as e:
            regular = RegularClass()
            assert regular.__str__(), "Failed to raise the correct error type"
        assert str(e.value) == "Method not implemented", "Error message does not match 'Method not implemented'"

