from django.urls import path
from .views import index

urlpatterns = [
    path('metrics/', index, name='index'),
]