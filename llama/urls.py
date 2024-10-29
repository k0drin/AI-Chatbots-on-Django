from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/", views.llama_view, name="llama-chat"),
]


