import requests
import json

headers = {"content-type": "application/json",
           "X-Api-Key": "MTEzMzA5ZTItMzA5Ny00OWZjLTkwN2UtOGJjMGU1NTZhNmQ1"}

workspaceId = "609a64c9ce8463062672b547"
userId = "609a64c9ce8463062672b546"
API_URL = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries"

# includes response status
response_data = requests.get(API_URL, headers=headers)

# list of tasks in workspace
task_list = json.loads(response_data.text)
for task in task_list:
    print(task)
