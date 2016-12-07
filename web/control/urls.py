from django.conf.urls import patterns, url

from control import views

urlpatterns = patterns('',
    url(r'^$', views.handle_control, name='control'),

    url(r'^(?P<vehicle_vin>.+)/$', views.handle_control, name='control'),

)
