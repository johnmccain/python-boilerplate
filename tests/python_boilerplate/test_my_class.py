import pytest

from python_boilerplate.models.app_config import AppConfig
from python_boilerplate.my_class import MyClass


def test_my_method_returns_int():
    my_class = MyClass()
    assert isinstance(my_class.my_method(), int)


def test_my_method_returns_configured_value():
    app_config = AppConfig(my_class_value=2)
    my_class = MyClass(app_config=app_config)
    assert my_class.my_method() == 2
