import requests
import time

request_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

task_ready_status = "Job is ready"
task_processing_status = "Job is NOT ready"
task_token_incorrect_error = "No job linked to this token"


def check_task_attrs(task_executing_response, timeout):
    result_token = task_executing_response.json()["token"]
    task_execution_time = task_executing_response.json()["seconds"]
    parameters = {"token": result_token}

    time.sleep(timeout)

    check_task_values = requests.get(request_url, params=parameters)

    if "error" in check_task_values.json():
        print(f"Error: No job linked to this token {result_token}")
    else:
        task_status = str(check_task_values.json()["status"])

    if timeout > task_execution_time:
        if task_status == task_ready_status:
            print("Task status is correct. It is the following: " + task_ready_status)
        else:
            print("Error: Task status is incorrect")
    elif task_status == task_processing_status:
            print("Task status is correct. It is the following: " + task_processing_status)
    else:
        print("Task status was incorrectly measured.")
        return

    if 'result' in check_task_values.json():
        task_result = check_task_values.json()["result"]
        print(f"'result' = {task_result} in json-response")
    elif task_status == 'Job is NOT ready':
        print("'result' is absent because the task is not ready")
    else:
        print("Take attention: Task was not executed")
        return


"""
Sending Request for new task executing:
"""
response_of_new_ticket = requests.get(request_url)

task_execution_time_sec = response_of_new_ticket.json()["seconds"]

"""
Immediate status check for task - 'status': 'Job is NOT ready'
"""
print("\n***\nImmediate status check for task:\n***")
check_task_attrs(response_of_new_ticket, 0)

"""
Status check for task after timeout > 'task execution time' - 'status': 'Job is ready'
"""
print("\n***\nStatus check for task after it is ready:\n***")
check_task_attrs(response_of_new_ticket, task_execution_time_sec + 1)
