from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views


urlpatterns = [
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('profile', user_views.profile, name='profile'),
    path('login/', user_views.login_req, name='login'),
    path('otp/', user_views.otp, name ='otp' ),
    path('resendotp/', user_views.resend_otp, name = 'resend-otp'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]