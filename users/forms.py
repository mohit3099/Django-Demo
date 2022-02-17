from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import UserInfo, profileModel


# class UserRegistrationForm(UserCreationForm):
#     username=forms.CharField(max_length=10)
#     first_name = forms.CharField(max_length=101)
#     last_name = forms.CharField(max_length=101)
#     email = forms.EmailField()

    # class Meta:
    #     model = User
    #     fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    class Meta:
        model = User
        fields =['username','email','mobile']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm,self).__init__(*args, **kwargs)

        for fieldname in ['username','email']:
            self.fields[fieldname].help_text=None

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profileModel
        fields = ['image']
        