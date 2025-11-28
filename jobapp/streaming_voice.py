"""
Streaming Voice Agent for Real-time Audio Processing
"""
import json
import asyncio
import time
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils.interview_ai_nvidia import ask_ai_question
from .tts import generate_tts

@csrf_exempt
@require_http_methods(["POST"])
def streaming_voice_chat(request):
    """Streaming voice chat with real-time responses"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        voice = data.get('voice', 'Daisy Studious')
        
        if not message:
            return JsonResponse({'success': False, 'error': 'No message provided'})
        
        def generate_streaming_response():
            # Start timing
            start_time = time.time()
            
            # Send initial response
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing...'})}\n\n"
            
            # Generate AI response
            llm_start = time.time()
            ai_response = ask_ai_question(
                message,
                candidate_name="User",
                job_title="Voice Chat",
                company_name="Streaming Lab"
            )
            llm_latency = int((time.time() - llm_start) * 1000)
            
            # Send AI response
            yield f"data: {json.dumps({'type': 'text', 'content': ai_response, 'llm_latency': llm_latency})}\n\n"
            
            # Generate TTS
            tts_start = time.time()
            audio_url = generate_tts(ai_response)
            tts_latency = int((time.time() - tts_start) * 1000)
            
            # Send audio response
            total_latency = int((time.time() - start_time) * 1000)
            yield f"data: {json.dumps({'type': 'audio', 'url': audio_url, 'tts_latency': tts_latency, 'total_latency': total_latency})}\n\n"
            
            # Send completion
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
        
        response = StreamingHttpResponse(
            generate_streaming_response(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        response['Access-Control-Allow-Origin'] = '*'
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt  
@require_http_methods(["POST"])
def streaming_tts_only(request):
    """Streaming TTS generation only"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        voice = data.get('voice', 'Daisy Studious')
        
        if not text:
            return JsonResponse({'success': False, 'error': 'No text provided'})
        
        def generate_tts_stream():
            start_time = time.time()
            
            yield f"data: {json.dumps({'type': 'start', 'message': 'Generating audio...'})}\n\n"
            
            audio_url = generate_tts(text)
            latency = int((time.time() - start_time) * 1000)
            
            yield f"data: {json.dumps({'type': 'audio', 'url': audio_url, 'latency': latency})}\n\n"
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
        
        response = StreamingHttpResponse(
            generate_tts_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        response['Access-Control-Allow-Origin'] = '*'
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})