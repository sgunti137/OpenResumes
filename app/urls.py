from django.urls import path, include
from django.contrib import admin
from app import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('index/<str:pk>/', views.index, name = 'index'),
    path('admin/', admin.site.urls),
    path('results/<str:pk>/', views.results, name = 'results'),
]
