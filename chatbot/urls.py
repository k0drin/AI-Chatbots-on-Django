from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/", views.chatbot_view, name="chatbot"),
]
