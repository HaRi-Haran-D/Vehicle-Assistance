from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, CustomerProfile
from mechanics.models import MechanicProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'role', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class BaseRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=15)
    terms = forms.BooleanField(required=True, label="Accept Terms")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with that phone number already exists.")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if type(field.widget) != forms.CheckboxInput:
                field.widget.attrs['class'] = 'form-control'

class CustomerRegistrationForm(BaseRegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CUSTOMER'
        if commit:
            user.save()
            # CustomerProfile is created via signals in accounts/signals.py
        return user

class MechanicRegistrationForm(BaseRegistrationForm):
    garage_name = forms.CharField(required=True)
    owner_name = forms.CharField(required=True)
    experience_years = forms.IntegerField(required=True)
    specialization = forms.CharField(required=True)
    workshop_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=True)
    profile_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if type(field.widget) != forms.CheckboxInput:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'MECHANIC'
        if self.cleaned_data.get('profile_image'):
            user.profile_image = self.cleaned_data.get('profile_image')
        if commit:
            user.save()
            MechanicProfile.objects.create(
                user=user,
                garage_name=self.cleaned_data.get('garage_name'),
                owner_name=self.cleaned_data.get('owner_name'),
                experience_years=self.cleaned_data.get('experience_years'),
                specialization=self.cleaned_data.get('specialization'),
                workshop_address=self.cleaned_data.get('workshop_address')
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('profile_image', 'address', 'city', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
