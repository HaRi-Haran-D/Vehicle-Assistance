from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import User, CustomerProfile
from .forms import CustomUserCreationForm, UserProfileForm, CustomerProfileForm
from mechanics.models import MechanicProfile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('admin_dashboard')
        elif user.is_mechanic():
            return reverse_lazy('mechanic_dashboard')
        return reverse_lazy('customer_dashboard')

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        user = self.object
        if user.is_mechanic():
            return reverse_lazy('mechanic_dashboard')
        return reverse_lazy('customer_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        if user.is_mechanic():
            MechanicProfile.objects.create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Registration successful.')
        return response

class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'u_form' not in context:
            context['u_form'] = UserProfileForm(instance=self.request.user)
        
        if self.request.user.is_customer():
            if 'p_form' not in context:
                context['p_form'] = CustomerProfileForm(instance=self.request.user.customer_profile)
        
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserProfileForm(request.POST, instance=request.user)
        
        if request.user.is_customer():
            p_form = CustomerProfileForm(request.POST, request.FILES, instance=request.user.customer_profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('edit_profile')
        else:
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('edit_profile')
                
        context = self.get_context_data(u_form=u_form)
        if request.user.is_customer():
            context['p_form'] = p_form
        return self.render_to_response(context)

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_admin():
            return context # Need better permission handling later
        
        from mechanics.models import MechanicProfile
        from assistance.models import ServiceRequest
        from accounts.models import User
        from django.db.models import Sum
        
        context['total_users'] = User.objects.filter(role='CUSTOMER').count()
        context['total_mechanics'] = User.objects.filter(role='MECHANIC').count()
        context['online_mechanics'] = MechanicProfile.objects.filter(is_available=True).count()
        context['pending_requests'] = ServiceRequest.objects.filter(status='REQUESTED').count()
        context['completed_repairs'] = ServiceRequest.objects.filter(status='COMPLETED').count() # Or PAID
        # Just simple stats for now to pass context to chart.js
        return context

def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_mechanic():
            return redirect('mechanic_dashboard')
        if request.user.is_admin():
            return redirect('admin_dashboard')
        return redirect('customer_dashboard')
    return render(request, 'landing.html')
