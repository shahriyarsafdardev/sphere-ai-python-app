from user.models.postgres_reference import PostgresReference
from user.utils.postgres_utility import fetch_tables_schema, ask_gpt, execute_query
from user.serializers.postgres_reference_serializer import PostgresReferenceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework import status, generics, permissions


class PostgresReferencesView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = PostgresReference.objects.all()
        response_data = PostgresReferenceSerializer(data, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)


class PostgresSearchView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(request, id):
        try:
            raw_query = request.GET.get('query')
            db_schema = fetch_tables_schema(id, raw_query)
            prompt = f'Your goal is to take this text: "{raw_query}" and suggest a Postgres query that will execute on a database with the following schema and answer their question: "{db_schema}". Explain your reasoning first, then include the complete query at the end of your response with :: before and after the query'
            gpt_query_response = ask_gpt(prompt)
            parsed_query = gpt_query_response.split('::')[1].split('::')[0]
            query_result = execute_query(id, parsed_query)
            return Response(query_result)
        except:
            return Response({'message': 'Unable to process your query'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
