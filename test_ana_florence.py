#!/usr/bin/env python3
"""
Test Ana Florence voice
"""
import os
import sys
import django
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.tts import generate_tts

def test_ana_florence():
    print("🎤 Testing Ana Florence Voice")
    print("=" * 40)
    
    test_text = "Hello! I'm Ana Florence, your new AI assistant. How can I help you today?"
    
    audio_url = generate_tts(test_text)
    if audio_url:
        print(f"✅ Ana Florence voice generated: {audio_url}")
        
        file_path = f".{audio_url}"
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ Audio file: {file_size} bytes")
        else:
            print(f"❌ File not found: {file_path}")
    else:
        print("❌ Failed to generate Ana Florence voice")

if __name__ == "__main__":
    test_ana_florence()