import requests

class TestHeader:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        expected_value = "Some secret value"
        expected_name = "x-secret-homework-header"

        response = requests.get(url)
        print(response.headers)

        assert expected_name in response.headers, f"Header {expected_name} is not in the response"
        assert response.headers.get(expected_name) == expected_value, f"Header Value {expected_value} is not equal to given one"