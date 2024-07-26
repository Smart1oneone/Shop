from urllib import request

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_email_verification import send_email

from .forms import UserCreateForm, LoginForm

User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']

            #create new user

            user = User.objects.create_user(
                username=user_username,
                email=user_email,
                password=user_password,
            )

            user.is_active = False

            send_email(user)

            return redirect('account:email_verification')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def email_verification(request):
    return render(request, 'account/email/email-verification.html')

def login_user(request):

    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('shop:shop')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/login/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('shop:products')

@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')

@login_required(login_url='account:login')
def profile_user(request):
    return render(request, 'account/dashboard/profile-management.html', context)
