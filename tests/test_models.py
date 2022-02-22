import pytest
from pydantic import ValidationError

from app.models import UserRegister


def should_return_true() -> None:
    # It should not raise an exception.
    UserRegister(email="test@test.com", name="test", password="Test1234")


def test_validate_password_without_upper_letter_should_return_false() -> None:
    with pytest.raises(ValidationError):
        UserRegister(email="test@test.com", name="test", password="test1234")


def test_validate_password_without_lower_letter_should_return_false() -> None:
    with pytest.raises(ValidationError):
        UserRegister(email="test@test.com", name="test", password="TEST1234")


def test_validate_password_without_number_should_return_false() -> None:
    with pytest.raises(ValidationError):
        UserRegister(email="test@test.com", name="test", password="TESTtest")
