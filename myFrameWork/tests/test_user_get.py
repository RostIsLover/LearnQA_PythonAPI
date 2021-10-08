import allure
from myFrameWork.lib.base_case import BaseCase
from myFrameWork.lib.assertions import Assertions
from datetime import datetime

from myFrameWork.lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    @allure.description("This test checks get user details no auth")
    @allure.feature("Negative test cases")
    @allure.issue("qweqwewqe1")
    @allure.severity("CRITICAL")
    @allure.story("Security")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test checks get user details as same user")
    @allure.feature("Positive test cases")
    @allure.issue("123easease")
    @allure.severity("CRITICAL")
    @allure.story("User story")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    # Ex16: Запрос данных другого пользователя
    @allure.description("This test checks get user details as another user")
    @allure.feature("Negative test cases")
    @allure.issue("12321323")
    @allure.severity("CRITICAL")
    @allure.story("Security")
    def test_get_user_by_another_user(self):
        data = {
            'password': f'123456{datetime.now().strftime("%m%d%Y%H%S")}',
            'username': f'username{datetime.now().strftime("%m%d%Y%H%S")}',
            'firstName': f'name{datetime.now().strftime("%m%d%Y%H%S")}',
            'lastName': f'lastName{datetime.now().strftime("%m%d%Y%H%S")}',
            'email': f"{datetime.now().strftime('%m%d%Y%H%S')}@example.com"
        }

        response_create_user = MyRequests.post("/user", data=data)

        response_login = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_login, "user_id")

        response_get = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response_get, "username")
        Assertions.assert_json_has_not_key(response_get, "email")
        Assertions.assert_json_has_not_key(response_get, "firstName")
        Assertions.assert_json_has_not_key(response_get, "lastName")





