"""
URL patterns for WebRTC SIP system
"""
from django.urls import path
from . import webrtc_sip

urlpatterns = [
    path('config/', webrtc_sip.webrtc_config, name='webrtc_config'),
    path('call/start/', webrtc_sip.webrtc_call_start, name='webrtc_call_start'),
    path('call/end/', webrtc_sip.webrtc_call_end, name='webrtc_call_end'),
]