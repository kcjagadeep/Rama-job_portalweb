"""
TTS.PY - Configured for Daisy Studious voice using new TTS API
"""
import requests
import os
from gtts import gTTS
from django.conf import settings
import hashlib
import logging

logger = logging.getLogger(__name__)

# New TTS API Configuration
NEW_TTS_API_KEY = getattr(settings, 'NEW_TTS_API_KEY', '') or os.environ.get('NEW_TTS_API_KEY', 'sk_jWLTvSRsgUBU0tc-itmrlBwUCQzyz-mw_aiudQphfpg')
NEW_TTS_API_URL = getattr(settings, 'NEW_TTS_API_URL', '') or os.environ.get('NEW_TTS_API_URL', 'http://34.232.76.115')
NEW_TTS_VOICE_ID = getattr(settings, 'NEW_TTS_VOICE_ID', '') or os.environ.get('NEW_TTS_VOICE_ID', 'Ana Florence')
NEW_TTS_MODEL_ID = getattr(settings, 'NEW_TTS_MODEL_ID', '') or os.environ.get('NEW_TTS_MODEL_ID', 'coqui')

if NEW_TTS_API_KEY:
    NEW_TTS_API_KEY = NEW_TTS_API_KEY.strip()

# Use only TTS API voices
DEFAULT_VOICE_ID = NEW_TTS_VOICE_ID or "Ana Florence"

def generate_tts_api_only(text, voice="Ana Florence"):
    """Generate TTS using only the main TTS API"""
    try:
        if not NEW_TTS_API_KEY or not NEW_TTS_API_URL:
            raise Exception("TTS API not configured")
        
        # Create filename for caching
        text_hash = hashlib.md5(f"{text}_{voice}".encode()).hexdigest()[:10]
        filename = f"tts_api_{text_hash}.mp3"
        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
        os.makedirs(tts_dir, exist_ok=True)
        filepath = os.path.join(tts_dir, filename)
        
        # Check cache first
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/media/tts/{filename}"
        
        # API request
        url = f"{NEW_TTS_API_URL.rstrip('/')}/v1/text-to-speech"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": NEW_TTS_API_KEY
        }
        
        payload = {
            "text": text.strip(),
            "voice_id": voice,
            "model_id": NEW_TTS_MODEL_ID or "coqui"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                return f"/media/tts/{filename}"
        
        raise Exception(f"TTS API failed: {response.status_code}")
        
    except Exception as e:
        logger.error(f"TTS API failed: {e}")
        raise e

def generate_elevenlabs_tts(text, voice="female_interview"):
    """Generate TTS using new API with Daisy Studious voice"""
    try:
        if not NEW_TTS_API_KEY or not NEW_TTS_API_URL:
            return generate_google_tts(text)
        
        # Create filename for caching
        text_hash = hashlib.md5(f"{text}_daisy".encode()).hexdigest()[:10]
        filename = f"daisy_{text_hash}.mp3"
        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
        os.makedirs(tts_dir, exist_ok=True)
        filepath = os.path.join(tts_dir, filename)
        
        # Check cache first
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/media/tts/{filename}"
        
        # API request
        url = f"{NEW_TTS_API_URL.rstrip('/')}/v1/text-to-speech"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": NEW_TTS_API_KEY
        }
        
        payload = {
            "text": text.strip(),
            "voice_id": DEFAULT_VOICE_ID,
            "model_id": NEW_TTS_MODEL_ID or "coqui"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                return f"/media/tts/{filename}"
        
        # If failed, fall back to Google TTS
        return generate_google_tts(text)
        
    except Exception as e:
        logger.error(f"Daisy TTS failed: {e}")
        return generate_google_tts(text)

def generate_google_tts(text, lang='en'):
    """Generate TTS using Google Text-to-Speech as fallback"""
    try:
        text_hash = hashlib.md5(f"{text}_google".encode()).hexdigest()[:10]
        filename = f"google_{text_hash}.mp3"
        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
        os.makedirs(tts_dir, exist_ok=True)
        filepath = os.path.join(tts_dir, filename)
        
        # Check cache first
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/media/tts/{filename}"
        
        # Generate with Google TTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/media/tts/{filename}"
        
        return None
        
    except Exception as e:
        logger.error(f"Google TTS failed: {e}")
        return None

def generate_tts(text, voice="Ana Florence"):
    """Main TTS function - tries TTS API first, falls back to Google TTS"""
    try:
        return generate_tts_api_only(text, voice)
    except Exception as e:
        logger.warning(f"TTS API failed ({e}), falling back to Google TTS")
        return generate_google_tts(text)

def generate_gtts_fallback(text):
    """Fallback function for Google TTS"""
    return generate_google_tts(text)

def estimate_audio_duration(text): 
    """Estimate audio duration based on text length"""
    # Average speaking rate is about 150-160 words per minute
    # Average word length is about 5 characters
    words = len(text.split())
    if words == 0:
        return 3.0  # Minimum duration
    
    # Estimate duration in seconds (150 words per minute)
    duration = (words / 150) * 60
    return max(3.0, min(duration, 30.0))  # Between 3-30 seconds

def get_audio_duration(file_path):
    """Get actual audio duration from file"""
    try:
        import os
        if not os.path.exists(file_path):
            return None
        
        # For now, return None to fall back to estimation
        # You could add audio library here if needed
        return None
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return None

def check_tts_api_status():
    """Check if TTS API is working"""
    if not NEW_TTS_API_KEY:
        return False, "API key not configured"
    
    try:
        url = f"{NEW_TTS_API_URL.rstrip('/')}/v1/text-to-speech"
        headers = {"xi-api-key": NEW_TTS_API_KEY, "Content-Type": "application/json"}
        payload = {"text": "test", "voice_id": DEFAULT_VOICE_ID, "model_id": NEW_TTS_MODEL_ID}
        
        response = requests.post(url, json=payload, headers=headers, timeout=8)
        
        if response.status_code == 200:
            return True, "API working"
        else:
            return False, f"API error: {response.status_code}"
            
    except Exception as e:
        return False, f"Connection error: {str(e)}"