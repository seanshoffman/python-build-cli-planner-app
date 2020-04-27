import pytest
from regular_reminder import RegularReminder
from abc_meta_reminder import ABCMetaReminder
from abc_reminder import ABCReminder
from basic_reminder import BasicReminder
from date_reminder import DateReminder
from datetime import datetime
from database import add_reminder

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

    @pytest.mark.task_five_date_reminder_class_1
    def test_task_five_date_reminder_class_1(self):
        date = DateReminder("Buy 6 eggs", "2020-01-31 15:00:00")
        assert date.is_due() == True, "The is_due method was not implemented correctly to compare the date property against the current time"
        assert date.reminder == "Buy 6 eggs", "DateReminder is not taking a reminder constructor parameter and setting the class property 'reminder'"
        assert date.date == datetime(2020, 1, 31, 15, 0), "DateReminder is not taking a date constructor parameter and setting the class property `parse(date)`"

    @pytest.mark.task_six_issubclass_1
    def test_task_six_issubclass_1(self):
        class FakeReminder():
            def __iter__(self):
                pass

            def is_due(self):
                pass

        assert issubclass(FakeReminder, ABCReminder), "__subclasshook__ is not checking for the presence of __iter__ and is_due methods"

    def test_task_six_isinstance_1(self):
        class FakeReminder():
            def __iter__(self):
                pass

            def is_due(self):
                pass

        fake = FakeReminder()

        assert isinstance(fake, ABCReminder), "__subclasshook__ is not checking for the presence of __iter__ and is_due methods"