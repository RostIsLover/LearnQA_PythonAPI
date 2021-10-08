import allure
from myFrameWork.lib.base_case import BaseCase
from myFrameWork.lib.assertions import Assertions
from myFrameWork.lib.my_requests import MyRequests

@allure.epic("Delete cases")
class TestUserDelete(BaseCase):

    @allure.description("This test checks removal")
    @allure.feature("Positive test cases")
    @allure.issue("3212323")
    @allure.severity("MEDIUM")
    @allure.story("Security")
    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE {user_id}
        response_delete = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # GET USER {user_id}
        response_get = MyRequests.get(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_value_by_name(response_get, "id", "2", "id 2 doesn't exist apparently")

    @allure.description("This test checks removal user as same user")
    @allure.feature("Positive test cases")
    @allure.issue("12312321")
    @allure.severity("CRITICAL")
    @allure.story("User story")
    def test_delete_user_as_same_user(self):
        # REGISTER NEW USER
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_register, "id")

        # LOGIN
        login_data = {
            'email': email,
            "password": password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")


        # DELETE {user_id}
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        # GET USER {user_id}
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        assert response_get.text == f"User not found", "User still exists"
        Assertions.assert_code_status(response_get, 404)

    @allure.description("This test checks removal user as another user")
    @allure.feature("Negative test cases")
    @allure.issue("32442")
    @allure.severity("CRITICAL")
    @allure.story("Security")
    def test_delete_user_as_another_user(self):
        # REGISTER NEW USER 1
        register_data_user1 = self.prepare_registration_data()
        response_register_user1 = MyRequests.post("/user/", data=register_data_user1)

        email = register_data_user1['email']
        password = register_data_user1['password']

        # REGISTER NEW USER 2
        register_data_user2 = self.prepare_registration_data()
        response_register_user2 = MyRequests.post("/user/", data=register_data_user2)

        user_id = self.get_json_value(response_register_user2, "id")

        # LOGIN by user 1
        login_data = {
            'email': email,
            "password": password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE user_2 by user_1
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        # GET USER 2 {user_id}
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response_get, "username")
        Assertions.assert_code_status(response_get, 200)

