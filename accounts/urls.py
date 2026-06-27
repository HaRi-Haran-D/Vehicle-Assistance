from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
