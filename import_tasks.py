import requests

list_id = "210793472"

lists = {
    "210793472",
    "216688395",
    "57254735"
}

url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

query = {
  "archived": "false",
  "page": "0",
  "order_by": "string",
  "reverse": "true",
  "subtasks": "false",
  "statuses": "string",
  "include_closed": "true",
  "assignees": "string",
  "tags": "string",
  "due_date_gt": "0",
  "due_date_lt": "0",
  "date_created_gt": "0",
  "date_created_lt": "0",
  "date_updated_gt": "0",
  "date_updated_lt": "0",
  "custom_fields": "string"
}

# create a secret env file to store the api key
headers = {
  "Content-Type": "application/json",
  "Authorization": "pk_14759065_KDKZBH5ECUN3UZYYE00QY4MN7FLJ7GD1"
}

response = requests.get(url, headers=headers, params=query)

data = response.json()
print(data)

timeframe = "2 weeks"
schedule_by = "priority"



def filter_tasks():
    return

def decipher_avaliability():
    return

#only retrieve tasks which have a time estimate
def get_tasks():
    return

def schedule_tasks(timeframe, schedule_by):
    return