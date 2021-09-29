import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        expected_value = "hw_value"
        expected_name = "HomeWork"

        response = requests.get(url)

        response_cookies = dict(response.cookies)
        print(response_cookies)

        assert expected_name in response_cookies, f"Cookie {expected_name} is not in the response"
        assert response_cookies.get(expected_name) == expected_value, f"Cookie Value is not equal to given one"


