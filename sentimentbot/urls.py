from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin URL
    path("admin/", admin.site.urls),

    # Application URLs
    path("chatbot/", include("chatbot.urls")),
    path("chatgpt/", include("chatgpt.urls")),
    # path("llama", include("llama.urls"))
]
