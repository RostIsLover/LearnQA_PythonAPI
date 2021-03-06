import allure
from myFrameWork.lib.base_case import BaseCase
from myFrameWork.lib.assertions import Assertions
from myFrameWork.lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    @allure.description("This test checks edit just created user")
    @allure.feature("Positive test cases")
    @allure.issue("424422")
    @allure.severity("CRITICAL")
    @allure.story("User story")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Ex17: Негативные тесты на PUT
    @allure.description("This test checks edit no auth")
    @allure.feature("Negative test cases")
    @allure.issue("242434")
    @allure.severity("CRITICAL")
    @allure.story("Security issue")
    def test_edit_no_auth(self):
        new_name = "Changed Name"

        response = MyRequests.put(
            "/user/2",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", "Incorrect response text from PUT-method"

    @allure.description("This test checks edit as another user")
    @allure.feature("Negative test cases")
    @allure.issue("3232323")
    @allure.severity("CRITICAL")
    @allure.story("Security issue")
    def test_edit_auth_as_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "username",
            "Vitaliy",
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks edit as same user with incorrect email")
    @allure.feature("Negative test cases")
    @allure.issue("3434322")
    @allure.severity("medium")
    @allure.story("User story")
    def test_edit_auth_as_same_user_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = self.getIncorrectEmail()

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.text == "Invalid email format", "Incorrect response text from edit with invalid email"

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "Wrong email of the user after edit"
        )

    @allure.description("This test checks edit as same user ")
    @allure.feature("Positive test cases")
    @allure.issue("092138912a")
    @allure.severity("CRITICAL")
    @allure.story("User story")
    def test_edit_username_auth_as_same_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_firstname = "a"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstname}
        )

        print(response3.text)
        Assertions.assert_code_status(response3, 400)

        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            "Wrong behave in editing firstname with one letter"
        )

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Wrong firstname of the user after edit"
        )


