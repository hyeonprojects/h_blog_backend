from django.urls import path, include
from . import views

urlpatterns = [
    path('posts', views.post),
    path('posts/<str:id>', views.post_detail),
]