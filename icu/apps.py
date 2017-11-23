from django.apps import AppConfig
from django import setup


class IcuConfig(AppConfig):
    name = 'icu'
    verbose_name = "ICU - GRV Solutions"
    runned = False

    def ready(self):
        if not self.runned:
            self.runned = True
            from icu.models import Device
            #MDevice = self.get_model('Device')
            devices = Device.objects.all()
            for device in devices:
                device.active()
        pass