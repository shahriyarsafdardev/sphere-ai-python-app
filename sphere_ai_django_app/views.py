import os
import hubspot
import openai
from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .postgres_helpers import *
from .hubspot_helpers import *

@api_view(['GET'])
def postgres_references(request):
  data = PostgresReference.objects.all()
  response_data = PostgresReferenceSerializer(data, many=True).data
  return Response(response_data)

@api_view(['GET'])
def show_postgres_reference(request, *args, **kwargs):
  reference = PostgresReference.objects.get(id=kwargs['reference_id'])
  return Response(PostgresReferenceSerializer(reference).data)

@api_view(['GET'])
def hubspot_references(request):
  data = HubspotReference.objects.all()
  response_data = HubspotReferenceSerializer(data, many=True).data
  return Response(response_data)

@api_view(['GET'])
def show_hubspot_reference(request, *args, **kwargs):
  reference = HubspotReference.objects.get(id=kwargs['reference_id'])
  return Response(HubspotReferenceSerializer(reference).data)

@api_view(['GET'])
def postgres_search(request, id):
  raw_query = request.GET.get('query')
  postgres_reference = PostgresReference.objects.get(pk=id)
  table_names = fetch_table_names(id)
  tables_prompt = f'Process the documentation from "{postgres_reference.documentation}" and table names from "{table_names}" to return the appropriate table names needed to process the query "{raw_query}". Add :: before the table name and dont add any additional information and tables'
  db_schema = fetch_tables_schema(id, parsed_table_names(tables_prompt))
  prompt = f'Your goal is to take this text: "{raw_query}" and suggest a Postgres query that will execute on a database with the following schema and answer their question: "{db_schema}". Explain your reasoning first, then include the complete query at the end of your response with :: before and after the query'
  gpt_query_response = ask_gpt(prompt)
  parsed_query = gpt_query_response.split('::')[1].split('::')[0]
  query_result = execute_query(id, parsed_query)
  response = [f"{row}\n" for row in query_result]
  return HttpResponse(response)

@api_view(['GET'])
def hubspot_search(request, id):
  query = request.GET.get('query')
  access_token = HubspotReference.objects.get(pk=id).hubspot_access_token
  openai.api_key = os.environ['OPENAI_API_KEY']
  api_client = hubspot.Client.create(access_token=access_token)
  question = f"from given query please identify which HubSpot object user is requesting data from. Just give me a one word response query: {query}."
  object_type = get_object_type(question)
  properties = get_properties(api_client, object_type)
  operators = ["EQ", "NEQ", "LT", "LTE", "GT", "GTE", "BETWEEN", "IN", "NOT_IN",
                "HAS_PROPERTY", "NOT_HAS_PROPERTY", "CONTAINS_TOKEN", "NOT_CONTAINS_TOKEN"]
  prompt = f"Please extract the filters from the user input: '{ query }' and create a HubSpot search API request body with filterGroups and filters based on the following available propertyNames: { properties } and the following available operators: { operators }. If the user input contains multiple filters with the AND operator, place all the filters within a single filterGroup. If the user input contains multiple filters with the OR operator, place each filter within its own filterGroup. Add :: before and after the json response and do not include the property names or anything in the body except json. The response should only the filters body in json format"
  body = get_body(prompt)
  results = get_results(object_type, access_token, body)
  return HttpResponse(results)
