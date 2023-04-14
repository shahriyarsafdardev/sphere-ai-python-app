from user.models.hubspot_reference import HubspotReference
from user.utils.hubspot_utility import hubspot_object_type, object_properties, get_filters_body, fetch_hubspot_object_results
from user.serializers.hubspot_reference_serializer import HubspotReferenceSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
import hubspot
import openai
import os


class HubspotReferencesView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = HubspotReference.objects.all()
        response_data = HubspotReferenceSerializer(data, many=True).data
        return Response(response_data)


class HubspotSearchView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(request, id):
        try:
            query = request.GET.get('query')
            access_token = HubspotReference.objects.get(
                pk=id).hubspot_access_token
            openai.api_key = os.environ['OPENAI_API_KEY']
            api_client = hubspot.Client.create(access_token=access_token)
            object_type = hubspot_object_type(query)
            properties = object_properties(api_client, object_type)
            body = get_filters_body(query, properties)
            results = fetch_hubspot_object_results(
                object_type, access_token, body)
            result_properties = [res['properties'] for res in results]
            return Response(result_properties)
        except:
            return Response({'message': 'Unable to process your query'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
