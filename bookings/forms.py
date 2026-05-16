from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['issue_type', 'description', 'image', 'user_latitude', 'user_longitude']
        widgets = {
            'user_latitude': forms.HiddenInput(attrs={'id': 'user_lat'}),
            'user_longitude': forms.HiddenInput(attrs={'id': 'user_lon'}),
            'issue_type': forms.Select(choices=[
                ('FLAT_TIRE', 'Flat Tire'),
                ('BATTERY', 'Dead Battery'),
                ('ENGINE', 'Engine Issue'),
                ('TOWING', 'Towing Required'),
                ('OTHER', 'Other'),
                ], attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm p-2 border'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm p-2 border', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-secondary'}),
        }
