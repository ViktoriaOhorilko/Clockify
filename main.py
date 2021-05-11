import requests, json, sys, datetime

headers = {"content-type": "application/json",
           "X-Api-Key": "MTEzMzA5ZTItMzA5Ny00OWZjLTkwN2UtOGJjMGU1NTZhNmQ1"}

workspaceId = "609a64c9ce8463062672b547"
userId = "609a64c9ce8463062672b546"
API_URL = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries"

# includes response status
response_data = requests.get(API_URL, headers=headers)

# list of tasks in workspace
task_list = json.loads(response_data.text)
total_time = datetime.timedelta(seconds=0)
finished_tasks = 0
for task in task_list:

    start_time = task['timeInterval']['start']
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    end_time = task['timeInterval']['end']
    if end_time == None:
        end_time = start_time
    else:
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        finished_tasks += 1

    duration = (end_time - start_time)
    total_time += duration

    sys.stdout.write('\nTask name: ' + task['description'])
    sys.stdout.write('\n\tStart: ' + str(start_time))
    sys.stdout.write('\n\tEnd: ' + str(end_time))
    sys.stdout.write('\n\tDuration: ' + str(duration))

sys.stdout.write('\n\nTotal time: ' + str(total_time))
if len(task_list) == finished_tasks:
    sys.stdout.write('\nAll task(s) finished.')
else:
    sys.stdout.write('\n' + str(len(task_list) - finished_tasks) + ' task(s) still in process.')
