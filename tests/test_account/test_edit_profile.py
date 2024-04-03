import pytest
from django.contrib.auth import get_user_model

from tests.utils import create_user

User = get_user_model()


@pytest.mark.django_db
def test_edit_profile_success(client):
    user_data = {"username": "michael", "password": "stringpassword"}
    user = create_user(**user_data)
    client.login(username=user_data["username"], password=user_data["password"])

    url = "/account/edit/"
    data = {
        "username": "nike",
        "first_name": "Nike",
        "email": "nike@gmail.com",
        "date_of_birth": "2006-04-19",
    }
    response = client.post(url, data=data)

    updated_user = User.objects.get(id=user.id)
    profile = updated_user.profile

    assert response.status_code == 200
    assert updated_user.username == data["username"]
    assert updated_user.first_name == data["first_name"]
    assert updated_user.email == data["email"]
    assert profile.date_of_birth.strftime("%Y-%m-%d") == data["date_of_birth"]


@pytest.mark.django_db
def test_edit_profile_fail_redirection(client):
    url = "/account/edit/"
    data = {
        "username": "nike",
        "first_name": "Nike",
        "email": "nike@gmail.com",
        "date_of_birth": "2006-04-19",
    }
    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile_fail_validation_error(client):
    user_data = {"username": "michael", "password": "stringpassword"}
    create_user(**user_data)
    client.login(username=user_data["username"], password=user_data["password"])
    url = "/account/edit/"
    data = {
        "username": "nike",
        "first_name": "Nike",
        "email": "nike",
        "date_of_birth": "2006-04-19",
    }

    response = client.post(url, data=data)
    error = list(response.context["user_form"].errors.values())[0][0]

    assert response.status_code == 200
    assert error == "Enter a valid email address."


@pytest.mark.django_db
def test_edit_profile_fail_unique_error(client):
    user_data = {"username": "michael", "password": "stringpassword"}
    user_data_2 = {"username": "nike", "password": "stringpassword"}
    create_user(**user_data)
    create_user(**user_data_2)
    client.login(username=user_data["username"], password=user_data["password"])
    url = "/account/edit/"
    data = {
        "username": "nike",
        "first_name": "Nike",
        "email": "nike@gmail.com",
        "date_of_birth": "2006-04-19",
    }

    response = client.post(url, data=data)
    error = list(response.context["user_form"].errors.values())[0][0]

    assert response.status_code == 200
    assert error == "A user with that username already exists."
