"""
URL patterns for Malayalam Voice Agent with IndicF5 TTS
"""
from django.urls import path
from . import malayalam_voice_agent, malayalam_voice_views

urlpatterns = [
    path('', malayalam_voice_views.malayalam_voice_agent_page, name='malayalam_voice_main'),
    path('start/', malayalam_voice_agent.start_malayalam_voice_session, name='malayalam_voice_start'),
    path('chat/', malayalam_voice_agent.malayalam_voice_chat, name='malayalam_voice_chat'),
    path('stop/', malayalam_voice_agent.stop_malayalam_voice_session, name='malayalam_voice_stop'),
    path('status/', malayalam_voice_agent.malayalam_voice_agent_status, name='malayalam_voice_status'),
    path('test/', malayalam_voice_views.malayalam_voice_test, name='malayalam_voice_test'),
]