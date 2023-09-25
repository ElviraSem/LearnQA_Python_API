import requests
import datetime
from datetime import timezone, timedelta


class TestIdentifyHeaders:
    def get_error_text(self, text):
        return "Cannot find header with name " + text + " in response"

    def test_identify_headers(self):

        response = requests.post("https://playground.learnqa.ru/api/homework_header")

        current_datetime_utc = datetime.datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S')

        delta_sec = 1  # time acceptance error receiving datetime value in headers
        current_datetime_utc_min = datetime.datetime.now(timezone.utc) - timedelta(seconds=delta_sec)
        current_datetime_utc_max = datetime.datetime.now(timezone.utc) + timedelta(seconds=delta_sec)

        current_datetime_utc_str_min = str(current_datetime_utc_min.strftime('%a, %d %b %Y %H:%M:%S')) + ' GMT'
        current_datetime_utc_str_max = str(current_datetime_utc_max.strftime('%a, %d %b %Y %H:%M:%S')) + ' GMT'

        headers_list = response.headers

        headers = {}
        index = 0
        for header_item in headers_list:
            header = header_item
            header_value = response.headers.get(header)
            print("header: " + header + " ; " + "header_value: " + header_value)

            headers[index] = {header: header_value}
            index += 1

        print("headers: ", headers)

        assert 'Date' in response.headers, self.get_error_text("'Date'")
        assert 'Content-Type' in response.headers, self.get_error_text("'Content-Type'")
        assert 'Content-Length' in response.headers, self.get_error_text("'Content-Length'")
        assert 'Connection' in response.headers, self.get_error_text("'Connection'")
        assert 'Keep-Alive' in response.headers, self.get_error_text("'Keep-Alive'")
        assert 'Server' in response.headers, self.get_error_text("'Server'")
        assert 'x-secret-homework-header' in response.headers, self.get_error_text("'x-secret-homework-header'")
        assert 'Cache-Control' in response.headers, self.get_error_text("'Cache-Control'")
        assert 'Expires' in response.headers, self.get_error_text("'Expires'")

        assert (headers[0] == {'Date': current_datetime_utc} or {'Date': current_datetime_utc_str_min} or
                {'Date': current_datetime_utc_str_max}), (
            self.get_error_text(f"'Date' and value '{current_datetime_utc}'"))  # Take into account an acceptable error
        # for time in current_datetime_utc and header value

        assert headers[1] == {'Content-Type': 'application/json'},  self.get_error_text("'Content-Type' and value "
                                                                                        "'application/json'")
        assert headers[2] == {'Content-Length': '15'}, self.get_error_text("'Content-Length' and value '15'")
        assert headers[3] == {'Connection': 'keep-alive'}, self.get_error_text("'Connection' and value 'keep-alive'")
        assert headers[4] == {'Keep-Alive': 'timeout=10'}, self.get_error_text("'Keep-Alive' and value 'timeout=10'")
        assert headers[5] == {'Server': 'Apache'}, self.get_error_text("'Server' and value 'Apache'")
        assert headers[6] == {'x-secret-homework-header': 'Some secret value'}, (
            self.get_error_text("'x-secret-homework-header' and value 'Some secret value'"))
        assert headers[7] == {'Cache-Control': 'max-age=0'}, self.get_error_text("'Cache-Control' and value "
                                                                                 "'max-age=0'")

        assert (headers[8] == {'Expires': current_datetime_utc} or {'Expires': current_datetime_utc_str_min} or
                {'Expires': current_datetime_utc_str_max}), (
            self.get_error_text(f"'Expires' and value '{current_datetime_utc}'"))  # Take into account an acceptable
        # error for time in current_datetime_utc and header value
