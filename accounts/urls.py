from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # Customer Auth
    path('customer/login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('customer/register/', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('customer/dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    
    # Mechanic Auth
    path('mechanic/login/', views.MechanicLoginView.as_view(), name='mechanic_login'),
    path('mechanic/register/', views.MechanicRegisterView.as_view(), name='mechanic_register'),
    
    # Generic
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
