import json.decoder
import secrets
from datetime import datetime
from requests import Response
import random
import string


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    @staticmethod
    def generate_name(length: int):
        letters = string.ascii_letters
        digits = string.digits
        synbols = string.ascii_letters + string.digits
        name = ''.join(random.choices(synbols, k=length))
        return name

    @staticmethod
    def prepare_email(base_part="learnqa", domain="example.ru"):
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        return email

    @staticmethod
    def prepare_name_list_with_definite_length(length: int):

        data = [
            (BaseCase.generate_name(length), 'userFirstName', 'userLastName', '123', BaseCase.prepare_email()),
            ('newuser', BaseCase.generate_name(length), 'userLastName', '123', BaseCase.prepare_email("learnqa1")),
            ('newuser', 'userFirstName', BaseCase.generate_name(length), '123', BaseCase.prepare_email("learnqa2"))
        ]
        return data






