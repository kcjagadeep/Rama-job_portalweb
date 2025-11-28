"""
TTS API Proxy - Handle API calls server-side to avoid CORS issues
"""
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

API_BASE = "http://34.232.76.115"

@csrf_exempt
@require_http_methods(["POST"])
def proxy_register(request):
    """Proxy registration to TTS API"""
    try:
        data = json.loads(request.body)
        response = requests.post(
            f"{API_BASE}/v1/auth/register",
            json=data,
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def proxy_models(request):
    """Proxy models endpoint"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        headers = {'xi-api-key': token} if token else {}
        
        response = requests.get(
            f"{API_BASE}/v1/models",
            headers=headers,
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def proxy_voices(request):
    """Proxy voices endpoint"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        model = request.GET.get('model')
        
        headers = {'xi-api-key': token} if token else {}
        params = {'model': model} if model else {}
        
        response = requests.get(
            f"{API_BASE}/v1/voices",
            headers=headers,
            params=params,
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def proxy_tts(request):
    """Proxy TTS generation"""
    try:
        data = json.loads(request.body)
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        headers = {
            'Content-Type': 'application/json',
            'xi-api-key': token
        } if token else {'Content-Type': 'application/json'}
        
        response = requests.post(
            f"{API_BASE}/v1/text-to-speech",
            json=data,
            headers=headers,
            timeout=30
        )
        
        if response.headers.get('content-type', '').startswith('audio/'):
            # Return audio file
            from django.http import HttpResponse
            return HttpResponse(
                response.content,
                content_type=response.headers.get('content-type', 'audio/mpeg')
            )
        else:
            return JsonResponse(response.json(), status=response.status_code)
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)