import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


@pytest.mark.django_db
def test_user_register_success(client):
    url = "/account/register/"
    data = {
        "username": "simpleuser",
        "first_name": "Simple",
        "email": "simple@user.ru",
        "password": "simplepassword",
        "password2": "simplepassword",
    }
    response = client.post(
        url,
        data=data,
    )
    user = User.objects.get(username=data["username"])

    assert response.status_code == 200
    assert user.first_name == data["first_name"]
    assert user.email == data["email"]
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_user_register_fail_validation_error(client):
    url = "/account/register/"
    data = {
        "username": "simpleuser",
        "first_name": "Simple",
        "email": "simple@user.ru",
        "password": "simplepassword",
        "password2": "wrongpassword",
    }
    response = client.post(
        url,
        data=data,
    )

    error_list = list(response.context["user_form"].errors.values())

    assert response.status_code == 400
    assert error_list[0][0] == "Passwords don't match."


@pytest.mark.django_db
def test_user_register_fail_unique_error(client):
    url = "/account/register/"
    data = {
        "username": "simpleuser",
        "first_name": "Simple",
        "email": "simple@user.ru",
        "password": "simplepassword",
        "password2": "simplepassword",
    }
    User.objects.create_user(
        username=data["username"],
        first_name=data["first_name"],
        email=data["email"],
        password=data["password"],
    )
    response = client.post(
        url,
        data=data,
    )

    error_list = list(response.context["user_form"].errors.values())

    assert response.status_code == 400
    assert error_list[0][0] == "A user with that username already exists."
