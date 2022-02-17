from multiprocessing import context
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from datetime import timedelta
from random import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from .models import profileModel
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
import random

def home(request):
    return render(request, 'users/home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance= request.user)
        p_form = ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilemodel)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'users/profile.html', context)

def register(request):
    form = SignupForm(request.POST)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username') 
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')         
            check_user = User.objects.filter(email = email).first()
            check_profile = profileModel.objects.filter(mobile = mobile).first()
            
            if check_user:
                context = {'message' : 'User already exists', 'class':'danger' }
                return render(request,'users/register.html', context)

            user = User(username = username, email = email)
            user.save()
            otp= str(random.randint(1000,9999))
            # print('otp is : ',otp)
            profile = profileModel(user = user, mobile = mobile, otp = otp, exp_time = timezone.now() + timedelta(seconds=60))
            profile.save()
            # send_mail('Your OTP', f'Your otp for Registration is: {otp}.','shahmohit3099@gmail.com', [email],fail_silently=False)
            request.session['email']= email
            return redirect('login')
            
            # messages.success(request, f'Your account has been created. You can log in now!')    
            # return redirect('login')
    else:
        form = SignupForm()
        pass

    context = {'form': form}
    return render(request, 'users/register.html', context)

def login_req(request):
    if request.method == 'POST':
        # mobile = request.POST.get('mobile')
        email = request.POST.get("email")
        
        # user = profileModel.objects.filter(mobile = mobile).first()
        user = User.objects.filter(email = email).first()
        profile = profileModel.objects.filter(user = user).first() 
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'users/login.html' , context)         
        otp = str(random.randint(1000 , 9999))
        profile.otp = otp
        profile.exp_time = timezone.now() + timedelta(seconds = 60)
        profile.save()
        print('otp is : ',otp)
        # send_otp(mobile , otp)
        send_mail(
            'your otp',
        f'Here is your otp: {otp}. It will expire in 1 minute',
            'shahmohit3099@gmail.com',
            [email],
                fail_silently=False
                                    )
        # request.session['mobile'] = mobile
        request.session['email'] = email
        return redirect('otp')        
    return render(request,'users/login.html')

def otp(request):
    email = request.session['email']
    context = {'email':email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.filter(email = email).first()
        profile = profileModel.objects.filter(user = user).first()

        if otp == profile.otp and profile.exp_time > timezone.now():
            print("--------------------------")
            user = User.objects.get(id = profile.user.id)
            print(user.id)
            login(request , user)
            profile.otp = None
            profile.save()
            return redirect('blog-index')

        if otp != profile.otp:
            context = {'message' : 'Wrong OTP', 'class' : 'danger','email':email}
            return render(request,'users/otp.html', context)
            # user = User.objects.get(id = profile.user.id)
            # login(request,user)
            # return redirect('home')
        else:
            profile.otp = None
            profile.save()
            context = {'message' : 'Expired OTP', 'class' : 'danger','email':email}
            return render(request,'users/otp.html', context)

    return render(request,'users/otp.html', context)


def resend_otp(request):
    email = request.session['email']
    user = User.objects.filter(email = email).first()
    profile = profileModel.objects.filter(user = user).first()
    if user is None:
        context = {'message': 'User not found','class': 'danger'}
        return render(request, 'users/login.html', context)
    otp = str(random.randint(1000, 9999))
    profile.otp = otp
    profile.exp_time = timezone.now() + timedelta(seconds=60)
    profile.save()
    send_mail(  
        'your otp',
        f'Here is your otp: {otp}.',
            'shahmohit3099@gmail.com',
            [email],
                fail_silently=False
                                    )
    # request.session['mobile'] = mobile
    request.session['email'] = email
    return redirect('otp') 
