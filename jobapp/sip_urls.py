"""
URL patterns for SIP Trunk system
"""
from django.urls import path
from . import sip_trunk, sip_views

urlpatterns = [
    path('', sip_views.sip_trunk_test, name='sip_trunk_test'),
    path('test/', sip_views.sip_trunk_test, name='sip_test_page'),
    path('status/', sip_views.sip_test_status, name='sip_test_status'),
    path('dial/', sip_trunk.sip_dial, name='sip_dial'),
    path('hangup/', sip_trunk.sip_hangup, name='sip_hangup'),
    path('call-status/', sip_trunk.sip_status, name='sip_status'),
    path('old/', sip_views.sip_trunk_test_old, name='sip_trunk_test_old'),
]