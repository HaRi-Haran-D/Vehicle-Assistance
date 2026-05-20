from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import CustomUserCreationForm
from mechanics.models import MechanicProfile

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_mechanic():
                return redirect('mechanic_dashboard')
            return redirect('customer_dashboard')
    else:
        form = AuthenticationForm()
        # Add Tailwind classes dynamically
        for field in form.fields.values():
            field.widget.attrs['class'] = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm p-2 border'
            
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_mechanic():
                MechanicProfile.objects.create(user=user)
            login(request, user)
            if user.is_mechanic():
                return redirect('mechanic_dashboard')
            return redirect('customer_dashboard')
    else:
        form = CustomUserCreationForm()
        for field in form.fields.values():
            field.widget.attrs['class'] = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm p-2 border'
            
    return render(request, 'accounts/register.html', {'form': form})

def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_mechanic():
            return redirect('mechanic_dashboard')
        return redirect('customer_dashboard')
    return render(request, 'landing.html')
