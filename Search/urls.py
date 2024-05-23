from django.urls import path, include
from .views import index_view,search_view
urlpatterns = [
    # path('index/', index_view),
    path('search/', search_view),
]
