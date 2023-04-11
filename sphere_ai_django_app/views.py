from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .postgres_helpers import *

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
def postgres_search(request):
  raw_query = request.GET.get('query')
  documentation = PostgresReference.objects.all().first().documentation
  table_names = fetch_table_names()
  tables_prompt = f'Process the documentation from "{documentation}" and table names from "{table_names}" to return the appropriate table names needed to process the query "{raw_query}". Add :: before the table name and dont add any additional information and tables'
  db_schema = fetch_tables_schema(parsed_table_names(tables_prompt))
  prompt = f'Your goal is to take this text: "{raw_query}" and suggest a Postgres query that will execute on a database with the following schema and answer their question: "{db_schema}". Explain your reasoning first, then include the complete query at the end of your response with :: before and after the query'
  gpt_query_response = ask_gpt(prompt)
  parsed_query = gpt_query_response.split('::')[1].split('::')[0]
  query_result = execute_query(parsed_query)
  response = [f"{row}\n" for row in query_result]
  return HttpResponse(response)
