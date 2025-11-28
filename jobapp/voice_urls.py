"""
URL patterns for Voice Agent system
"""
from django.urls import path
from . import voice_agent, voice_views

urlpatterns = [
    path('', voice_views.voice_agent_demo, name='voice_agent_main'),  # Main voice agent page
    path('start/', voice_agent.start_voice_session, name='voice_start'),
    path('chat/', voice_agent.voice_chat, name='voice_chat'),
    path('stop/', voice_agent.stop_voice_session, name='voice_stop'),
    path('status/', voice_agent.voice_agent_status, name='voice_status'),
    path('demo/', voice_views.voice_agent_demo, name='voice_demo'),
    path('test/', voice_views.voice_agent_test, name='voice_test'),
    path('test-page/', voice_views.voice_agent_test_page, name='voice_test_page'),
    path('info/', voice_views.get_voice_info, name='voice_info'),
    path('test-voice/', voice_views.test_voice, name='test_voice'),
]