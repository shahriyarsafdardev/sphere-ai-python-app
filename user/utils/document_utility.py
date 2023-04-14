
import re


def get_matches(document, query):
    query = re.sub('[^0-9A-Za-z ]', '', query).strip()
    regex = re.compile(query, re.IGNORECASE)
    matches = []

    if document and document.transcript:
        for page in document.transcript:
            page_matches = []
            text = page['text']
            words = re.split('[\s\n]+', text)

            for i in range(len(words)):
                if regex.match(' '.join(words[i:(i + len(query.split(' ')))])):
                    start_index = max(0, i - 50)
                    end_index = max(len(words) - 1, i +
                                    len(query.split(' ')) + 50)
                    context_words = words[start_index:end_index]
                    context = ' '.join(context_words).strip()
                    page_matches.append(context)

            if page_matches:
                matches.append({
                    'page_number': page['number'],
                    'page_matches': page_matches
                })

    return matches


def document_object(document):
    return {
        'id': document.id if document else None,
        'title': document.title if document else None,
        'url': document.url if document else None,
        'published_at': document.published_at if document else None,
        'company_name': document.company.name if document and document.company else None
    }
