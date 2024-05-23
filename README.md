# Information Retrieval: Local Search Engine using Indexing Algorithms

The search engine will be built using Python and Django, and it will utilize various indexing algorithms to provide efficient and accurate search results.

## Indexing Algorithms

The search engine will support three indexing algorithms: Boolean, Extended Boolean, and Vector Space Model.

### Boolean Model

*The Boolean model is the simplest indexing algorithm. It treats each document as a set of keywords and performs a set intersection operation to find documents that contain all the query keywords. The algorithm does not consider the frequency or proximity of keywords in the document.*

### Extended Boolean Model

*The Extended Boolean model is an extension of the Boolean model that considers the frequency of keywords in the document. It assigns a weight to each keyword based on its frequency and uses this weight to rank the documents. The algorithm also supports logical operators such as AND, OR, and NOT.*

### Vector Space Model

*The Vector Space Model (VSM) is a more advanced indexing algorithm that represents documents and queries as vectors in a high-dimensional space. The algorithm computes the cosine similarity between the query vector and the document vectors to rank the documents. The VSM algorithm considers the frequency and proximity of keywords in the document.*

## Implementation

The search engine will be implemented using Django, a Python web framework. The engine will consist of the following components:

### Models

The search engine will use two models: Index and Document. The Index model will store the index entries for each document and keyword, while the Document model will store the document content and metadata.

### Views

The search engine will have a single view that will handle the search requests. The view will take the search query and the indexing algorithm as input and return the search results as a JSON response.

### Algorithms

The search engine will implement the three indexing algorithms as separate functions. The boolean_search function will implement the Boolean model, the extended_boolean_search function will implement the Extended Boolean model, and the vector_search function will implement the Vector Space Model.

### Utilities

The search engine will also include several utility functions, such as highlight_terms and extract_relevant_paragraphs. The highlight_terms function will highlight the search terms in the document content, while the extract_relevant_paragraphs function will extract the paragraphs that contain the search terms.

~ NOTE: this demo is based on my documents.
[DEMO](https://irlsengine.pythonanywhere.com/)
