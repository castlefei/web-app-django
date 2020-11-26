from django.urls import path

from . import views

urlpatterns = [
    # /
    path('', views.home, name='home'),
    #
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
    path('signout', views.sign_out, name='signout'),
    path('calendar', views.calendar, name='calendar'),
    path('schedule', views.schedule, name='schedule'),
    path('preference', views.preference, name='preference'),
    path('findmeetingtime', views.schedule_findmeetingtime, name='findmeetingtime'),
    path('getfreeorbusy', views.schedule_getfreeorbusy, name='getfreeorbusy'),
    path('getggevents', views.get_googleevents, name='getggevents'),
    path('mail', views.mail, name='mail'),
    path('mailtobc', views.mailtoBC, name='mailtoBC'),
    path('invitee', views.inviteeReply_handle, name='invitee'),
    path('inviteeB', views.inviteeB_handle, name='inviteeB'),
    path('inviteeC', views.inviteeC_handle, name='inviteeC')
]

