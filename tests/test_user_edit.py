from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
from lib.user_actions import UserActions


class TestUserEdit(BaseCase):

    data_for_edit = {
        'username': "Changed name",
        'firstName': "Changed first name",
        'lastName': "Changed last name",
        'password': "Changed password",
        'email': BaseCase.prepare_email("edit", "my.ru")
    }

    def test_edit_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_params['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        # GET
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

    @allure.description("Edit user data without being authorized")
    def test_edit_unauthorized_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()

        user_params = user.register_user(register_data)

        # EDIT
        for key, name in self.data_for_edit.items():
            response = MyRequests.put(f"/user/{user_params['id']}",
                                      data={key: name}
                                      )
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("UTF-8") == "Auth token not supplied", "User is authorized without token"

    @allure.description("This test checks that user's params can't be edited by another authorized user")
    def test_user_edited_by_another_authorized_user(self):
        user1 = UserActions()
        user2 = UserActions()

        # REGISTER USER1
        data_user1 = self.prepare_registration_data()
        user1_params = user1.register_user(data_user1)

        # REGISTER USER2
        data_user2 = self.prepare_registration_data()
        user2_params = user2.register_user(data_user2)

        # LOGIN AS USER2
        data = {
            'email': user2_params['email'],
            'password': user2_params['password']
        }

        response_user2_login = MyRequests.post("/user/login", data=data)
        auth_sid_user2 = self.get_cookie(response_user2_login, "auth_sid")
        token_user2 = self.get_header(response_user2_login, "x-csrf-token")

        # EDIT USER1 DATA BY AUTHORIZED USER2
        for key, name in self.data_for_edit.items():

            response_edit_u1_by_u2 = MyRequests.put(f"/user/{user1_params['id']}",
                                                    headers={"x-csrf-token": token_user2},
                                                    cookies={"auth_sid": auth_sid_user2},
                                                    data={key: name}
                                                    )

            Assertions.assert_code_status(response_edit_u1_by_u2, 200)

        # LOGIN AS USER1 AND CHECK USER DATA
        UserActions.login_and_check_user_data(user1, user1_params)

    @allure.description("Edit user email without '@' symbol being authorized")
    def test_edit_email_of_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = user_params['email'].replace('@', '')
        response3 = MyRequests.put(f"/user/{user_params['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'email': new_email}
                                   )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("UTF-8") == "Invalid email format", \
            "User is authorized with invalid email format"

    @allure.description("Edit firstName to 1 symbol long being authorized")
    def test_edit_firstname_to_short_of_just_created_user(self):
        user = UserActions()

        # REGISTER
        register_data = self.prepare_registration_data()
        user_params = user.register_user(register_data)

        # LOGIN
        login_data = {
            'email': user_params['email'],
            'password': user_params['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_firstname = self.generate_name(1)
        response3 = MyRequests.put(f"/user/{user_params['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_firstname}
                                   )

        error = self.get_json_value(response3, 'error')

        Assertions.assert_code_status(response3, 400)
        assert error == "Too short value for field firstName"
