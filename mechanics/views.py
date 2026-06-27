from django.views.generic import TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import MechanicProfile

class MechanicDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mechanics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context like pending jobs, completed jobs etc. later
        return context

class MechanicProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MechanicProfile
    template_name = 'mechanics/profile_form.html'
    fields = ['vehicle_types_supported', 'skills', 'experience_years', 'documents']
    success_url = reverse_lazy('mechanic_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.mechanic_profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

class ToggleAvailabilityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        profile = request.user.mechanic_profile
        profile.is_available = not profile.is_available
        profile.save()
        status = "Online" if profile.is_available else "Offline"
        messages.success(request, f"You are now {status}.")
        return redirect('mechanic_dashboard')
