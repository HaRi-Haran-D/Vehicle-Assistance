from django import forms
from .models import ServiceRequest, ServiceImage

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['vehicle', 'problem_category', 'problem_description', 'emergency_contact', 'preferred_mechanic', 'current_latitude', 'current_longitude']
        widgets = {
            'problem_description': forms.Textarea(attrs={'rows': 3}),
            'current_latitude': forms.HiddenInput(),
            'current_longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ServiceImageForm(forms.Form):
    images = MultipleFileField(required=False, widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}))
