from user.models.document import Document
from user.utils.document_utility import document_object, get_matches
from rest_framework.response import Response
from rest_framework import generics, permissions


class BingSearchView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query')
        total_documents = Document.objects.count()
        results = []
        documents = Document.objects.select_related('company').all()
        for document in documents:
            matches = get_matches(document, query)
            if matches:
                document_data = document_object(document)
                document_data['matches'] = matches
                results.append(document_data)

        return Response({
            'result': [r for r in results if r],
            'total_documents': total_documents
        })
