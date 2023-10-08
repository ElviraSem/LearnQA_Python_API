from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

import pytest
import allure


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):

    user_empty_params = [
        ('newuser', 'userFirstName', 'userLastName', '123', None),
        ('newuser', 'userFirstName', 'userLastName', None, 'newuser@example.com'),
        ('newuser', 'userFirstName', None, '123', 'newuser@example.com'),
        ('newuser', None, 'userLastName', '123', 'newuser@example.com'),
        (None, 'userFirstName', 'userLastName', '123', 'newuser@example.com')
    ]

    user_short_params = BaseCase.prepare_name_list_with_definite_length(1)

    user_long_params = BaseCase.prepare_name_list_with_definite_length(250)

    @allure.feature("Positive user registration scenarios")
    @allure.story("Basic user registration scenario")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("POST request")
    @allure.title("User registration scenario")
    @allure.description("Test checks that user exists after sending POST request for register")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        with allure.step(f"Register user '{data['username']}'"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.feature("Negative user registration scenarios")
    @allure.story("Basic user registration scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("POST request")
    @allure.title("User registration if user with the same email already exists")
    @allure.description("Test checks that user can't be registered if user with the same email has been registered")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        with allure.step(f"Register user with email '{data['email']}'"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("UTF-8") == f"Users with email '{email}' already exists", \
                f"Unexpected response content {response.content}"

    @allure.feature("Negative user registration scenarios")
    @allure.story("User registration with incorrect input data")
    @allure.tag("POST request")
    @allure.title("User registration with incorrect email format")
    @allure.description("This test checks that user cannot be registered with incorrect email format")
    def test_create_user_with_incorrect_email_format(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        with allure.step(f"Register user with email '{data['email']}'"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("UTF-8") == "Invalid email format", \
                f"Unexpected response content {response.content}"

    @allure.feature("Negative user registration scenarios")
    @allure.story("User registration with incorrect input data")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("POST request")
    @allure.title("User registration without one of POST-request input params")
    @allure.description("This test checks that user cannot be registered without one of params")
    @pytest.mark.parametrize('username, firstname, lastname, password, email', user_empty_params)
    def test_create_user_without_any_parameter(self, username, firstname, lastname, password, email):

        user_params = {
            'username': username,
            'firstName': firstname,
            'lastName': lastname,
            'password': password,
            'email': email
        }

        for user_param in user_params:
            if user_param is None:
                empty_field = user_param
                with (allure.step(f"Register user without  '{user_param}'")):
                    response = MyRequests.post("/user/", data=user_params)

                    Assertions.assert_code_status(response, 400)
                    assert response.content.decode("UTF-8") == (f"The following required params are missed:"
                                                                f" {empty_field}"), ("Unexpected response content "
                                                                                     "{response.content}")

    @allure.feature("Negative user registration scenarios")
    @allure.story("User registration with incorrect input data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("POST request")
    @allure.title("User registration with one of names of 1 symbol long")
    @allure.description("This test checks that user cannot be registered with one of names of 1 symbol long")
    @pytest.mark.parametrize('username, firstName, lastName, password, email', user_short_params)
    def test_create_user_with_short_name(self, username, firstName, lastName, password, email):

        data = {
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'password': '123',
            'email': email
        }

        current_name = ""
        for key, name in data.items():
            if len(name) == 1:
                current_name = key
        with allure.step(f"Register user with  '{current_name}' of 1 symbol long"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("UTF-8") == f"The value of '{current_name}' field is too short", \
                f"Unexpected response content {response.content}"

    @allure.feature("Negative user registration scenarios")
    @allure.story("User registration with incorrect input data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("POST request")
    @allure.title("User registration with one of names of 250 symbols long")
    @allure.description("This test checks that user can be registered with one of names of 250 symbols long")
    @pytest.mark.parametrize('username, firstName, lastName, password, email', user_long_params)
    def test_create_user_with_long_name(self, username, firstName, lastName, password, email):

        data = {
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'password': '123',
            'email': email
        }

        current_name = ""
        for key, name in data.items():
            if len(name) == 250:
                current_name = key
        with allure.step(f"Register user with  '{current_name}' of 250 symbols long"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")
