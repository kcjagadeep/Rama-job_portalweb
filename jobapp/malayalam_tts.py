"""
Malayalam IndicF5 TTS Service
Integrates with http://34.232.76.115:8021/ for Malayalam text-to-speech
"""
import requests
import os
import hashlib
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Malayalam IndicF5 API Configuration
MALAYALAM_TTS_API_URL = "http://34.232.76.115:8021"
MALAYALAM_TTS_ENDPOINT = f"{MALAYALAM_TTS_API_URL}/v2/speech"

def generate_malayalam_tts(text, voice_id="malayalam_female"):
    """Generate Malayalam TTS using IndicF5 v2 API"""
    try:
        # Create filename for caching
        text_hash = hashlib.md5(f"{text}_malayalam".encode()).hexdigest()[:10]
        filename = f"malayalam_{text_hash}.wav"
        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
        os.makedirs(tts_dir, exist_ok=True)
        filepath = os.path.join(tts_dir, filename)
        
        # Check cache first
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/media/tts/{filename}"
        
        # Prepare API request for IndicF5 v2
        headers = {
            "Content-Type": "application/json",
            "Accept": "audio/wav"
        }
        
        payload = {
            "text": text.strip(),
            "voice_id": "malayalam_female",
            "model_id": "indicf5",
            "language": "ml"
        }
        
        logger.info(f"Requesting Malayalam TTS for: {text[:50]}...")
        
        response = requests.post(
            MALAYALAM_TTS_ENDPOINT, 
            json=payload, 
            headers=headers, 
            timeout=30
        )
        
        if response.status_code == 200:
            # Save audio file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                logger.info(f"Malayalam TTS generated successfully: {filename}")
                return f"/media/tts/{filename}"
            else:
                logger.error("Generated Malayalam audio file is too small")
                return None
        else:
            logger.error(f"Malayalam TTS API error: {response.status_code} - {response.text}")
            return None
        
    except Exception as e:
        logger.error(f"Malayalam TTS generation failed: {e}")
        return None

def check_malayalam_tts_status():
    """Check if Malayalam IndicF5 TTS API is working"""
    try:
        test_payload = {
            "text": "നമസ്കാരം",
            "voice_id": "malayalam_female",
            "model_id": "indicf5",
            "language": "ml"
        }
        
        response = requests.post(
            MALAYALAM_TTS_ENDPOINT,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Malayalam IndicF5 API working"
        else:
            return False, f"API error: {response.status_code}"
            
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def estimate_malayalam_audio_duration(text):
    """Estimate audio duration for Malayalam text"""
    # Malayalam has different speaking patterns
    # Average speaking rate is about 120-140 words per minute for Malayalam
    words = len(text.split())
    if words == 0:
        return 3.0
    
    # Estimate duration in seconds (130 words per minute for Malayalam)
    duration = (words / 130) * 60
    return max(3.0, min(duration, 45.0))  # Between 3-45 seconds