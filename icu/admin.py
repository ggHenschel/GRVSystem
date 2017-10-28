from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(DeviceType)
admin.site.register(DeviceModel)
admin.site.register(Device)