from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Application URLs
    path("", include("chatbot.urls")),
]
