import requests

list_id = "210793472"

lists = {
    "210793472",
    "216688395",
    "57254735"
}

url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

headers = {
  "Content-Type": "application/json",
  "Authorization": "pk_14759065_KDKZBH5ECUN3UZYYE00QY4MN7FLJ7GD1"
}

query = {
  "archived": "false",
  "page": "0",
  "reverse": "true",
  "subtasks": "false",
  "include_closed": "false",
  "statuses": ['Open', 'In Progress', 'scheduled'],
}

# create a secret env file to store the api key

timeframe = "2 weeks"
schedule_by = "priority"



def get_tasks():
    return

def filter_tasks():
    return

def decipher_avaliability():
    return

def schedule_tasks(timeframe, schedule_by):
    return


response = requests.get(url, headers=headers, params=query)
data = response.json()

for task in data["tasks"]:
    print(task["name"])
