from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks what user's params can't be received by another authorized user")
    def test_user_details_auth_as_another_user(self):

        # CREATE USER1
        data = self.prepare_registration_data()

        response_user1 = MyRequests.post("/user/", data=data)
        user1_id = self.get_json_value(response_user1, "id")

        # LOGIN AS USER2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_user2_login = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_user2_login, "auth_sid")
        token = self.get_header(response_user2_login, "x-csrf-token")

        # GET USER1 DATA BY AUTHORIZED USER2
        response_user2_get_user1_data = MyRequests.get(f"/user/{user1_id}",
                                                       headers={"x-csrf-token": token},
                                                       cookies={"auth_sid": auth_sid}
                                                       )
        unexpected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response_user2_get_user1_data, "username")
        Assertions.assert_json_has_not_keys(response_user2_get_user1_data, unexpected_fields)
