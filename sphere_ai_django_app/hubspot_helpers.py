import openai
import json
import requests


def get_object_type(question):
  response = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[{'role': 'user', 'content': question}],
      temperature=0.5
  )
  object_type = response.choices[0].message.content.strip()
  if object_type.endswith('.'):
      object_type = object_type[:-1]

  return object_type


def get_properties(api_client, object_type):
  properties = api_client.crm.properties.core_api.get_all(
      object_type=object_type, archived=False)
  return list(map(lambda result: result.name, properties.results))


def get_body(prompt):
  response_body = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[{'role': 'user', 'content': prompt}],
      temperature=0.5
  )
  body = response_body.choices[0].message.content.split('::')
  try:
      body = json.loads(body[-2])
  except (IndexError, ValueError):
      body = {}
  return body


def get_results(object_type, access_token, body):
  hubspot_endpoint = f"https://api.hubapi.com/crm/v3/objects/{object_type}/search"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"
  }
  response = requests.post(hubspot_endpoint, headers=headers, json=body)
  if response.status_code == 200:
      response_data = response.json()
      formated_data = response_data.get("results", [])
      return formated_data
  else:
      print(f"Error retrieving {object_type}: {response.status_code}")
      return "Error"
