import requests


class TestIdentifyCookie:
    def test_identify_cookies(self):
        response = requests.post("https://playground.learnqa.ru/api/homework_cookie")

        cookies_list = response.cookies.keys()

        for cookie_item in cookies_list:
            cookie_name = cookie_item
            print("cookie_name: ", cookie_name)

            cookie_value = response.cookies[cookie_name]
            print("cookie_value: ", cookie_value)

            cookie = {cookie_name: cookie_value}

            assert cookie == {"HomeWork": "hw_value"}, (f"Cannot find cookie with name '{cookie_name}' and value"
                                                        f" '{cookie_value}' in response")








