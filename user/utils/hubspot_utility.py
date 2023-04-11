import openai
import json
import requests


def hubspot_object_type(query):
    question = f"from given query please identify which HubSpot object user is requesting data from. Just give me a one word response query: {query}."
    response = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[{'role': 'user', 'content': question}],
      temperature=0.5
    )
    object_type = response.choices[0].message.content.strip()
    if object_type.endswith('.'):
        object_type = object_type[:-1]

    return object_type


def object_properties(api_client, object_type):
    properties = api_client.crm.properties.core_api.get_all(
        object_type=object_type, archived=False)
    return list(map(lambda result: result.name, properties.results))


def get_filters_body(query, properties):
    operators = ["EQ", "NEQ", "LT", "LTE", "GT", "GTE", "BETWEEN", "IN", "NOT_IN",
                 "HAS_PROPERTY", "NOT_HAS_PROPERTY", "CONTAINS_TOKEN", "NOT_CONTAINS_TOKEN"]
    prompt = f"Please extract the filters from the user input: '{ query }' and create a HubSpot search API request body with filterGroups and filters based on the following available propertyNames: { properties } and the following available operators: { operators }. If the user input contains multiple filters with the AND operator, place all the filters within a single filterGroup. If the user input contains multiple filters with the OR operator, place each filter within its own filterGroup. Add :: before and after the json response and do not include the property names or anything in the body except json. The response should only the filters body in json format"
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


def fetch_hubspot_object_results(object_type, access_token, body):
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
