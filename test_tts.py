#!/usr/bin/env python3
"""
Test TTS functionality
"""
import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.tts import generate_tts, generate_google_tts, check_tts_api_status

def test_tts():
    """Test TTS functionality"""
    print("🎤 Testing TTS Systems")
    print("=" * 50)
    
    test_text = "Hello, this is a test of the text to speech system using Rachel voice."
    
    # Test 1: Check API status
    print("1. Checking TTS API Status...")
    try:
        status, message = check_tts_api_status()
        print(f"   Status: {'✅' if status else '❌'} {message}")
    except Exception as e:
        print(f"   ❌ Status check failed: {e}")
    
    # Test 2: Generate TTS with primary system
    print("\n2. Testing Primary TTS (Rachel voice)...")
    try:
        audio_url = generate_tts(test_text)
        if audio_url:
            print(f"   ✅ Generated: {audio_url}")
            # Check if file exists
            file_path = f"media{audio_url}" if not audio_url.startswith('/') else f".{audio_url}"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   ✅ File exists: {file_size} bytes")
            else:
                print(f"   ❌ File not found: {file_path}")
        else:
            print("   ❌ No audio generated")
    except Exception as e:
        print(f"   ❌ Primary TTS failed: {e}")
    
    # Test 3: Test Google TTS fallback
    print("\n3. Testing Google TTS Fallback...")
    try:
        audio_url = generate_google_tts(test_text)
        if audio_url:
            print(f"   ✅ Generated: {audio_url}")
            file_path = f"media{audio_url}" if not audio_url.startswith('/') else f".{audio_url}"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   ✅ File exists: {file_size} bytes")
            else:
                print(f"   ❌ File not found: {file_path}")
        else:
            print("   ❌ No audio generated")
    except Exception as e:
        print(f"   ❌ Google TTS failed: {e}")
    
    # Test 4: Test different voices
    print("\n4. Testing Different Voices...")
    voices = ["Rachel", "Drew", "Clyde", "female_interview"]
    
    for voice in voices:
        try:
            # Temporarily set voice for testing
            from jobapp import tts
            original_voice = tts.DAISY_VOICE_ID
            tts.DAISY_VOICE_ID = voice
            
            audio_url = generate_tts(f"Testing {voice} voice", voice)
            if audio_url:
                print(f"   ✅ {voice}: Generated successfully")
            else:
                print(f"   ❌ {voice}: Failed to generate")
                
            # Restore original voice
            tts.DAISY_VOICE_ID = original_voice
            
        except Exception as e:
            print(f"   ❌ {voice}: Error - {e}")
    
    print("\n🎯 TTS Test Complete!")

if __name__ == "__main__":
    test_tts()