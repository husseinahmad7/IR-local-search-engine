from django.shortcuts import render
from .forms import IndexingForm, SearchForm
# from .models import Document, Index
from .indexing import index_documents
from .search import perform_search

def index_view(request):
    if request.method == 'POST':
        form = IndexingForm(request.POST)
        if form.is_valid():
            # directory = form.cleaned_data['directory']
            directory = 'D:\S.V.U\SIR\IR-local-search-engine\Data'
            language = form.cleaned_data['language']
            
            index_documents(directory, language)
    else:
        form = IndexingForm()
    return render(request, 'Search\index.html', {'form': form})

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            algorithm = form.cleaned_data['algorithm']
            # Implement search logic based on the algorithm
            results = perform_search(query, algorithm)
            return render(request, r'Search\results.html', {'results': results,'algorithm':algorithm})
    else:
        form = SearchForm()
    return render(request, 'Search\search.html', {'form': form})
