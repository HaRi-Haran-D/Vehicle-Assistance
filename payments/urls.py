from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('<int:pk>/invoice/', views.GenerateInvoiceView.as_view(), name='generate_invoice'),
]
