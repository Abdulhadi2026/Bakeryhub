from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, sync_user_role


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('staff', 'Staff')],
        required=True,
        initial='staff',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'Last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'Email address'})
        self.fields['role'].widget.attrs.update({'class': 'form-select auth-input'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control auth-input', 'placeholder': 'Confirm password'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.save()
            sync_user_role(user)
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'role')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
