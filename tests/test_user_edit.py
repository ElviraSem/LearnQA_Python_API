from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from lib.user_actions import UserActions


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):

    data_for_edit = {
        'username': "Changed name",
        'firstName': "Changed first name",
        'lastName': "Changed last name",
        'password': "Changed password",
        'email': BaseCase.prepare_email("edit", "my.ru")
    }

    @allure.feature("Positive user edit scenarios")
    @allure.story("Basic user edit scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("PUT request")
    @allure.title("New authorized User edits his own user data")
    @allure.description("User edits his own user data being authorized")
    def test_edit_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Register user with email '{register_data['email']}'"):
            user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        with allure.step(f"Login as User by email '{login_data['email']}' and password '{login_data['password']}'"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        with allure.step(f"Edit 'firstName'"):
            response3 = MyRequests.put(f"/user/{user_params['id']}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={'firstName': new_name}
                                       )
            Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step(f"Check edited User's firstName"):
            response4 = MyRequests.get(f"/user/{user_params['id']}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       )
            Assertions.assert_json_value_by_name(
                response4,
                'firstName',
                new_name,
                "Wrong name of user after edit"
            )

    @allure.feature("Negative user edit scenarios")
    @allure.story("User edit scenario with incorrect input data")
    @allure.tag("PUT request")
    @allure.title("Edit user data without being authorized")
    @allure.description("Test check that user data can't be edited without his being authorized")
    def test_edit_unauthorized_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Register user with email '{register_data['email']}'"):
            user_params = user.register_user(register_data)

        # EDIT
        for key, name in self.data_for_edit.items():
            with allure.step(f"Edit '{key}' in user params"):
                response = MyRequests.put(f"/user/{user_params['id']}",
                                          data={key: name}
                                          )
                Assertions.assert_code_status(response, 400)
                assert response.content.decode("UTF-8") == "Auth token not supplied", "User is authorized without token"

    @allure.feature("Negative user edit scenarios")
    @allure.story("User edit scenario by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("PUT request")
    @allure.title("Edit user data by another authorized user")
    @allure.description("This test checks that user's params can't be edited by another authorized user")
    def test_user_edited_by_another_authorized_user(self):
        user1 = UserActions()
        user2 = UserActions()

        # REGISTER USER1
        data_user1 = self.prepare_registration_data()
        with allure.step(f"Register User1 with email '{data_user1['email']}'"):
            user1_params = user1.register_user(data_user1)

        # REGISTER USER2
        data_user2 = self.prepare_registration_data()
        with allure.step(f"Register User2 with email '{data_user2['email']}'"):
            user2_params = user2.register_user(data_user2)

        # LOGIN AS USER2
        data = {
            'email': user2_params['email'],
            'password': user2_params['password']
        }
        with allure.step(f"Login as User2 by email '{data['email']}' and password '{data['password']}'"):
            response_user2_login = MyRequests.post("/user/login", data=data)
            auth_sid_user2 = self.get_cookie(response_user2_login, "auth_sid")
            token_user2 = self.get_header(response_user2_login, "x-csrf-token")

        # EDIT USER1 DATA BY AUTHORIZED USER2
        for key, name in self.data_for_edit.items():
            with allure.step(f"Edit '{key}' in User1"):
                response_edit_u1_by_u2 = MyRequests.put(f"/user/{user1_params['id']}",
                                                        headers={"x-csrf-token": token_user2},
                                                        cookies={"auth_sid": auth_sid_user2},
                                                        data={key: name}
                                                        )

                Assertions.assert_code_status(response_edit_u1_by_u2, 200)

        # LOGIN AS USER1 AND CHECK USER DATA
        with allure.step(f"Login as User1 by email '{user1_params['email']}' "
                         f"and password '{user1_params['password']}'"):
            UserActions.login_and_check_user_data(user1, user1_params)

    @allure.feature("Negative user edit scenarios")
    @allure.story("User edit scenario with incorrect input data")
    @allure.tag("PUT request")
    @allure.title("Edit user email without '@' symbol being authorized")
    @allure.description("Test checks that authorized user can't edit his email which hasn't '@' symbol")
    def test_edit_email_of_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Register User with email '{register_data['email']}'"):
            user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        with allure.step(f"Login as User by email '{login_data['email']}' and password '{login_data['password']}'"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = user_params['email'].replace('@', '')
        with allure.step(f"Edit 'email' of User to invalid format"):
            response3 = MyRequests.put(f"/user/{user_params['id']}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={'email': new_email}
                                       )
            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode("UTF-8") == "Invalid email format", \
                "User is authorized with invalid email format"

    @allure.feature("Negative user edit scenarios")
    @allure.story("User edit scenario with incorrect input data")
    @allure.tag("PUT request")
    @allure.title("Edit firstName to string of 1 symbol long by authorized user")
    @allure.description("Edit firstName to string of 1 symbol long being authorized")
    def test_edit_firstname_to_short_of_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step(f"Register User with email '{register_data['email']}'"):
            user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        with allure.step(f"Login as User by email '{login_data['email']}' and password '{login_data['password']}'"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_firstname = self.generate_name(1)
        with allure.step(f"Edit 'firstName' of User to short string of 1 symbol long"):
            response3 = MyRequests.put(f"/user/{user_params['id']}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={'firstName': new_firstname}
                                       )

            error = self.get_json_value(response3, 'error')

            Assertions.assert_code_status(response3, 400)
            assert error == "Too short value for field firstName"
