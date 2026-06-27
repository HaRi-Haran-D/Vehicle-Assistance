from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import User, CustomerProfile
from .forms import CustomerRegistrationForm, MechanicRegistrationForm, UserProfileForm, CustomerProfileForm
from mechanics.models import MechanicProfile

class CustomerLoginView(LoginView):
    template_name = 'auth/customer_login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.is_mechanic():
            messages.error(self.request, "This account is registered as a Mechanic. Please login through the Mechanic Portal.")
            return redirect('customer_login')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('customer_dashboard')

class MechanicLoginView(LoginView):
    template_name = 'auth/mechanic_login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.is_customer():
            messages.error(self.request, "This account is registered as a Customer. Please login through the Customer Portal.")
            return redirect('mechanic_login')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('mechanic_dashboard')

class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'auth/customer_register.html'

    def get_success_url(self):
        return reverse_lazy('customer_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Customer Registration successful.')
        return response

class MechanicRegisterView(CreateView):
    model = User
    form_class = MechanicRegistrationForm
    template_name = 'auth/mechanic_register.html'

    def get_success_url(self):
        return reverse_lazy('mechanic_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Mechanic Registration successful.')
        return response

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/dashboard.html'
    # Fallback to the base layout or create a new template if needed.
    # Currently just rendering a placeholder or the actual customer dashboard.

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer() and not request.user.is_admin():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
        context['completed_repairs'] = ServiceRequest.objects.filter(status='COMPLETED').count()
        return context

def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_mechanic():
            return redirect('mechanic_dashboard')
        if request.user.is_admin():
            return redirect('admin_dashboard')
        return redirect('customer_dashboard')
    return render(request, 'landing.html')
