import requests
from myFrameWork.lib.base_case import BaseCase
from myFrameWork.lib.assertions import Assertions
from datetime import datetime

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    # Ex16: Запрос данных другого пользователя
    def test_get_user_by_another_user(self):
        data = {
            'password': f'123456{datetime.now().strftime("%m%d%Y%H%S")}',
            'username': f'username{datetime.now().strftime("%m%d%Y%H%S")}',
            'firstName': f'name{datetime.now().strftime("%m%d%Y%H%S")}',
            'lastName': f'lastName{datetime.now().strftime("%m%d%Y%H%S")}',
            'email': f"{datetime.now().strftime('%m%d%Y%H%S')}@example.com"
        }

        response_create_user = requests.post("https://playground.learnqa.ru/api/user", data=data)

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_login, "user_id")

        response_get = requests.get(
            "https://playground.learnqa.ru/api/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response_get, "username")
        Assertions.assert_json_has_not_key(response_get, "email")
        Assertions.assert_json_has_not_key(response_get, "firstName")
        Assertions.assert_json_has_not_key(response_get, "lastName")





