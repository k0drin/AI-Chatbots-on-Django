from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path("api/v1/", views.chatbot_view, name="chatbot"),
]

