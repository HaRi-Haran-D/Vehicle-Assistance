from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:pk>/review/', views.CreateReviewView.as_view(), name='create_review'),
    path('mechanic/reviews/', views.MechanicReviewsListView.as_view(), name='mechanic_reviews'),
]
