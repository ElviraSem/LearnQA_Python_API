from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("UTF-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email_format(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("UTF-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    user_empty_params = [
        ('newuser', 'userFirstName', 'userLastName', '123', None),
        ('newuser', 'userFirstName', 'userLastName', None, 'newuser@example.com'),
        ('newuser', 'userFirstName', None, '123', 'newuser@example.com'),
        ('newuser', None, 'userLastName', '123', 'newuser@example.com'),
        (None, 'userFirstName', 'userLastName', '123', 'newuser@example.com')
    ]

    # @pytest.mark.parametrize('username, firstName, lastName, password, email')
    # def test_create_user_without_any_parameter(self):
    #
    #
    #     response = MyRequests.post("/user/", data=user_empty_params)
    #     print(response.status_code)
    #
    #     Assertions.assert_code_status(response, 400)
    #     assert response.content.decode("UTF-8") == "Invalid email format", \
    #         f"Unexpected response content {response.content}"