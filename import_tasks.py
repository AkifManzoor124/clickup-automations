import requests
from copy import deepcopy
from datetime import datetime, timedelta, date

team_id = "10542198"

#include the lists for office hours and meetings
lists = {
    "210793472",
    "216688395",
    "57254735"
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
    "end_of_day": '4:59:00',
    'sprint_end_date': '2022-11-21 4:59:59'
}

api_params = {
    'headers' : {
        "Content-Type": "application/json",
        "Authorization": "pk_14759065_5EHH6LBJQZ1N3CKTS6Z6W44FY8WZ7IS5"
    }
}

def get_filtered_tasks(query):
    url = "https://api.clickup.com/api/v2/team/" + team_id + "/task"

    response = requests.get(url, headers=api_params['headers'], params=query)
    data = response.json()

    return data
    

def get_tasks_to_schedule():
    tasks_to_schedule = []

    data = get_filtered_tasks(query)

    print("\n\n\nTASKS TO BE ASSIGNED\n")
    for task in data["tasks"]:
        if(task["start_date"] == None):
            tasks_to_schedule.append(task)

    return tasks_to_schedule

def get_scheduled_tasks():
    scheduled_tasks = []
    recurring_tasks = []

    data = get_filtered_tasks(query)

    for task in data["tasks"]:
        for custom_field in task["custom_fields"]:
            if(custom_field["name"] == "Recurring Days"):
                recurring_tasks.append(task)
            
    #For whichever tasks don't have the custom field "Recurring Days", add them to the scheduled_tasks list
    for task in data["tasks"]:
        if(task not in recurring_tasks):
            if(task["start_date"] != None):
                scheduled_tasks.append(task)

    return scheduled_tasks, recurring_tasks

