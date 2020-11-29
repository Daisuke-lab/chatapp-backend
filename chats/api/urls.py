from django.urls import path, re_path

from .views import *


app_name='chat'


urlpatterns = [
    path('chat/<int:pk>/', get_chats),
    path('chat/create/', create_chat),
    path('chat/detail/<pk>/', ChatDetailView.as_view()),
    path('chat/update/<pk>/', ChatUpdateView.as_view()),
    path('chat/delete/<pk>/', ChatDeleteView.as_view()),
    path('contact/', ContactListView.as_view()),
    path('contact/create/', ContactCreateView.as_view()),
    path('contact/detail/<pk>/', get_contact),
    path('contact/update/<pk>/', add_friend),
    path('contact/delete/<pk>/', ContactDeleteView.as_view()),
]