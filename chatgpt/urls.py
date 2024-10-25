from django.urls import path
from . import views 

urlpatterns = [
        path("api/v1/", views.chatgpt_view, name="chatgpt")
]
