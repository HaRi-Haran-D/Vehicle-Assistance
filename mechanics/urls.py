from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.MechanicDashboardView.as_view(), name='mechanic_dashboard'),
    path('profile/edit/', views.MechanicProfileUpdateView.as_view(), name='mechanic_profile_edit'),
    path('toggle-availability/', views.ToggleAvailabilityView.as_view(), name='toggle_availability'),
]
