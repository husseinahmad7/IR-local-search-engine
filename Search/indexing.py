import os
import docx
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from .models import Document, Index

def parse_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def index_documents(directory, language):
    documents = []
    for filename in os.listdir(directory):
        if filename.startswith('M'):
            language = 'en'
        else:
            language = 'ar'
        if filename.endswith(".docx"):
            file_path = os.path.join(directory, filename)
            try:
                content = parse_docx(file_path)
                documents.append((filename, content, language))
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

    algorithms = {
        'boolean': CountVectorizer(binary=True),
        'extended_boolean': CountVectorizer(),
        'vector': TfidfVectorizer(),
    }

    contents = [doc[1] for doc in documents]
    
    for algorithm_name, vectorizer in algorithms.items():
        X = vectorizer.fit_transform(contents)
        terms = vectorizer.get_feature_names_out()

        index_entries = []
        for idx, (filename, content, language) in enumerate(documents):
            doc, created = Document.objects.get_or_create(title=filename, defaults={'content': content, 'language': language})
            if not created:
                doc.content = content
                doc.language = language
                doc.save()

            frequencies = X[idx].toarray()[0]

            for term, freq in zip(terms, frequencies):
                if freq > 0:  # Only index terms that are present in the document
                    if algorithm_name == 'boolean':
                        weight = 1  # Boolean model assigns a weight of 1 for presence
                    elif algorithm_name == 'extended_boolean':
                        weight = freq  # Extended boolean model uses term frequency
                    elif algorithm_name == 'vector':
                        weight = freq  # Vector model uses TF-IDF weight

                    index_entries.append(Index(term=term, document=doc, frequency=int(freq), weight=weight, algorithm=algorithm_name))

        # Use bulk_create to insert all index entries at once
        Index.objects.bulk_create(index_entries, batch_size=1000)




# def index_documents(directory, language, algorithm):
#     algorithms = [('boolean',CountVectorizer(binary=True)),('extended_boolean',CountVectorizer()),('vector',TfidfVectorizer())]

#     index_list = []
#     for filename in os.listdir(directory):
#         if filename.startswith('M'):
#             language = 'en'
#         else:
#             language = 'ar'
#         if filename.endswith(".docx"):
#             file_path = os.path.join(directory, filename)
#             content = parse_docx(file_path)
#             if content:
                 
#                 doc = Document.objects.create(title=filename, content=content, language=language)
                
#                 # if algorithm == 'boolean':
#                 #     vectorizer = CountVectorizer(binary=True)
#                 # elif algorithm == 'extended_boolean':
#                 #     vectorizer = CountVectorizer()
#                 # elif algorithm == 'vector':
#                 #     vectorizer = TfidfVectorizer()
#                 for algorithm, vectorizer in algorithms:
#                     X = vectorizer.fit_transform([content])
#                     terms = vectorizer.get_feature_names_out()
#                     frequencies = X.toarray()[0]
                    
#                     for term, freq in zip(terms, frequencies):
#                             index_list.append(Index(term=term, document=doc, frequency=freq, weight=freq if algorithm != 'vector' else freq))
#                     # Batch create Index objects for the current algorithm
#                     Index.objects.bulk_create(index_list)
#                     index_list.clear()
