from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Get user details cases")
class TestUserGet(BaseCase):
    @allure.feature("Negative get user details scenarios")
    @allure.story("Get user details by unauthorized user")
    @allure.tag("GET request")
    @allure.title("Get user details by the same unauthorized user")
    @allure.description("Test checks that user with id=2 can't get its details when unauthorized")
    def test_get_user_details_not_auth(self):
        with allure.step('Send GET request for User details (ID = 2)'):
            response = MyRequests.get("/user/2")

            Assertions.assert_json_has_key(response, "username")
            Assertions.assert_json_has_not_key(response, "email")
            Assertions.assert_json_has_not_key(response, "firstName")
            Assertions.assert_json_has_not_key(response, "lastName")

    @allure.feature("Positive get user details scenarios")
    @allure.story("Basic scenario of Getting user details by him authorized")
    @allure.tag("GET request")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Getting user details by him authorized")
    @allure.description("Test checks that authorized user can get its details")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step(f"Login as user by email '{data['email']}' and password '{data['password']}'"):
            response1 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step(f'Send GET request for User details (ID = "{user_id_from_auth_method}")'):
            response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )
            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.feature("Negative get user details scenarios")
    @allure.story("Get user details by another authorized user")
    @allure.tag("GET request")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Get user details by another authorized user")
    @allure.description("This test checks what user's params can't be received by another authorized user")
    def test_user_details_auth_as_another_user(self):

        # REGISTER USER1
        data = self.prepare_registration_data()
        with allure.step(f"Register user '{data['username']}'"):
            response_user1 = MyRequests.post("/user/", data=data)
            user1_id = self.get_json_value(response_user1, "id")

        # LOGIN AS USER2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Login as User2 by email '{data['email']}' and password '{data['password']}'"):
            response_user2_login = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response_user2_login, "auth_sid")
            token = self.get_header(response_user2_login, "x-csrf-token")

        # GET USER1 DATA BY AUTHORIZED USER2
        with allure.step(f'Get User1 details (ID = "{user1_id}") by authorized User2'):
            response_user2_get_user1_data = MyRequests.get(f"/user/{user1_id}",
                                                           headers={"x-csrf-token": token},
                                                           cookies={"auth_sid": auth_sid}
                                                           )
            unexpected_fields = ["email", "firstName", "lastName"]

            Assertions.assert_json_has_key(response_user2_get_user1_data, "username")
            Assertions.assert_json_has_not_keys(response_user2_get_user1_data, unexpected_fields)
