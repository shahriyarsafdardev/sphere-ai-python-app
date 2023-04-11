from django.http import HttpResponse
from user.models.hubspot_reference import HubspotReference
from rest_framework.decorators import api_view
from user.utils.hubspot_utility import hubspot_object_type, object_properties, get_filters_body, fetch_hubspot_object_results
import os
import hubspot
import openai
from user.serializers.hubspot_reference_serializer import HubspotReferenceSerializer
from rest_framework.response import Response


@api_view(['GET'])
def hubspot_references(request):
    data = HubspotReference.objects.all()
    response_data = HubspotReferenceSerializer(data, many=True).data
    return Response(response_data)


@api_view(['GET'])
def hubspot_search(request, id):
    query = request.GET.get('query')
    access_token = HubspotReference.objects.get(pk=id).hubspot_access_token
    openai.api_key = os.environ['OPENAI_API_KEY']
    api_client = hubspot.Client.create(access_token=access_token)
    object_type = hubspot_object_type(query)
    properties = object_properties(api_client, object_type)
    body = get_filters_body(query, properties)
    results = fetch_hubspot_object_results(object_type, access_token, body)
    return HttpResponse(results)
