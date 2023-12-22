from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,AccountInfo,VehicleInfo

admin.site.register(CustomUser)
admin.site.register(AccountInfo)
admin.site.register(VehicleInfo)
