from django.urls import path
from django.http import HttpResponse

from .views import index

urlpatterns =[
    path('', index)
]
