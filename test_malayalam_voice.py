#!/usr/bin/env python3
"""
Test script for Malayalam Voice Agent with IndicF5 TTS
"""
import os
import sys
import django

# Setup Django
sys.path.append('/Users/kcjagadeep/Rama-job_portalweb')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.malayalam_tts import check_malayalam_tts_status, generate_malayalam_tts

def test_malayalam_tts():
    """Test Malayalam TTS functionality"""
    print("🧪 Testing Malayalam IndicF5 TTS Integration...")
    print("=" * 50)
    
    # Test API status
    print("1. Checking Malayalam TTS API status...")
    status, message = check_malayalam_tts_status()
    print(f"   Status: {'✅ Working' if status else '❌ Failed'}")
    print(f"   Message: {message}")
    print()
    
    # Test TTS generation
    if status:
        print("2. Testing Malayalam TTS generation...")
        test_text = "നമസ്കാരം! ഞാൻ മലയാളം സംസാരിക്കുന്ന AI ആണ്."
        print(f"   Text: {test_text}")
        
        audio_url = generate_malayalam_tts(test_text)
        if audio_url:
            print(f"   ✅ Audio generated: {audio_url}")
        else:
            print("   ❌ Audio generation failed")
    else:
        print("2. ⏭️  Skipping TTS generation (API not available)")
    
    print()
    print("🔗 Malayalam Voice Agent URL: http://localhost:8000/malayalam-voice/")
    print("🔗 API Endpoint: http://34.232.76.115:8021/v2/tts")
    print("🤖 LLM Model: NVIDIA Llama-3.3-Nemotron")

if __name__ == "__main__":
    test_malayalam_tts()