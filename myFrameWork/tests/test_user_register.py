import pytest
import requests
from myFrameWork.lib.base_case import BaseCase
from myFrameWork.lib.assertions import Assertions
from datetime import datetime

class TestUserRegister(BaseCase):
    absent_params = [
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email"),
        ("password")
    ]

    def setup(self):
        self.base_part = 'learnqa'
        self.domain = 'example.com'
        self.random_part = datetime.now().strftime("%m%d%Y%H%S")
        self.email = f"{self.base_part}{self.random_part}@{self.domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_mail(self):
        incorrect_email = f"{self.base_part}{self.random_part}{self.domain}"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': incorrect_email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        print(response.content)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("absent_param", absent_params)
    def test_create_with_no_one_param(self, absent_param):

        if absent_param == "username":
            data = {
                'password': '123',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }

        elif absent_param == "firstName":
            data = {
                'password': '123',
                'username': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }
        elif absent_param == "password":
            data = {
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }
        elif absent_param == "lastName":
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'email': self.email
            }
        elif absent_param == "email":
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa'
            }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.text == f"The following required params are missed: {absent_param}"

    def test_create_user_with_short_name(self):
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short"

    def test_create_user_with_long_name(self):
        data = {
            'password': '123',
            'username': 'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long"

