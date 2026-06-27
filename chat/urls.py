from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/send/', views.SendMessageView.as_view(), name='send_message'),
    path('<int:pk>/fetch/', views.GetMessagesView.as_view(), name='fetch_messages'),
]
