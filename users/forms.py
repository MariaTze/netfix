from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer

class AvatarChoiceForm(forms.Form):
    AVATAR_STYLES = [
        ("adventurer", "Adventurer"),
        ("avataaars", "Avataaars"),
        ("bottts", "Bottts"),
        ("croodles", "Croodles"),
        ("identicon", "Identicon"),
        ("micah", "Micah"),
        ("open-peeps", "Open Peeps"),
        ("personas", "Personas"),
        ("pixel-art", "Pixel Art"),
    ]
    style = forms.ChoiceField(choices=AVATAR_STYLES)


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Verify Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'autocomplete': 'new-password'})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'date_of_birth',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                birth=self.cleaned_data['date_of_birth']
            )
        return user


class CompanySignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    field_of_work = forms.ChoiceField(
        label='Field of Work',
        choices=Company.FIELD_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Field of Work'})
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Verify Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'autocomplete': 'new-password'})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Company.objects.create(
                user=user,
                field_of_work=self.cleaned_data['field_of_work']
            )
        return user


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'on'

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )


    def clean(self):
        return super().clean()
