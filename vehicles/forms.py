from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'brand', 'model_name', 'registration_number', 'fuel_type', 'insurance_expiry', 'puc_expiry']
        widgets = {
            'insurance_expiry': forms.DateInput(attrs={'type': 'date'}),
            'puc_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
