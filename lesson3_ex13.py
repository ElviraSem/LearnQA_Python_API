import json.decoder

import requests
import pytest
from requests import Response


class TestUserAgentCheck:

    user_agents = [
        (
            'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 '
            '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mobile', 'No', 'Android'
        ),
        (
            'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'Mobile', 'Chrome', 'iOS'
        ),
        (
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Googlebot', 'Unknown', 'Unknown'
        ),
        (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 '
            'Safari/537.36 Edg/91.0.100.0',
            'Web', 'Chrome', 'No'
        ),
        (
            'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Mobile', 'No', 'iPhone'
        )
    ]

    def get_json_value(self, response: Response, name: str):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response has not '{name}' key"
        return response_as_dict[name]

    @pytest.mark.parametrize('user_agent, expected_platform, expected_browser, expected_device', user_agents)
    def test_user_agent_check(self, user_agent, expected_platform, expected_browser, expected_device):
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )

        actual_platform_in_response = self.get_json_value(response, 'platform')
        actual_browser_in_response = self.get_json_value(response, 'browser')
        actual_device_in_response = self.get_json_value(response, 'device')

        assert actual_platform_in_response == expected_platform, (f"There is an incorrect 'platform' field value in "
                                                                  f"User-Agent '{user_agent}'")
        assert actual_browser_in_response == expected_browser, (f"There is an incorrect 'browser' field value in "
                                                                f"User-Agent '{user_agent}'")
        assert actual_device_in_response == expected_device, (f"There is an incorrect 'device' field value in "
                                                              f"User-Agent '{user_agent}'")
