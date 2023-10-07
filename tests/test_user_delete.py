from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from lib.user_actions import UserActions


class TestUserDelete(BaseCase):
    @allure.description("Test checks that user with id=2 can't be deleted when authorized")
    def test_delete_user_id_2(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response_delete = MyRequests.delete(
            "/user/2",
            data=data,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 400)
        assert response_delete.content.decode("UTF-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    @allure.description("Test checks positive delete scenario")
    def test_delete_user_successfully(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        user_params = user.register_user(register_data)

        # LOGIN AS USER AND DELETE USER
        data = user.login_and_delete(user_params, user_params)
        token = data.get('x-csrf-token')
        auth_sid = data.get('auth_sid')

        # GET USER
        response_get = MyRequests.get(f"/user/{user_params['id']}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )
        assert response_get.content.decode("UTF-8") == "User not found"

    @allure.description("Delete user by another authorized one")
    def test_delete_user_by_another_authorized_user(self):
        user1 = UserActions()
        user2 = UserActions()

        # REGISTER USER1
        register_data_user1 = self.prepare_registration_data()
        register_data_user1['username'] = "username_user1"
        user1_params = user1.register_user(register_data_user1)

        # REGISTER USER2
        register_data_user2 = self.prepare_registration_data()
        register_data_user2['username'] = "username_user2"
        user2_params = user2.register_user(register_data_user2)

        # LOGIN AS USER1 AND DELETE USER2
        data = user1.login_and_delete(user1_params, user2_params)
        token = data.get('x-csrf-token')
        auth_sid = data.get('auth_sid')

        # GET USER2
        response_get_user2 = MyRequests.get(f"/user/{user2_params['id']}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid},
                                            )

        Assertions.assert_code_status(response_get_user2, 200)
        Assertions.assert_json_value_by_name(
            response_get_user2,
            'username',
            user2_params['username'],
            "User was illegally deleted by another authorized user")
