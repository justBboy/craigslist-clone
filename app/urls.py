from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newsearch', views.new_search, name='app/new_search')
]