def create_duplicate_task(next_day, task):
    task_copy = deepcopy(task)

    start_time = datetime.utcfromtimestamp(int(task['start_date'])/1000).strftime('%H:%M:%S')
    due_time = datetime.utcfromtimestamp(int(task['due_date'])/1000).strftime('%H:%M:%S')

    task_copy['start_date'] = int(datetime.strptime(next_day.strftime('%Y-%m-%d') + ' ' + start_time,'%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    task_copy['due_date'] = int(datetime.strptime(next_day.strftime('%Y-%m-%d') + ' ' + due_time,'%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    
    return task_copy

# I want to now add to recurring_tasks list the task for every weekday until settings['sprint_end_date']
def setup_recurring_tasks(task, occurence):
    duplicated_tasks = []

    days_in_between = int(datetime.strptime(settings["sprint_end_date"],'%Y-%m-%d %H:%M:%S').strftime('%d')) - int(datetime.today().strftime('%d'))

    for i in range(0, days_in_between):
        next_day = datetime.today() + timedelta(days=i)
        if(occurence == 'Everyday'):
            duplicated_tasks.append(create_duplicate_task(next_day, task))
        elif(occurence == 'Weekdays'):
            if(next_day.weekday() < 5):
                duplicated_tasks.append(create_duplicate_task(next_day, task))
        elif(next_day.strftime('%A') == occurence):
            if(i > 1):
                duplicated_tasks.append(create_duplicate_task(next_day, task))

    return duplicated_tasks

def find_recurring_tasks(recurring_tasks):
    recurring_days = []

    for task in recurring_tasks:
        for custom_field in task["custom_fields"]:
            if(custom_field["name"] == "Recurring Days"):
                if('value' in custom_field):
                    for option in custom_field["type_config"]["options"]:
                        for custom_field_value in custom_field["value"]:
                            if(option["id"] == custom_field_value):

                                recurring_day = {
                                    'name': task["name"],
                                    'days': option["label"]
                                }

                                recurring_days.append( recurring_day )
    
    return recurring_days


def replicate_recurring_tasks(recurring_tasks):
    replicated_tasks = []
    recurring_days = []

    #For all the tasks, I want to find the recurring days and then replicate the task for each day
    recurring_days = find_recurring_tasks(recurring_tasks)

    #I want to add the task to the replicated_tasks list for each day that it is recurring until settings['sprint_end_date']

    #If Quranic Studies is recurring on Thursdays, and it can reoccure until settings['sprint_end_date'], then I want to add it to the replicated_tasks list for each Thursday until settings['sprint_end_date']
    #If Evening Ritual is recurring every weekday, I want to add it to the replicated_tasks list for each weekday until settings['sprint_end_date']
    #If Personal Development is recurrin on Monday, Wednesday and Friday, I want to add it to the replicated_tasks list for each Monday, Wednesday and Friday until settings['sprint_end_date']

    for recurring_day in recurring_days:
        for task in recurring_tasks:
            if(recurring_day['name'] == task['name']):
                replicated_tasks.extend(setup_recurring_tasks(task, recurring_day['days']))

    #for whichever tasks that are not in the replicated_tasks list from recurring_tasks, add them to the replicated_tasks list
    for task in recurring_tasks:
        if(task not in replicated_tasks):
            replicated_tasks.append(task)
    
    return replicated_tasks


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

'''
I want to find the next available time slot to schedule a time estimate
I want the scheduled timeslot to be scheduled between the due_date of the second task and start_date of the first task
I want the time estimate to be scheduled within settings[start_of_day] and settings[end_of_day]

return the start_date and due_date of the available time slot
'''
def find_next_available_time_slot(scheduled_tasks, time_estimate):

    start_date = None
    due_date = None

    time_estimate = int(time_estimate)

    available_time_slot = {}

    #convert the start_of_day and end_of_day to datetime objects with today's date
    start_of_day = datetime.strptime(datetime.today().strftime('%Y-%m-%d') + ' ' + settings['start_of_day'],'%Y-%m-%d %H:%M:%S')
    end_of_day = datetime.strptime(datetime.today().strftime('%Y-%m-%d') + ' ' + settings['end_of_day'],'%Y-%m-%d %H:%M:%S')
    start_of_day = start_of_day + timedelta(days=-1)
    end_of_day = end_of_day + timedelta(days=-1)
    
    
    for i in range(0, len(scheduled_tasks)-1):

        if(scheduled_tasks[i]['start_date'] == scheduled_tasks[i+1]['start_date']):
            continue

        if(int(scheduled_tasks[i]['due_date']) > int(scheduled_tasks[i+1]['start_date'])):
            continue


        first_point =  int(scheduled_tasks[i]['due_date'])
        second_point = int(scheduled_tasks[i+1]['start_date'])

        #find if the time estimate + first_point can fit between the two points
        if(time_in_range(first_point, second_point, first_point + time_estimate)):
            start_date = first_point
            due_date = first_point + time_estimate

            print('Time is within range for the task ' + scheduled_tasks[i]['name'] + ' and ' + scheduled_tasks[i+1]['name'])
        

        if(start_date != None and due_date != None):

            #covert the start_date_time and due_date_time to datetime objects
            start_date_time = datetime.fromtimestamp(start_date/1000)
            due_date_time = datetime.fromtimestamp(due_date/1000)

            #add day to end_of_day if start_of_day is greater than end_of_day
            if(start_of_day > end_of_day):
                end_of_day = end_of_day + timedelta(days=1)

            #if the task name is evening ritual, then add a day to start_of_day and end_of_day
            if(scheduled_tasks[i]['name'] == 'Evening Ritual'):
                start_of_day = start_of_day + timedelta(days=1)
                end_of_day = end_of_day + timedelta(days=1)
            
            #if the start_date_time is greater than the start_of_day and the due_date_time is less than the end_of_day, then the time estimate can be scheduled
            if(start_date_time >= start_of_day and due_date_time <= end_of_day):
                available_time_slot = {
                    'start_date': start_date,
                    'due_date': due_date
                }
                return available_time_slot
            




    #If there are no available time slots, then return None
    return None


def schedule_task(task_to_be_scheduled, start_date, end_date):
    url = "https://api.clickup.com/api/v2/task/" + task_to_be_scheduled["id"]
    payload = {
        "name": task_to_be_scheduled["name"],
        "description": task_to_be_scheduled["description"],
        "status": "open",
        "priority": task_to_be_scheduled["priority"],
        "start_date": start_date,
        "start_date_time": True,
        "due_date": end_date,
        "due_date_time": True,
        "time_estimate": task_to_be_scheduled["time_estimate"],
        "assignees": task_to_be_scheduled["assignees"],
        "archived": False,

    }

    print(payload)

    response = requests.put(url, json=payload, headers=api_params['headers'], params=query)
    data = response.json()

    print(data)

    #print the time that the task was scheduled for

#remove duplicate tasks from the list
def remove_duplicate_tasks(tasks):
    #remove duplicate tasks if they have the same name and start_date
    for i in range(0, len(tasks)-1):
        for j in range(i+1, len(tasks)-1):
            if(tasks[i]['name'] == tasks[j]['name'] and int(tasks[i]['start_date']) == int(tasks[j]['start_date'])):
                
                print('Removing duplicate task ' + tasks[j]['name'])
                del tasks[j]


    
    return tasks


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
# Fix the issue with personal development showing for today, and also missing for a day
# Need to fix the bug where tasks are being scheduled for the same time
# fix turbo console log
# add feature for tasks that have recurring days which end on a certain date
# add feature for tasks that have recurring days which end after a certain number of occurrences
# add feature to exclude certain days from being scheduled
# add feature to only allow tasks to be scheduled on certain times of the day and certain days of the week
# Fix the bug where recurring tasks are being scheduled for the same time
# Remove tasks that are scheduled after sprint end date


print("\n\n\nScheduled Times\n")

scheduled_tasks, recurring_tasks = get_scheduled_tasks()

for task in scheduled_tasks:
    print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))


