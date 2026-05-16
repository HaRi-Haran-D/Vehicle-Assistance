from django.urls import path
from . import views

urlpatterns = [
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('mechanic/dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('booking/accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('booking/update/<int:pk>/', views.update_status, name='update_status'),
    path('booking/api/status/<int:pk>/', views.api_get_status, name='api_get_status'),
    path('mechanic/api/update-location/', views.update_mechanic_location, name='update_mechanic_location'),
    path('work-records/', views.work_records, name='work_records'),
]
