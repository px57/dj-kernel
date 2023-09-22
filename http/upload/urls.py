


from django.urls import path, include
from . import views

urlpatterns = [
    path('avatar/', views.avatar, name='avatar'),
    path('video/', views.video, name='video'),
    path('for_order/', views.for_order, name='for_order'),
]
