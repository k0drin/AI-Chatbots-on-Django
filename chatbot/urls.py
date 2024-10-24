from django.urls import path
from .views import chatbot_view, chatgpt_view

urlpatterns = [
    # Home page
    path('', chatbot_view, name='chatbot'),
    # GPT chat page
    path('chatgpt/', chatgpt_view, name='chatgpt'),
]

