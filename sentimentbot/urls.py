# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from chatbot.views import home_view

urlpatterns = [
    # Admin URL
    path("admin/", admin.site.urls),

    path('', home_view, name='home'),


    # JWT URLs
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Application URLs
    path("chatbot/", include("chatbot.urls")),
    path("chatgpt/", include("chatgpt.urls")),
    path("llama/", include("llama.urls"))
]
