from django.http import HttpResponse
from user.models.hubspot_reference import HubspotReference
from rest_framework.decorators import api_view
from user.utils.hubspot_utility import hubspot_object_type, object_properties, get_filters_body, fetch_hubspot_object_results
import os
import hubspot
import openai


@api_view(['GET'])
def hubspot_search(request, id):
    query = request.GET.get('query')
    access_token = HubspotReference.objects.get(pk=id).hubspot_access_token
    openai.api_key = os.environ['OPENAI_API_KEY']
    api_client = hubspot.Client.create(access_token=access_token)
    question = f"from given query please identify which HubSpot object user is requesting data from. Just give me a one word response query: {query}."
    object_type = hubspot_object_type(question)
    properties = object_properties(api_client, object_type)
    operators = ["EQ", "NEQ", "LT", "LTE", "GT", "GTE", "BETWEEN", "IN", "NOT_IN",
                 "HAS_PROPERTY", "NOT_HAS_PROPERTY", "CONTAINS_TOKEN", "NOT_CONTAINS_TOKEN"]
    prompt = f"Please extract the filters from the user input: '{ query }' and create a HubSpot search API request body with filterGroups and filters based on the following available propertyNames: { properties } and the following available operators: { operators }. If the user input contains multiple filters with the AND operator, place all the filters within a single filterGroup. If the user input contains multiple filters with the OR operator, place each filter within its own filterGroup. Add :: before and after the json response and do not include the property names or anything in the body except json. The response should only the filters body in json format"
    body = get_filters_body(prompt)
    results = fetch_hubspot_object_results(object_type, access_token, body)
    return HttpResponse(results)
