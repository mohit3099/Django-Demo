from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=10)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    email=models.EmailField()
    password=models.CharField(max_length=8)
    otp=models.IntegerField()
  
    
class profileModel(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    image = models.ImageField(default = 'default.jpg',upload_to='profile', validators=[FileExtensionValidator(['png','jpg','jpeg'])])
    otp = models.CharField(max_length=6, null=True, blank=True)
    exp_time = models.DateTimeField()


    def __str__(self):
        return self.user.username
