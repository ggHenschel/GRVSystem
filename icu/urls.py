from django.conf.urls import url
from django.contrib import admin
from . import views

app_name="icu"
urlpatterns = [
    url(r'^index/$',views.DevicesView.as_view(),name='index'),
    url(r'^login/$',views.login_user,name='login'),
    url(r'^logout/$',views.LogoutRequest,name='logout'),
    url(r'^create_profile/$',views.CreateProfile.as_view(),name='create_profile'),
    url(r'^update_profile/(?P<pk>[0-9]+)$',views.UpdateProfile.as_view(),name='update_profile'),
    url(r'^device/(?P<slug>[\w-]+)/$',views.DeviceDetails.as_view(),name='device_detail')
]