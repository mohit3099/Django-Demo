from django.contrib import admin
from .models import profileModel
# Register your models here.

@admin.register(profileModel)
class profileModelAdmin(admin.ModelAdmin):
    list_display = ('user','mobile','otp')