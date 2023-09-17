import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

redirects = response.history
redirects_number = len(redirects)
last_url = redirects[redirects_number-1].url

print("Number of redirects = ", redirects_number)
print(f"The last url is {last_url}")





