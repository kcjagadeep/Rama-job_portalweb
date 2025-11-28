"""
TTS Testing URLs - Separate URL configuration for TTS testing
"""
from django.urls import path
from . import tts_views

urlpatterns = [
    path('test/', tts_views.tts_test_view, name='tts_test'),
    path('generate-token/', tts_views.generate_tts_token, name='generate_tts_token'),
    path('generate-speech/', tts_views.generate_tts_speech, name='generate_tts_speech'),
    path('chat/', tts_views.tts_chat_agent, name='tts_chat_agent'),
    path('models/', tts_views.get_tts_models, name='get_tts_models'),
    path('voices/', tts_views.get_voices_by_model, name='get_voices_by_model'),
    path('analyze-performance/', tts_views.analyze_conversation_performance, name='analyze_conversation_performance'),
    path('production/', tts_views.voice_agent_production, name='voice_agent_production'),
]