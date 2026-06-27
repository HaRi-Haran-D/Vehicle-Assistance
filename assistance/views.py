from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import ServiceRequest, ServiceImage, StatusUpdate, RepairDetails
from .forms import ServiceRequestForm, ServiceImageForm

class CustomerRequestListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'assistance/customer_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user).order_by('-created_at')

class RequestDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'assistance/request_detail.html'
    context_object_name = 'service_request'

class CreateRequestView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'assistance/create_request.html'
    success_url = reverse_lazy('customer_requests')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_form'] = ServiceImageForm(self.request.POST, self.request.FILES)
        else:
            data['image_form'] = ServiceImageForm()
        # Restrict vehicle dropdown to user's vehicles
        data['form'].fields['vehicle'].queryset = self.request.user.vehicles.all()
        # Restrict mechanic dropdown to verified available mechanics
        from mechanics.models import MechanicProfile
        # We need a proper way to query users who are mechanics and available.
        # For simplicity, assuming any mechanic in the system can be preferred.
        from accounts.models import User
        data['form'].fields['preferred_mechanic'].queryset = User.objects.filter(role='MECHANIC')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        if image_form.is_valid():
            form.instance.customer = self.request.user
            self.object = form.save()
            
            images = self.request.FILES.getlist('images')
            for image in images:
                ServiceImage.objects.create(service_request=self.object, image=image, image_type='PROBLEM')
            
            messages.success(self.request, 'Assistance requested successfully.')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class MechanicJobListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'assistance/mechanic_job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        # Show jobs assigned to this mechanic OR requested jobs without an assigned mechanic (pool)
        user = self.request.user
        return ServiceRequest.objects.filter(
            models.Q(mechanic=user) | 
            models.Q(mechanic__isnull=True, status='REQUESTED')
        ).order_by('-created_at')
        
from django.db import models

class AcceptJobView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        if service_request.status == 'REQUESTED' and service_request.mechanic is None:
            service_request.mechanic = request.user
            service_request.status = 'ACCEPTED'
            service_request.save()
            messages.success(request, 'Job accepted successfully.')
        else:
            messages.error(request, 'Job is no longer available.')
        return redirect('job_detail', pk=pk)

class UpdateJobStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        if service_request.mechanic == request.user:
            new_status = request.POST.get('status')
            if new_status in dict(ServiceRequest.STATUS_CHOICES):
                service_request.status = new_status
                service_request.save()
                messages.success(request, f'Status updated to {new_status}.')
        return redirect('job_detail', pk=pk)
