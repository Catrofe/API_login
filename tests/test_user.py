from app.models import UserRegister
from app.user import verify_email_already_exists

register = UserRegister(
    email="christian@outlook.com", name="christian", password="passworD1"
)


def test_verify_email_should_false():
    assert not verify_email_already_exists(register.email)
