from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email-verification/', email_verification, name='email_verification'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Dashboard
    path('dashboard/', dashboard_user, name='dashboard'),
    path('profile-management/', profile_user, name='profile-management'),
    path('delete-user/', delete_user, name='delete-user'),
]