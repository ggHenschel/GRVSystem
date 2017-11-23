from django.http import *
from django.shortcuts import render, render_to_response,redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from . import models

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('icu:index'))
        request.error = True
        print("Login Error")
    return render(request, 'icu/login_form.html')

class DevicesView(LoginRequiredMixin, ListView):
    login_url = '/icu/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'icu/index_form.html'
    context_object_name = 'devices_list'

    def get_queryset(self):
        #print(models.Device.objects.all())
        return models.Device.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DevicesView,self).get_context_data(**kwargs)
        try:
            profile = models.Profile.objects.get(user=self.request.user)
            if profile:
                context['profile'] = profile
        except:
            pass
        return context

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect(reverse('icu:index'))

class CreateProfile(LoginRequiredMixin, CreateView):
    login_url = '/icu/login/'
    redirect_field_name = 'redirect_to'
    model = models.Profile
    template_name = 'icu/create_profile_form.html'
    fields = ['user','first_name','last_name','email','phone']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        print(obj)
        return HttpResponseRedirect(reverse('icu:index'))

    def get_initial(self):
        initial = super(CreateProfile,self).get_initial()
        initial['user'] = self.request.user
        return initial

class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = '/icu/login/'
    redirect_field_name = 'redirect_to'
    model = models.Profile
    template_name = 'icu/create_profile_form.html'
    fields = ['user', 'first_name', 'last_name', 'email', 'phone']

    def get_success_url(self):
        return reverse_lazy('icu:index')

class DeviceDetails(LoginRequiredMixin, DetailView):
    model = models.Device
    template_name = 'icu/device_detail.html'
    fields = ['device_name','mac_address','ip_address','device_model']

    def get_object(self, queryset=None):
        device = get_object_or_404(models.Device,slug=self.kwargs['slug'])
        return device

    def get_context_data(self, **kwargs):
        context = super(DeviceDetails,self).get_context_data(**kwargs)
        context['all_devices'] = models.Device.objects.all()
        try:
            profile = models.Profile.objects.get(user=self.request.user)
            if profile:
                context['profile'] = profile
        except:
            pass

        return context