replicated_tasks = remove_duplicate_tasks(replicate_recurring_tasks(recurring_tasks))

print("\n\n\nRecurring Times Removing Duplicates\n")

for task in replicated_tasks:
   print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))


tasks_to_schedule = get_tasks_to_schedule()

for task_to_schedule in tasks_to_schedule:
    print(task_to_schedule["name"], task_to_schedule["time_estimate"]) 



print("\n\n\n")
print("\nBefore Sorting Replicated Times\n")

for task in replicated_tasks:  
    #convert start_date to string
    task['start_date'] = str(task['start_date'])

print("\n\n\n")
print("\nAfter Sorting Replicated Times Based on name\n")

#sort the replicated tasks by name
replicated_tasks.sort(key = lambda i: i['name'])

for task in replicated_tasks:  
    print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))

#add the scheduled tasks to the replicated tasks
replicated_tasks.extend(scheduled_tasks)

print("\n\n\n")
print("\nAfter Extending replicated tasks with scheduled_tasks\n")  

for task in replicated_tasks:  
    print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))

print("\n\n\n")
print("\nAfter Sorting Replicated Times Based on start_date\n")   

replicated_tasks.sort(key=lambda x: x["start_date"])

for task in replicated_tasks:  
    print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))

for task_to_schedule in tasks_to_schedule:
    available_time_slot = find_next_available_time_slot(replicated_tasks, task_to_schedule["time_estimate"])

    if available_time_slot is not None:
        print("\nScheduling task: ", task_to_schedule["name"], " at ", datetime.utcfromtimestamp(int(available_time_slot['start_date'])/1000).strftime('%Y-%m-%d %H:%M:%S'), " to ", datetime.utcfromtimestamp(int(available_time_slot['due_date'])/1000).strftime('%Y-%m-%d %H:%M:%S'))

        task_to_schedule["start_date"] = str(available_time_slot['start_date'])
        task_to_schedule["due_date"] = str(available_time_slot['due_date'])

        replicated_tasks.append(deepcopy(task_to_schedule))
        
        replicated_tasks.sort(key=lambda x: x['start_date'])

        print('\n\n\n')

        for task in replicated_tasks:
            print(task["name"], datetime.utcfromtimestamp(int(task["start_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(int(task["due_date"])/1000).strftime('%Y-%m-%d %H:%M:%S'))

    #schedule_task(task_to_schedule, available_time_slot['start_date'], available_time_slot['due_date'])


