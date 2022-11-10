import requests
from datetime import datetime

team_id = "10542198"

#include the lists for office hours and meetings
lists = {
    "210793472",
    "216688395",
    "57254735"
}



url = "https://api.clickup.com/api/v2/team/" + team_id + "/task"

headers = {
    "Content-Type": "application/json",
    "Authorization": "pk_14759065_9UEWXK3AEJPW1GO8IRYF484IE910H3JL"
}

query = {
    "archived": "false",
    "page": "0",
    "order_by": "due_date",
    "reverse": "true",
    "subtasks": "false",
    "include_closed": "false",
    "statuses": ['Open', 'In Progress', 'scheduled'],
    "custom_fields": "[{\"field_id\":\"038dd945-e9c6-443d-92c7-169a15adaf7d\",\"operator\":\"IS NOT NULL\",\"value\":\"Yes\"}]",
}

settings={
    "start_of_day": '12:00:00',
    "end_of_day": '4:00:00',
}


def get_tasks_to_schedule():
    tasks_to_schedule = []

    response = requests.get(url, headers=headers, params=query)
    data = response.json()

    print("\n\n\nTASKS TO BE ASSIGNED\n")
    for task in data["tasks"]:
        if(task["start_date"] == None):
            tasks_to_schedule.append(task)

    return tasks_to_schedule

def get_scheduled_tasks():
    scheduled_tasks = []

    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    for task in data["tasks"]:
        if(task["start_date"] != None):
            scheduled_tasks.append(task)

    return scheduled_tasks

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def find_next_available_time(blocked_tasks, time_estimate):
    time_estimate = int(task["time_estimate"])
    for i in range(0, len(blocked_tasks)-1):

        unix_start_of_day = datetime.strptime(settings["start_of_day"],"%H:%M:%S")
        unix_end_of_day = datetime.strptime(settings["end_of_day"],"%H:%M:%S")

        if(int(blocked_tasks[i+1]["start_date"]) - int(blocked_tasks[i]["due_date"]) > time_estimate):

            end_date = int(blocked_tasks[i]["due_date"]) + time_estimate

            #If the hour of the due date falls inside of the start_of_day and end_of_day, then schedule the task
            due_date_hour: int = datetime.utcfromtimestamp(int(blocked_tasks[i]["due_date"])/1000).strftime('%H')
            start_of_day_hour = unix_start_of_day.strftime('%H')
            end_of_day_hour = unix_end_of_day.strftime('%H')

            if(time_in_range(start_of_day_hour, end_of_day_hour, due_date_hour)):
                return blocked_tasks[i]["due_date"], end_date
            else:
                continue
        else:
            continue

def schedule_task(task, start_date, end_date):
    url = "https://api.clickup.com/api/v2/task/" + task["id"]
    payload = {
        "name": task["name"],
        "description": task["description"],
        "status": "open",
        "priority": task["priority"],
        "start_date": start_date,
        "start_date_time": True,
        "due_date": end_date,
        "due_date_time": True,
        "time_estimate": task["time_estimate"],
        "assignees": task["assignees"],
        "archived": False,

    }
    response = requests.put(url, json=payload, headers=headers, params=query)
    data = response.json()

    #print the time that the task was scheduled for

response = requests.get(url, headers=headers, params=query)
data = response.json()

# create a secret env file to store the api key
# can only include tasks that have a time estimate
# Why was one of my timeslots completely skipped?
# I want to add the ability to add recurring tasks within the scheduled_tasks
# I want to add comments to my code to make it more readable
# I want to hook up github issues/PRs to my clickup tasks so that I can schedule them as well
# Find out how to retrieve tasks with custom fields as a label 
# I want the ability to exclude certain times slots and days from being scheduled
# I want to retrieve scheduled meetings within my calendar and exclude those times from being scheduled
# Create a function that will retrieve all the tasks which need to be scheduled



scheduled_tasks = get_scheduled_tasks()

task = get_tasks_to_schedule()[0];
print(task["name"] + " " + str(task["start_date"]) + " " + str(task["due_date"]) + " " + str(task["time_estimate"]) + '\n\n\n')

start_date, end_date = find_next_available_time(scheduled_tasks, task["time_estimate"])
schedule_task(task, start_date, end_date)


print("\n\n\nBLOCKED TIMES\n")
for task in get_scheduled_tasks():
    print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))