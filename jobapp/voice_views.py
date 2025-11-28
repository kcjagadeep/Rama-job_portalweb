"""
Views for Voice Agent Demo and Integration
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .tts import check_tts_api_status
from django.conf import settings
import os
import json

def voice_agent_demo(request):
    """Demo page for the real-time voice agent"""
    context = {
        'title': 'Real-time Voice Agent Demo',
        'page_description': 'Experience telephone-like conversations with AI'
    }
    return render(request, 'jobapp/voice_agent_demo.html', context)

def voice_agent_test_page(request):
    """Test page for voice agent functionality"""
    return render(request, 'jobapp/voice_test.html')

@csrf_exempt
def voice_agent_test(request):
    """Test endpoint for voice agent functionality"""
    if request.method == 'POST':
        return JsonResponse({
            'success': True,
            'message': 'Voice agent test successful',
            'timestamp': str(request.POST.get('timestamp', 'unknown'))
        })
    
    return JsonResponse({
        'success': True,
        'status': 'Voice agent system operational',
        'endpoints': [
            '/voice/start/',
            '/voice/chat/',
            '/voice/stop/',
            '/voice/status/'
        ]
    })

def get_voice_info(request):
    """Get current voice and TTS health status"""
    try:
        # Get current voice setting
        current_voice = getattr(settings, 'NEW_TTS_VOICE_ID', '') or os.environ.get('NEW_TTS_VOICE_ID', 'Ana Florence')
        
        # Check TTS health
        tts_healthy, tts_message = check_tts_api_status()
        
        return JsonResponse({
            'success': True,
            'current_voice': current_voice,
            'tts_healthy': tts_healthy,
            'tts_status': tts_message
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'current_voice': 'Ana Florence',
            'tts_healthy': False,
            'tts_status': 'Error checking TTS'
        })

@csrf_exempt
@require_http_methods(["POST"])
def test_voice(request):
    """Test a specific voice with sample text"""
    try:
        data = json.loads(request.body)
        voice_name = data.get('voice', 'Ana Florence')
        test_text = data.get('text', f'Hello, I am {voice_name}.')
        
        # Temporarily override the voice setting
        from . import tts
        original_voice = tts.DAISY_VOICE_ID
        tts.DAISY_VOICE_ID = voice_name
        
        # Generate TTS with the selected voice
        from .tts import generate_tts
        audio_url = generate_tts(test_text)
        
        # Restore original voice
        tts.DAISY_VOICE_ID = original_voice
        
        return JsonResponse({
            'success': True,
            'audio_url': audio_url,
            'voice': voice_name
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })