

from django.urls import path, include
from . import views

urlpatterns = [
    path('recept/', views.recept, name='recept'),
]
