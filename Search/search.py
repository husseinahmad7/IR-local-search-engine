from .models import Index, Document
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re

def highlight_terms(text, terms):
    for term in terms:
        text = re.sub(f"(?i)({term})", r'<span style="background-color: yellow">\1</span>', text)
    return text

def extract_relevant_paragraphs(document, terms):
    paragraphs = document.content.split('\n')
    relevant_paragraphs = []

    for para in paragraphs:
        if any(term.lower() in para.lower() for term in terms):
            highlighted_para = highlight_terms(para, terms)
            relevant_paragraphs.append(highlighted_para)

    return relevant_paragraphs

def perform_search(query, algorithm):
    if algorithm == 'boolean':
        results = boolean_search(query)
    elif algorithm == 'extended_boolean':
        results = extended_boolean_search(query)
    elif algorithm == 'vector':
        results = vector_search(query)
    return results

# def boolean_search(query):
#     terms = query.split()
#     documents = Document.objects.filter(index__term__in=terms).distinct()
#     return documents
def boolean_search(query):
    # terms = query.lower().split()
    terms = query.split()

    index_entries = Index.objects.filter(term__in=terms, algorithm='boolean').select_related('document')
    
    document_scores = {}
    for entry in index_entries:
        if entry.document_id not in document_scores:
            document_scores[entry.document_id] = 0
        document_scores[entry.document_id] += entry.weight

    results = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    
    documents = []
    for doc_id, score in results:
        document = Document.objects.get(id=doc_id)
        relevant_paragraphs = extract_relevant_paragraphs(document, terms)
        documents.append({'document': document, 'score': score, 'paragraphs': relevant_paragraphs})

    return documents

def extended_boolean_search(query, p=2):
    terms = query.split()  # Simple tokenization TODO lower
    index_entries = Index.objects.filter(term__in=terms, algorithm='extended_boolean').select_related('document')

    document_scores = {}
    for term in terms:
        term_entries = index_entries.filter(term=term)
        for entry in term_entries:
            doc_id = entry.document_id
            if doc_id not in document_scores:
                document_scores[doc_id] = 0
            document_scores[doc_id] += pow(entry.frequency, p)

    # Normalize scores by the number of terms and take the p-th root
    for doc_id in document_scores:
        document_scores[doc_id] = pow(document_scores[doc_id], 1/p)

    # Order documents by score
    results = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    # Fetch the documents
    documents = []
    for doc_id, score in results:
        document = Document.objects.get(id=doc_id)
        relevant_paragraphs = extract_relevant_paragraphs(document, terms)

        documents.append({'document': document, 'score': score, 'paragraphs': relevant_paragraphs})

    return documents


def vector_search(query):
    terms = query.split()

    # Retrieve all documents and their contents
    docs = Document.objects.all()
    doc_contents = [doc.content for doc in docs]
    doc_ids = [doc.id for doc in docs]

    # Vectorize the documents and the query
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(doc_contents)
    query_vector = vectorizer.transform([query])

    # Compute cosine similarity between the query and the documents
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()

    # Pair document ids with their similarity scores and sort by score
    doc_sim_pairs = sorted(zip(doc_ids, similarities), key=lambda x: x[1], reverse=True)

    # Retrieve the documents ordered by similarity score and add relevant paragraphs
    results = []
    for doc_id, score in doc_sim_pairs:
        if score > 0.0:
            document = Document.objects.get(id=doc_id)
            relevant_paragraphs = extract_relevant_paragraphs(document, terms)
            results.append({'document': document, 'score': score, 'paragraphs': relevant_paragraphs})

    return results

# def vector_search(query):
#     # Retrieve all documents and their contents
#     docs = Document.objects.all()
#     doc_contents = [doc.content for doc in docs]
#     doc_ids = [doc.id for doc in docs]

#     # Vectorize the documents and the query
#     vectorizer = TfidfVectorizer()
#     doc_vectors = vectorizer.fit_transform(doc_contents)
#     query_vector = vectorizer.transform([query])

#     # Compute cosine similarity between the query and the documents
#     similarities = cosine_similarity(query_vector, doc_vectors).flatten()

#     # Pair document ids with their similarity scores and sort by score
#     doc_sim_pairs = sorted(zip(doc_ids, similarities), key=lambda x: x[1], reverse=True)

#     # Retrieve the documents ordered by similarity score
#     results = [{'document': Document.objects.get(id=doc_id), 'score': score} for doc_id, score in doc_sim_pairs]

#     return results