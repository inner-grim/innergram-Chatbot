# chatbot_api/urls.py
from django.urls import path
from .views import ChatbotAPIView
# from .views import chatbot_response

urlpatterns = [
    path('get-response/', ChatbotAPIView.as_view(), name='chatbot-response'),
]