"""
Real-time Voice Agent System
Handles continuous conversation flow with minimal latency
"""
import json
import asyncio
import logging
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from .tts import generate_tts, estimate_audio_duration
from .utils.interview_ai_nvidia import ask_ai_question
import time

logger = logging.getLogger(__name__)

class VoiceAgentSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.is_active = False
        self.conversation_history = []
        self.last_activity = time.time()
        
    def start_session(self):
        self.is_active = True
        self.last_activity = time.time()
        welcome_message = "Hey there! Good to see you. What's on your mind today?"
        return self.generate_response(welcome_message, is_initial=True)
    
    def generate_response(self, text, is_initial=False, voice=None):
        try:
            if not is_initial:
                # Add user input to history
                self.conversation_history.append({"role": "user", "content": text})
            
            # Generate AI response with timing
            llm_start = time.time()
            if is_initial:
                ai_response = text
                llm_latency = 0
            else:
                # Build context from conversation history
                context = "\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in self.conversation_history[-4:]  # Last 4 exchanges
                ])
                
                full_prompt = f"Previous conversation:\n{context}\n\nCandidate just said: {text}"
                try:
                    ai_response = ask_ai_question(
                        full_prompt,
                        candidate_name="User",
                        job_title="General Position",
                        company_name="Our Company"
                    )
                    llm_latency = int((time.time() - llm_start) * 1000)
                except Exception as e:
                    logger.error(f"NVIDIA LLM Error: {e}")
                    raise e
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Generate audio with timing using selected voice
            tts_start = time.time()
            if voice:
                # Temporarily override voice for this response
                from . import tts
                original_voice = tts.DAISY_VOICE_ID
                tts.DAISY_VOICE_ID = voice
                audio_url = generate_tts(ai_response)
                tts.DAISY_VOICE_ID = original_voice
            else:
                audio_url = generate_tts(ai_response)
            tts_latency = int((time.time() - tts_start) * 1000)
            audio_duration = estimate_audio_duration(ai_response)
            
            self.last_activity = time.time()
            
            return {
                "success": True,
                "text": ai_response,
                "audio_url": audio_url,
                "audio_duration": audio_duration,
                "session_active": self.is_active,
                "tts_latency": tts_latency,
                "llm_latency": llm_latency,
                "model": "nvidia/llama-3.3-nemotron-70b-instruct",
                "voice": voice or "Ana Florence"
            }
            
        except Exception as e:
            logger.error(f"Voice agent error: {e}")
            return {
                "success": False,
                "error": f"NVIDIA Llama-3.3-Nemotron model error: {str(e)}",
                "session_active": self.is_active,
                "model": "nvidia/llama-3.3-nemotron-70b-instruct"
            }
    
    def stop_session(self):
        self.is_active = False
        return {"success": True, "message": "Session ended"}

# Global session storage (use Redis in production)
active_sessions = {}

@csrf_exempt
@require_http_methods(["POST"])
def start_voice_session(request):
    """Start a new voice agent session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', f"session_{int(time.time())}")
        
        # Create new session
        session = VoiceAgentSession(session_id)
        active_sessions[session_id] = session
        
        # Start session and get welcome message
        response = session.start_session()
        response['session_id'] = session_id
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"Failed to start voice session: {e}")
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def voice_chat(request):
    """Handle voice input and generate response"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        user_text = data.get('text', '').strip()
        selected_voice = data.get('voice')
        
        if not session_id or session_id not in active_sessions:
            return JsonResponse({"success": False, "error": "Invalid session"})
        
        if not user_text:
            return JsonResponse({"success": False, "error": "No text provided"})
        
        session = active_sessions[session_id]
        if not session.is_active:
            return JsonResponse({"success": False, "error": "Session not active"})
        
        # Generate response with selected voice
        response = session.generate_response(user_text, voice=selected_voice)
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def stop_voice_session(request):
    """Stop voice agent session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if session_id in active_sessions:
            session = active_sessions[session_id]
            response = session.stop_session()
            del active_sessions[session_id]
            return JsonResponse(response)
        
        return JsonResponse({"success": True, "message": "Session not found"})
        
    except Exception as e:
        logger.error(f"Failed to stop voice session: {e}")
        return JsonResponse({"success": False, "error": str(e)})

@require_http_methods(["GET"])
def voice_agent_status(request):
    """Get voice agent system status"""
    return JsonResponse({
        "success": True,
        "active_sessions": len(active_sessions),
        "system_status": "ready"
    })