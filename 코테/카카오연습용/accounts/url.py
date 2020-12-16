from django.urls import path, include
from .views import Hello
urlpatterns = [
    path('', Hello),
]

