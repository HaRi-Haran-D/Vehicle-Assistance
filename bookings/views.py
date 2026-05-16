from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ServiceRequest
from mechanics.models import MechanicProfile
from .forms import ServiceRequestForm

@login_required
def customer_dashboard(request):
    if request.user.role != 'CUSTOMER':
        return redirect('mechanic_dashboard')
    
    # Get active request
    active_request = ServiceRequest.objects.filter(
        customer=request.user
    ).exclude(status__in=['COMPLETED', 'CANCELLED']).first()

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid() and not active_request:
            service_req = form.save(commit=False)
            service_req.customer = request.user
            service_req.save()
            return redirect('customer_dashboard')
    else:
        form = ServiceRequestForm()

    past_requests = ServiceRequest.objects.filter(customer=request.user, status__in=['COMPLETED', 'CANCELLED']).order_by('-created_at')

    context = {
        'active_request': active_request,
        'past_requests': past_requests,
        'form': form
    }
    return render(request, 'bookings/customer_dashboard.html', context)

@login_required
def mechanic_dashboard(request):
    if request.user.role != 'MECHANIC':
        return redirect('customer_dashboard')
    
    try:
        profile = request.user.mechanic_profile
    except MechanicProfile.DoesNotExist:
        profile = MechanicProfile.objects.create(user=request.user)
    
    active_job = ServiceRequest.objects.filter(
        mechanic=request.user
    ).exclude(status__in=['COMPLETED', 'CANCELLED']).first()

    available_requests = ServiceRequest.objects.filter(
        status='REQUESTED',
        mechanic__isnull=True
    ).order_by('-created_at')

    past_jobs = ServiceRequest.objects.filter(
        mechanic=request.user, 
        status__in=['COMPLETED', 'CANCELLED']
    ).order_by('-created_at')[:5]

    if request.method == 'POST':
        if 'toggle_availability' in request.POST:
            profile.is_available = not profile.is_available
            profile.save()
            return redirect('mechanic_dashboard')

    context = {
        'profile': profile,
        'active_job': active_job,
        'available_requests': available_requests,
        'available_count': available_requests.count(),
        'past_jobs': past_jobs
    }
    return render(request, 'bookings/mechanic_dashboard.html', context)

@login_required
def accept_request(request, pk):
    if request.method == 'POST' and request.user.role == 'MECHANIC':
        req = get_object_or_404(ServiceRequest, id=pk, mechanic__isnull=True)
        req.mechanic = request.user
        req.status = 'ACCEPTED'
        req.save()
    return redirect('mechanic_dashboard')

@login_required
def update_status(request, pk):
    if request.method == 'POST' and request.user.role == 'MECHANIC':
        req = get_object_or_404(ServiceRequest, id=pk, mechanic=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(ServiceRequest.STATUS_CHOICES):
            req.status = new_status
            req.save()
    return redirect('mechanic_dashboard')

@login_required
def api_get_status(request, pk):
    req = get_object_or_404(ServiceRequest, id=pk)
    if request.user == req.customer or request.user == req.mechanic:
        data = {
            'status': req.status,
            'status_display': req.get_status_display()
        }
        if req.mechanic and hasattr(req.mechanic, 'mechanic_profile'):
            profile = req.mechanic.mechanic_profile
            data.update({
                'mechanic_lat': float(profile.current_latitude) if profile.current_latitude else None,
                'mechanic_lon': float(profile.current_longitude) if profile.current_longitude else None,
                'mechanic_name': req.mechanic.username
            })
        return JsonResponse(data)
@login_required
def work_records(request):
    if request.user.role == 'CUSTOMER':
        records = ServiceRequest.objects.filter(customer=request.user).order_by('-created_at')
        title = "My Service History"
    else:
        records = ServiceRequest.objects.filter(mechanic=request.user).order_by('-created_at')
        title = "My Work Records"
    
    context = {
        'records': records,
        'title': title
    }
    return render(request, 'bookings/work_records.html', context)

@login_required
def update_mechanic_location(request):
    if request.method == 'POST' and request.user.role == 'MECHANIC':
        import json
        from mechanics.models import MechanicProfile
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')
        if lat and lon:
            profile, _ = MechanicProfile.objects.get_or_create(user=request.user)
            profile.current_latitude = lat
            profile.current_longitude = lon
            profile.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
