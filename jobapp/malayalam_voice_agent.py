"""
Malayalam Voice Agent System with IndicF5 TTS and NVIDIA Llama-3.3-Nemotron
"""
import json
import time
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .malayalam_tts import generate_malayalam_tts, estimate_malayalam_audio_duration
from .utils.interview_ai_nvidia import ask_ai_question

logger = logging.getLogger(__name__)

class MalayalamVoiceAgentSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.is_active = False
        self.conversation_history = []
        self.last_activity = time.time()
        
    def start_session(self):
        self.is_active = True
        self.last_activity = time.time()
        welcome_message = "ഹായ്! എങ്ങനെയുണ്ട്? ഇന്ന് എന്താണ് പ്ലാൻ?"
        return self.generate_response(welcome_message, is_initial=True)
    
    def generate_response(self, text, is_initial=False):
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
                
                # Enhanced prompt for Malayalam context
                full_prompt = f"""You are a helpful AI assistant that can communicate in Malayalam. 
                The user is speaking in Malayalam or English. Please respond appropriately in the same language they use.
                If they speak Malayalam, respond in Malayalam. If they speak English, respond in English.
                
                Previous conversation:
                {context}
                
                User just said: {text}
                
                Please provide a helpful, natural response."""
                
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
                    # Fallback response in Malayalam
                    ai_response = "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ പ്രതികരിക്കാൻ കഴിയുന്നില്ല. ദയവായി വീണ്ടും ശ്രമിക്കുക."
                    llm_latency = int((time.time() - llm_start) * 1000)
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Generate Malayalam audio with timing
            tts_start = time.time()
            audio_url = generate_malayalam_tts(ai_response)
            tts_latency = int((time.time() - tts_start) * 1000)
            audio_duration = estimate_malayalam_audio_duration(ai_response)
            
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
                "voice": "Malayalam IndicF5",
                "language": "malayalam"
            }
            
        except Exception as e:
            logger.error(f"Malayalam voice agent error: {e}")
            return {
                "success": False,
                "error": f"Malayalam voice agent error: {str(e)}",
                "session_active": self.is_active,
                "model": "nvidia/llama-3.3-nemotron-70b-instruct",
                "language": "malayalam"
            }
    
    def stop_session(self):
        self.is_active = False
        return {"success": True, "message": "Session ended", "language": "malayalam"}

# Global session storage
malayalam_active_sessions = {}

@csrf_exempt
@require_http_methods(["POST"])
def start_malayalam_voice_session(request):
    """Start a new Malayalam voice agent session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', f"malayalam_session_{int(time.time())}")
        
        # Create new session
        session = MalayalamVoiceAgentSession(session_id)
        malayalam_active_sessions[session_id] = session
        
        # Start session and get welcome message
        response = session.start_session()
        response['session_id'] = session_id
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"Failed to start Malayalam voice session: {e}")
        return JsonResponse({"success": False, "error": str(e), "language": "malayalam"})

@csrf_exempt
@require_http_methods(["POST"])
def malayalam_voice_chat(request):
    """Handle Malayalam voice input and generate response"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        user_text = data.get('text', '').strip()
        
        if not session_id or session_id not in malayalam_active_sessions:
            return JsonResponse({"success": False, "error": "Invalid session", "language": "malayalam"})
        
        if not user_text:
            return JsonResponse({"success": False, "error": "No text provided", "language": "malayalam"})
        
        session = malayalam_active_sessions[session_id]
        if not session.is_active:
            return JsonResponse({"success": False, "error": "Session not active", "language": "malayalam"})
        
        # Generate response
        response = session.generate_response(user_text)
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"Malayalam voice chat error: {e}")
        return JsonResponse({"success": False, "error": str(e), "language": "malayalam"})

@csrf_exempt
@require_http_methods(["POST"])
def stop_malayalam_voice_session(request):
    """Stop Malayalam voice agent session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if session_id in malayalam_active_sessions:
            session = malayalam_active_sessions[session_id]
            response = session.stop_session()
            del malayalam_active_sessions[session_id]
            return JsonResponse(response)
        
        return JsonResponse({"success": True, "message": "Session not found", "language": "malayalam"})
        
    except Exception as e:
        logger.error(f"Failed to stop Malayalam voice session: {e}")
        return JsonResponse({"success": False, "error": str(e), "language": "malayalam"})

@require_http_methods(["GET"])
def malayalam_voice_agent_status(request):
    """Get Malayalam voice agent system status"""
    return JsonResponse({
        "success": True,
        "active_sessions": len(malayalam_active_sessions),
        "system_status": "ready",
        "language": "malayalam",
        "tts_service": "IndicF5",
        "llm_model": "nvidia/llama-3.3-nemotron-70b-instruct"
    })