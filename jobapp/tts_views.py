"""
TTS Testing Views - Separate module for TTS testing functionality
"""
import json
import requests
import time
import os
import hashlib
import secrets
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
# Only use http://34.232.76.115 API

def tts_test_view(request):
    """TTS Testing Lab main page"""
    return render(request, 'jobapp/tts_test.html')

def voice_agent_production(request):
    """Production Voice Agent for real testing"""
    return render(request, 'jobapp/voice_agent_production.html')

@csrf_exempt
@require_http_methods(["POST"])
def generate_tts_token(request):
    """Generate API token for TTS testing"""
    try:
        # Use valid API key
        token = "sk_jWLTvSRsgUBU0tc-itmrlBwUCQzyz-mw_aiudQphfpg"
        
        # Fetch models and voices when token is generated
        models = []
        voices = []
        api_status = 'disconnected'
        
        # Try multiple endpoints and methods
        endpoints = [
            "/v1/models",
            "/models", 
            "/api/v1/models"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"http://34.232.76.115{endpoint}"
                # Try with and without auth
                for headers in [{"xi-api-key": token}, {}]:
                    response = requests.get(url, headers=headers, timeout=5)
                    print(f"Trying {url} with headers {headers}: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"Success! Data: {data}")
                        if data:
                            api_status = 'connected'
                            # Parse response
                            if isinstance(data, list):
                                for item in data:
                                    models.append({
                                        'id': item.get('model_id', item.get('id', item.get('name', f'model_{len(models)+1}'))),
                                        'name': item.get('name', item.get('model_id', f'Model {len(models)+1}')),
                                        'description': item.get('description', 'TTS Model')
                                    })
                            elif isinstance(data, dict):
                                if 'models' in data:
                                    for item in data['models']:
                                        models.append({
                                            'id': item.get('model_id', item.get('id', f'model_{len(models)+1}')),
                                            'name': item.get('name', f'Model {len(models)+1}'),
                                            'description': item.get('description', 'TTS Model')
                                        })
                            break
                    if models:
                        break
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
            if models:
                break
                
        # Use only API models
            
        # Try multiple endpoints for voices
        voice_endpoints = [
            "/v1/voices",
            "/voices",
            "/api/v1/voices"
        ]
        
        for endpoint in voice_endpoints:
            try:
                url = f"http://34.232.76.115{endpoint}"
                for headers in [{"xi-api-key": token}, {}]:
                    response = requests.get(url, headers=headers, timeout=5)
                    print(f"Trying {url} with headers {headers}: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"Voices success! Data: {data}")
                        if data:
                            # Parse response
                            if isinstance(data, list):
                                for item in data:
                                    voices.append({
                                        'id': item.get('voice_id', item.get('id', item.get('name', f'voice_{len(voices)+1}'))),
                                        'name': item.get('name', f'Voice {len(voices)+1}'),
                                        'gender': item.get('gender', item.get('labels', {}).get('gender', 'Unknown')),
                                        'style': item.get('style', item.get('labels', {}).get('accent', 'General'))
                                    })
                            elif isinstance(data, dict) and 'voices' in data:
                                for item in data['voices']:
                                    voices.append({
                                        'id': item.get('voice_id', item.get('id', f'voice_{len(voices)+1}')),
                                        'name': item.get('name', f'Voice {len(voices)+1}'),
                                        'gender': item.get('gender', item.get('labels', {}).get('gender', 'Unknown')),
                                        'style': item.get('style', item.get('labels', {}).get('accent', 'General'))
                                    })
                            break
                    if voices:
                        break
            except Exception as e:
                print(f"Error with voices {endpoint}: {e}")
            if voices:
                break
                
        # Fallback voices
        if not voices:
            voices = [
                {'id': 'Rachel', 'name': 'Rachel', 'gender': 'Female', 'style': 'American'},
                {'id': 'Drew', 'name': 'Drew', 'gender': 'Male', 'style': 'American'},
                {'id': 'Clyde', 'name': 'Clyde', 'gender': 'Male', 'style': 'American'}
            ]
        
        return JsonResponse({
            'success': True,
            'token': token,
            'expires_in': 3600,
            'api_status': api_status,
            'models': models,
            'voices': voices
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def generate_tts_speech(request):
    """Generate speech using TTS API"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        model = data.get('model', 'default')
        voice = data.get('voice', 'default')
        token = data.get('token', '')
        
        if not text:
            return JsonResponse({'success': False, 'error': 'No text provided'})
        
        if not model or model == 'default':
            return JsonResponse({'success': False, 'error': 'Please select a TTS model'})
        
        if not voice or voice == 'default':
            return JsonResponse({'success': False, 'error': 'Please select a voice'})
        
        start_time = time.time()
        
        # Use real API endpoint from OpenAPI spec
        api_url = "http://34.232.76.115/v1/text-to-speech"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": data.get('token', token)
        }
        
        payload = {
            "text": text,
            "model_id": data.get('tts_model', model),
            "voice_id": voice
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Save audio file
            text_hash = hashlib.md5(f"{text}_{model}_{voice}".encode()).hexdigest()[:10]
            filename = f"tts_test_{text_hash}.mp3"
            tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
            os.makedirs(tts_dir, exist_ok=True)
            filepath = os.path.join(tts_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            latency = int((time.time() - start_time) * 1000)
            
            return JsonResponse({
                'success': True,
                'audio_url': f'/media/tts/{filename}',
                'latency': latency,
                'model': model,
                'voice': voice
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'TTS API error: {response.status_code} - {response.text}'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def tts_chat_agent(request):
    """Chat with AI agent and generate TTS responses"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        llm_model = data.get('model', 'gpt-3.5-turbo')
        voice = data.get('voice', 'Daisy Studious')
        auto_speak = data.get('auto_speak', True)
        
        if not message:
            return JsonResponse({'success': False, 'error': 'No message provided'})
        
        # Generate AI response using real NVIDIA LLM
        from .utils.interview_ai_nvidia import ask_ai_question
        
        llm_start = time.time()
        
        # Use NVIDIA LLM - no fallbacks allowed
        conversation_context = f"You are a helpful AI voice assistant. The user just said: '{message}'. Respond naturally and conversationally. Keep responses brief (1-2 sentences) and engaging. Be helpful and friendly."
        
        ai_response = ask_ai_question(
            conversation_context,
            candidate_name="User",
            job_title="Voice Conversation",
            company_name="AI Assistant"
        )
        
        llm_latency = int((time.time() - llm_start) * 1000)
        
        print(f"✅ User: {message}")
        print(f"✅ AI: {ai_response}")
        print(f"⚡ Response Time: {llm_latency}ms")
        
        # Generate TTS for AI response using selected model and voice
        audio_url = None
        tts_latency = 0
        
        if auto_speak:
            try:
                tts_start = time.time()
                
                # Get TTS parameters from request
                voice_id = data.get('voice_id', 'en_female_1')
                model_id = data.get('model_id', 'coqui')
                api_key = data.get('token', '')
                
                api_url = "http://34.232.76.115/v1/text-to-speech"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": api_key
                }
                
                payload = {
                    "text": ai_response,
                    "model_id": model_id,
                    "voice_id": voice_id
                }
                
                print(f"TTS Request: {model_id} + {voice_id} + {ai_response[:50]}...")
                
                response = requests.post(api_url, json=payload, headers=headers, timeout=20)
                tts_latency = int((time.time() - tts_start) * 1000)
                
                print(f"TTS Response: {response.status_code}")
                
                if response.status_code == 200:
                    text_hash = hashlib.md5(f"{ai_response}_{model_id}_{voice_id}".encode()).hexdigest()[:8]
                    filename = f"agent_{text_hash}.mp3"
                    tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
                    os.makedirs(tts_dir, exist_ok=True)
                    filepath = os.path.join(tts_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    audio_url = f'/media/tts/{filename}'
                    print(f"TTS Success: {audio_url}")
                else:
                    print(f"TTS Failed: {response.text}")
                    
            except Exception as e:
                print(f"TTS generation failed: {e}")
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'audio_url': audio_url,
            'model_used': 'nvidia/llama-3.3-nemotron-super-49b-v1',
            'tts_model_used': data.get('model_id', 'coqui'),
            'voice_used': data.get('voice_id', 'en_female_1'),
            'llm_latency': llm_latency,
            'tts_latency': tts_latency,
            'total_latency': llm_latency + tts_latency,
            'timestamp': int(time.time() * 1000)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_voices_by_model(request):
    """Get voices using real API endpoint"""
    try:
        # Get API key from request header
        api_key = request.headers.get('xi-api-key', 'sk_jWLTvSRsgUBU0tc-itmrlBwUCQzyz-mw_aiudQphfpg')
        model_id = request.GET.get('model')
        
        headers = {
            'accept': 'application/json',
            'xi-api-key': api_key
        }
        
        # Build URL with model parameter if provided
        url = "http://34.232.76.115/v1/voices"
        if model_id:
            url += f"?model={model_id}"
        
        print(f"Calling voices API: {url} with key: {api_key}")
        
        voices_response = requests.get(url, headers=headers, timeout=15)
        
        print(f"Voices API response: {voices_response.status_code}")
        print(f"Voices API content: {voices_response.text}")
        
        if voices_response.status_code == 200:
            voices_data = voices_response.json()
            return JsonResponse({
                'success': True, 
                'voices': voices_data.get('voices', voices_data)
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': f'API returned {voices_response.status_code}: {voices_response.text}'
            })
            
    except Exception as e:
        print(f"Voices API error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_tts_models(request):
    """Get available TTS models using real API key"""
    try:
        # Get API key from request header
        api_key = request.headers.get('xi-api-key', 'sk_jWLTvSRsgUBU0tc-itmrlBwUCQzyz-mw_aiudQphfpg')
        
        headers = {
            'accept': 'application/json',
            'xi-api-key': api_key
        }
        
        print(f"Calling models API with key: {api_key}")
        
        models_response = requests.get(
            "http://34.232.76.115/v1/models", 
            headers=headers, 
            timeout=15
        )
        
        print(f"Models API response: {models_response.status_code}")
        print(f"Models API content: {models_response.text}")
        
        if models_response.status_code == 200:
            models_data = models_response.json()
            return JsonResponse({
                'success': True, 
                'models': models_data.get('models', models_data)
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': f'API returned {models_response.status_code}: {models_response.text}'
            })
            
    except Exception as e:
        print(f"Models API error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def analyze_conversation_performance(request):
    """Analyze conversation performance metrics"""
    try:
        data = json.loads(request.body)
        metrics = data.get('metrics', [])
        
        if not metrics:
            return JsonResponse({'success': False, 'error': 'No metrics provided'})
        
        # Calculate performance statistics
        total_conversations = len(metrics)
        avg_total_latency = sum(m.get('totalLatency', 0) for m in metrics) / total_conversations
        avg_speech_recognition = sum(m.get('speechRecognitionTime', 0) for m in metrics) / total_conversations
        avg_llm_response = sum(m.get('llmResponseTime', 0) for m in metrics) / total_conversations
        avg_tts_generation = sum(m.get('ttsGenerationTime', 0) for m in metrics) / total_conversations
        
        return JsonResponse({
            'success': True,
            'analysis': {
                'total_conversations': total_conversations,
                'average_latencies': {
                    'total': round(avg_total_latency),
                    'speech_recognition': round(avg_speech_recognition),
                    'llm_response': round(avg_llm_response),
                    'tts_generation': round(avg_tts_generation)
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})