from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput, PasswordInput

User = get_user_model()

class UserCreateForm(UserCreationForm):
    model = User
    fields = ('username', 'email', 'password1', 'password2')
    email = forms.EmailField(required=True, label='Email')
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your Email Address'
        self.fields['email'].required = True
        self.fields['username'].help_text = 'Your Username'
        self.fields['password1'].help_text = 'Your Password'


    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError('Email already registered or too long')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

