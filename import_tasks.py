import requests

list_id = "210793472"

lists = {
    "210793472",
    "216688395"
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
