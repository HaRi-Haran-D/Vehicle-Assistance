from django.urls import path
from . import views

urlpatterns = [
    path('read/<int:pk>/', views.MarkAsReadView.as_view(), name='mark_notification_read'),
]
