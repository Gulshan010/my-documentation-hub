from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


SEMESTER_CHOICES = [
    ('', 'Select Class'),
    ('BCA I SEM', 'BCA I SEM'),
    ('BCA II SEM', 'BCA II SEM'),
    ('BCA III SEM', 'BCA III SEM'),
    ('BCA IV SEM', 'BCA IV SEM'),
    ('BCA V SEM', 'BCA V SEM'),
    ('BCA VI SEM', 'BCA VI SEM'),
]


class BaseUserAccessForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    class_name = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        required=False,
        label='Class'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        class_name = cleaned_data.get('class_name', '')
        if role == UserProfile.ROLE_STUDENT and not class_name:
            self.add_error('class_name', 'Class is required for student accounts.')
        if role != UserProfile.ROLE_STUDENT:
            cleaned_data['class_name'] = ''
        return cleaned_data


class RegistrationForm(BaseUserAccessForm):
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError('This name is already registered.')
        return name


class LoginForm(BaseUserAccessForm):
    def clean_name(self):
        return self.cleaned_data['name'].strip()
