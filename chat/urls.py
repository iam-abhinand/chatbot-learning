from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path("rag-chat/", views.rag_chat_view, name="rag-chat"),
]