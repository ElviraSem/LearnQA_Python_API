import json

json_text = ('{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And '
             'this is a second message","timestamp":"2021-06-04 16:41:01"}]}')

obj = json.loads(json_text) # json_text string parsing

second_element_of_obj = obj['messages'][1]  # Second element of 'messages' dict
second_message_text = second_element_of_obj['message']

print(second_message_text)


