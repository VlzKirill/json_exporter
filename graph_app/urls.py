from django.urls import path
from .views import GraphView

urlpatterns = [
    path('graph/', GraphView.as_view(), name='graph'),
]