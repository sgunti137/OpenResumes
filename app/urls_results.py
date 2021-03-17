from django.urls import path
from app import views

urlpatterns = [
    path('',views.results, name = 'results'),
]