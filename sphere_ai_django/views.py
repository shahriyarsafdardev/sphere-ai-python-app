from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
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