from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

class UserActions(BaseCase):
    def register_user(self, register_data: dict) -> dict:

        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")
        username = register_data['username']
        email = register_data['email']
        first_name = register_data['firstName']
        last_name = register_data['lastName']
        password = register_data['password']

        return {
            "id": user_id,
            'username': username,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'password': password
        }

    def login_and_check_user_data(self, user_params: dict):
        # LOGIN AS USER1

        data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        with allure.step(f"Login as User1 by email '{data['email']}' and password '{data['password']}'"):
            response_user_login = MyRequests.post("/user/login", data=data)
            auth_sid_user = self.get_cookie(response_user_login, "auth_sid")
            token_user = self.get_header(response_user_login, "x-csrf-token")

        # GET
        with allure.step(f"'Get User1 details (ID = '{user_params['id']}') by authorized User2'"):
            response_user_getdata = MyRequests.get(f"/user/{user_params['id']}",
                                                   headers={"x-csrf-token": token_user},
                                                   cookies={"auth_sid": auth_sid_user},
                                                   )

            Assertions.assert_json_value_by_name(
                response_user_getdata,
                "firstName", user_params['firstName'],
                "Wrong firstName of user after edit"
            )
            Assertions.assert_json_value_by_name(
                response_user_getdata,
                "lastName", user_params['lastName'],
                "Wrong lastName of user after edit"
            )
            Assertions.assert_json_value_by_name(
                response_user_getdata,
                "username", user_params['username'],
                "Wrong username of user after edit"
            )
            Assertions.assert_json_value_by_name(
                response_user_getdata,
                "email", user_params['email'],
                "Wrong username of user after edit")

    def login_and_delete(self, user1_params: dict, user2_params: dict):
        # LOGIN USER1
        login_data_user1 = {
            'email': user1_params['email'],
            'password': user1_params['password']
        }
        with allure.step(f"Login as User1 by email '{login_data_user1['email']}' "
                         f"and password '{login_data_user1['password']}'"):
            response_login_user1 = MyRequests.post("/user/login", data=login_data_user1)
            auth_sid = self.get_cookie(response_login_user1, "auth_sid")
            token = self.get_header(response_login_user1, "x-csrf-token")

        # DELETE USER2
        with allure.step(f"Delete user '{user2_params['username']}'"):
            response_delete_user2 = MyRequests.delete(
                f"/user/{user2_params['id']}",
                data=login_data_user1,
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response_delete_user2, 200)
            return {
                "x-csrf-token": token,
                "auth_sid": auth_sid
            }
