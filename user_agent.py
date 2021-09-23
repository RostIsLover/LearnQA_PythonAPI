import pytest
import requests
from jsonschema import validate

class TestUserAgent:

    linuxUA = "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    iPad1UA = "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"
    googleBotUA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    windowsUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"
    iPad2UA = "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

    user_agents = [
        (linuxUA),
        (iPad1UA),
        (googleBotUA),
        (windowsUA),
        (iPad2UA)
    ]

    user_agents_dict = {
        linuxUA: {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
        iPad1UA: {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
        googleBotUA: {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
        windowsUA: {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
        iPad2UA: {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
    }

    headers = {"User-Agent": ""}

    schema = {
        "type": "object",
        "properties": {
            "user_agent": {"type": "string"},
            "platform": {"type": "string"},
            "browser": {"type": "string"},
            "device": {"type": "string"},
        },
        "required": ["user_agent", "platform", "browser", "device"]
    }

    @pytest.mark.parametrize('user_agent', user_agents)
    def test_user_agent(self, user_agent):
        # Адрес запроса
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        # Формирование хедеров для запроса
        self.headers.update({"User-Agent": user_agent})

        # Запрос
        response = requests.get(url, headers=self.headers)

        # Проверка схемы
        validate(instance=response.json(), schema=self.schema)

        # Проверки ожидаемых полей
        assert self.user_agents_dict[user_agent]['platform'] == response.json()['platform'], f"platform doesn't match. UA"
        assert self.user_agents_dict[user_agent]['browser'] == response.json()['browser'], f"browser doesn't match. UA"
        assert self.user_agents_dict[user_agent]['device'] == response.json()['device'], f"device doesn't match"