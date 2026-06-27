from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from assistance.models import ServiceRequest

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_review.html'
    
    def get_success_url(self):
        return reverse_lazy('request_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_request'] = get_object_or_404(ServiceRequest, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        service_request = get_object_or_404(ServiceRequest, pk=self.kwargs['pk'])
        
        # Ensure user hasn't already reviewed this request
        if hasattr(service_request, 'review'):
            messages.error(self.request, 'You have already reviewed this request.')
            return redirect(self.get_success_url())
            
        form.instance.service_request = service_request
        form.instance.customer = self.request.user
        form.instance.mechanic = service_request.mechanic
        
        messages.success(self.request, 'Thank you for your review!')
        return super().form_valid(form)

class MechanicReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/mechanic_reviews.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        return Review.objects.filter(mechanic=self.request.user).order_by('-created_at')
