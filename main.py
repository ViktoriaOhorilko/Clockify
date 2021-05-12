import requests, json, sys, datetime

headers = {"content-type": "application/json",
           "X-Api-Key": "MTEzMzA5ZTItMzA5Ny00OWZjLTkwN2UtOGJjMGU1NTZhNmQ1"}

API_URL = "https://api.clockify.me/api/v1/user"


# returns dictionary with workspace/user IDs by "X-Api-Key"
def get_IDs():
    global API_URL
    response_data = requests.get(API_URL, headers=headers)
    user_data = json.loads(response_data.text)
    workspaceId = user_data['activeWorkspace']
    userId = user_data['id']
    return {'workspaceId': workspaceId,
            'userId': userId}


# returns array of tasks by workspace/user ID
def get_tasks(workspaceId=None, userId=None):
    API_URL = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries"
    response_data = requests.get(API_URL, headers=headers)
    return json.loads(response_data.text)


# returns dictionary of tasks array by key 'date'
def form_data(task_list):
    dated_list = dict()

    for task in task_list:
        new_task = dict()

        new_task['description'] = task['description']
        start_time = task['timeInterval']['start']
        end_time = task['timeInterval']['end']

        if end_time:
            new_task['status'] = 'finished'
        else:
            end_time = start_time
            new_task['status'] = 'in process'

        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        duration = (end_time - start_time)

        new_task['start_time'] = start_time.time()
        new_task['end_time'] = end_time.time()
        new_task['duration'] = duration
        date = start_time.date()

        if date not in dated_list:
            dated_list[date] = []

        dated_list[date].append(new_task)

    return dated_list


# print tasks and count used time by date/total
def print_data(task_list):
    total_time = datetime.timedelta(seconds=0)

    for date in task_list:
        total_time_by_date = datetime.timedelta(seconds=0)

        for task in task_list[date]:

            sys.stdout.write('\nTask name: ' + task['description'])
            sys.stdout.write('\n\tStart: ' + str(task['start_time']))

            if task['status'] == 'finished':
                sys.stdout.write('\n\tEnd: ' + str(task['end_time']))
                sys.stdout.write('\n\tDuration: ' + str(task['duration']))
            else:
                sys.stdout.write('\n\tStill in process...')

            total_time_by_date += task['duration']

        sys.stdout.write('\n\nTotal time by '+str(date)+': '+str(total_time_by_date))
        total_time += total_time_by_date

    sys.stdout.write('\n\nTotal time by all time: ' + str(total_time))


if __name__ == '__main__':
    IDs = get_IDs()
    task_list = get_tasks(workspaceId=IDs['workspaceId'],
                          userId=IDs['userId'])

    task_list = form_data(task_list)
    print_data(task_list)

