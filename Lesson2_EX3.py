import requests

request_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

methods = {"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}

negative_response = "Wrong method provided"
positive_response = '{"success":"!"}'


def print_incorrect_server_answers(url, request_type: str, params: tuple):
    index = 0
    for index in range(len(methods)):
        current_parameter = methods[index]["method"]
        if request_type == "GET":
            response = requests.get(url, params=params[index])
        elif request_type == "POST":
            response = requests.post(url, data=params[index])
        elif request_type == "PUT":
            response = requests.put(url, data=params[index])
        elif request_type == "DELETE":
            response = requests.delete(url, data=params[index])
        else:
            print(f"Request type '{request_type}' is out of range (GET, POST, PUT, DELETE)")
            return

        request_type = response.request.method

        if (current_parameter != request_type) and (response.text == positive_response):
            print(f"{request_type}-Request method and 'method':'{current_parameter}' in params are different but "
                  f"response is positive: " + '{''"success":"!"}')
        if (current_parameter == request_type) and (response.text == negative_response):
            print(f"{request_type}-Request method and 'method':'{current_parameter}' in params are the same but "
                  f"response is negative: 'Wrong method provided'")
        index = index + 1

"""
http-request without 'method' parameter:
"""
print("Task #1 - http-request without 'method' parameter:")
get_response_without_params = requests.get(request_url)
post_response_without_params = requests.post(request_url)
put_response_without_params = requests.put(request_url)
delete_response_without_params = requests.delete(request_url)

print("Response of GET-request without parameters: ", get_response_without_params.text)
print("Response of POST-request without parameters: ", post_response_without_params.text)
print("Response of PUT-request without parameters: ", put_response_without_params.text)
print("Response of DELETE-request without parameters: ", delete_response_without_params.text)

"""
http-request with 'HEAD' parameter which is out of 'method' parameter range:
"""
print("\nTask #2 - http-request with 'HEAD' parameter which is out of 'method' parameter range:")
head_payload = {"method": "HEAD"}
get_response_with_extra_param = requests.get(request_url, params=head_payload)
post_response_with_extra_param = requests.post(request_url, data=head_payload)
put_response_with_extra_param = requests.put(request_url, data=head_payload)
delete_response_with_extra_param = requests.delete(request_url, data=head_payload)

print("Response of GET-request with 'method = HEAD' parameter': ", get_response_with_extra_param.text)
print("Response of POST-request with 'method = HEAD' parameter': ", post_response_with_extra_param.text)
print("Response of PUT-request with 'method = HEAD' parameter': ", put_response_with_extra_param.text)
print("Response of DELETE-request with 'method = HEAD' parameter': ", delete_response_with_extra_param.text)

"""
http-request with correct 'method' parameter:
"""

print("\nTask #3 - http-request with correct 'method' parameter:")
get_response_with_correct_parameter = requests.get(request_url, params=methods[0])
post_response_with_correct_parameter = requests.post(request_url, data=methods[1])
put_response_with_correct_parameter = requests.put(request_url, data=methods[2])
delete_response_with_correct_parameter = requests.delete(request_url, data=methods[3])

print("Response of GET-request with 'method = GET' parameter': ", get_response_with_correct_parameter.text)
print("Response of POST-request 'method = POST' parameter': ", post_response_with_correct_parameter.text)
print("Response of PUT-request 'method = PUT' parameter': ", put_response_with_correct_parameter.text)
print("Response of DELETE-request 'method = DELETE' parameter': ", delete_response_with_correct_parameter.text)

print("\nTask #4 - incorrect result of http-request with 'method' parameter:")
print_incorrect_server_answers(request_url, "GET", methods)
print_incorrect_server_answers(request_url, "POST", methods)
print_incorrect_server_answers(request_url, "PUT", methods)
print_incorrect_server_answers(request_url, "DELETE", methods)



