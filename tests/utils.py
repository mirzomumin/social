from django.contrib.auth import get_user_model

from account.models import Profile

User = get_user_model()


def create_user(
    username: str, password: str, email: str = "", first_name: str = ""
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
    )
    Profile.objects.create(user=user)
    return user
