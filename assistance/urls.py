from django.urls import path
from . import views

urlpatterns = [
    path('customer/requests/', views.CustomerRequestListView.as_view(), name='customer_requests'),
    path('request/new/', views.CreateRequestView.as_view(), name='create_request'),
    path('request/<int:pk>/', views.RequestDetailView.as_view(), name='request_detail'),
    path('mechanic/jobs/', views.MechanicJobListView.as_view(), name='mechanic_jobs'),
    path('request/<int:pk>/accept/', views.AcceptJobView.as_view(), name='accept_job'),
    path('request/<int:pk>/status/', views.UpdateJobStatusView.as_view(), name='update_job_status'),
]
