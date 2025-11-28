"""
Views for Malayalam Voice Agent with IndicF5 TTS
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .malayalam_tts import check_malayalam_tts_status

def malayalam_voice_agent_page(request):
    """Malayalam Voice Agent page with IndicF5 TTS"""
    # Check TTS status
    tts_working, tts_message = check_malayalam_tts_status()
    
    context = {
        'title': 'Malayalam Voice Agent - IndicF5',
        'page_description': 'Malayalam voice conversations with NVIDIA Llama-3.3-Nemotron',
        'tts_status': tts_working,
        'tts_message': tts_message,
        'api_endpoint': 'http://34.232.76.115:8021',
        'model': 'NVIDIA Llama-3.3-Nemotron'
    }
    return render(request, 'jobapp/malayalam_voice_agent.html', context)

@csrf_exempt
def malayalam_voice_test(request):
    """Test endpoint for Malayalam voice agent"""
    if request.method == 'POST':
        return JsonResponse({
            'success': True,
            'message': 'Malayalam voice agent test successful',
            'language': 'malayalam',
            'tts_service': 'IndicF5',
            'api_endpoint': 'http://34.232.76.115:8021/v2',
            'model': 'nvidia/llama-3.3-nemotron-70b-instruct'
        })
    
    # Check system status
    tts_working, tts_message = check_malayalam_tts_status()
    
    return JsonResponse({
        'success': True,
        'status': 'Malayalam voice agent operational',
        'tts_status': tts_working,
        'tts_message': tts_message,
        'endpoints': [
            '/malayalam-voice/start/',
            '/malayalam-voice/chat/',
            '/malayalam-voice/stop/',
            '/malayalam-voice/status/'
        ],
        'language': 'malayalam',
        'api_endpoint': 'http://34.232.76.115:8021/v2'
    })