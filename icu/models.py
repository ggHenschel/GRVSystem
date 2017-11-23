from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.http import response
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from camera import client, server
import threading as thr

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


    def active(self,ip):
        # POG
        if self.device_type.get_camera():
            self.th_server = thr.Thread(target=server.server_run)
            self.th_server.start()
            self.th_camera = thr.Thread(target=client.camera)
            self.th_camera.start()


class Device(models.Model):
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, blank=False)
    mac_address = models.TextField(blank=False,unique=True,primary_key=True)
    ip_address = models.GenericIPAddressField(blank=False,unique=True)
    device_name = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    activeted = False

    def __str__(self):
        return str(self.device_name)

    def save(self, **kwargs):
        self.slug = slugify(self.mac_address)
        super(Device,self).save(**kwargs)

    def active(self):
        if not self.activeted:
            print("Ativando Objeto:"+str(self)+str(self.activeted))
            self.activeted = True
            self.device_model.active(self.ip_address)
            print("Objeto:" + str(self) +" Ativo "+ str(self.activeted))