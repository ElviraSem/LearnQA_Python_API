from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from lib.user_actions import UserActions


@allure.epic("Delete users feature cases")
class TestUserDelete(BaseCase):

    @allure.feature("Negative delete scenarios")
    @allure.story("Delete undeletable user")
    @allure.tag("DELETE request")
    @allure.title("Delete User (id=2) when he is authorized")
    @allure.description("Test checks that user with id=2 can't be deleted when authorized")
    def test_delete_user_id_2(self):
        # LOGIN
        with allure.step('Login as User with ID = 2'):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response_login = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        with (allure.step('Try to deleteUser with ID = 2')):
            response_delete = MyRequests.delete(
                "/user/2",
                data=data,
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response_delete, 400)
            assert response_delete.content.decode("UTF-8") == ("Please, do not delete test users with ID "
                                                               "1, 2, 3, 4 or 5.")

    @allure.feature("Positive delete scenarios")
    @allure.story("Basic user Delete scenario")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Delete an authorized user")
    @allure.tag("DELETE request")
    @allure.description("Test checks positive delete scenario")
    def test_delete_user_successfully(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Register user '{register_data['username']}'"):
            user_params = user.register_user(register_data)

        # LOGIN AS USER AND DELETE USER
        with allure.step(f"Login user '{register_data['username']}' and delete him"):
            data = user.login_and_delete(user_params, user_params)
            token = data.get('x-csrf-token')
            auth_sid = data.get('auth_sid')

        # GET USER
        with allure.step(f"Get userdata of user '{register_data['username']}' and check that user is deleted"):
            response_get = MyRequests.get(f"/user/{user_params['id']}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid},
                                          )
            assert response_get.content.decode("UTF-8") == "User not found"

    @allure.feature("Negative delete scenarios")
    @allure.story("Delete user by another one unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Delete user by another one unauthorized")
    @allure.tag("DELETE request")
    @allure.description("Delete user by another one authorized")
    def test_delete_user_by_another_authorized_user(self):
        user1 = UserActions()
        user2 = UserActions()

        # REGISTER USER1
        register_data_user1 = self.prepare_registration_data()
        register_data_user1['username'] = "username_user1"
        with allure.step(f"Register user '{register_data_user1['username']}'"):
            user1_params = user1.register_user(register_data_user1)

        # REGISTER USER2
        register_data_user2 = self.prepare_registration_data()
        register_data_user2['username'] = "username_user2"
        with allure.step(f"Register user '{register_data_user2['username']}'"):
            user2_params = user2.register_user(register_data_user2)

        # LOGIN AS USER1 AND DELETE USER2
        data = user1.login_and_delete(user1_params, user2_params)
        token = data.get('x-csrf-token')
        auth_sid = data.get('auth_sid')

        # GET USER2
        with allure.step(f"Get userdata of user '{register_data_user2['username']}' and check that user is deleted"):
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
