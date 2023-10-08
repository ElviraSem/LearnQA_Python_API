import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Login by user email: '{data['email']}' and password '{data['password']}'"):
            response1 = MyRequests.post("/user/login", data=data)

            self.auth_sid = self.get_cookie(response1, 'auth_sid')
            self.token = self.get_header(response1, "x-csrf-token")
            self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.feature("Positive authorization scenarios")
    @allure.story("Check that user is authorized")
    @allure.tag("GET request")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User is authorized after he is logged in")
    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):
        with allure.step(f"Get request and check that user is authorized"):
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                self.user_id_from_auth_method,
                "User id from auth method is not equal to user id from check method"
            )

    @allure.feature("Negative authorization scenarios")
    @allure.story("Check that user is not authorized without token or cookie")
    @allure.tag("GET request")
    @allure.title("Authorization status without sending auth cookie or token")
    @allure.description("This test checks authorization status without sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        with allure.step(f"Get request and check that user is not authorized"):
            if condition == 'no_cookie':
                response2 = MyRequests.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token}
                )
            else:
                response2 = MyRequests.get(
                    "/user/auth",
                    cookies={"auth_sid": self.auth_sid}
                )

            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                0,
                f"User is authorized with condition {condition}"
            )

