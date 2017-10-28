from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.http import response
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from . import camera

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=80)
    email = models.EmailField()
    phone = models.TextField(max_length=20)

    def __str__(self):
        return str(self.first_name)+" "+str(self.last_name)

class DeviceType(models.Model):
    type_name = models.TextField(max_length=50)
    type_description = models.TextField(max_length=300)

    def __str__(self):
        return str(self.type_name)

    def get_camera(self):
        if self.type_name == 'Camera':
            return True
        else:
            return False

class DeviceModel(models.Model):
    device_type = models.ForeignKey(DeviceType,on_delete=models.CASCADE)
    device_model = models.TextField(max_length=120)

    def __str__(self):
        return str(self.device_model)

    #POG
    def get_camera(self,ip):
        #POG
        if self.device_type.get_camera():
            cam = camera.Camera(ip)
            return response.StreamingHttpResponse(response.HttpResponse(cam.gen()))
        else:
            pass

class Device(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, blank=False)
    mac_address = models.TextField(blank=False,unique=True,primary_key=True)
    ip_address = models.GenericIPAddressField(blank=False,unique=True)
    device_name = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return str(self.device_name)

    def save(self, **kwargs):
        self.slug = slugify(self.mac_address)
        super(Device,self).save(**kwargs)

    def get_camera(self):
        return self.device_model.get_camera(self.ip_address)