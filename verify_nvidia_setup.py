#!/usr/bin/env python3
"""
Verify NVIDIA LLM setup is correct
"""
import os
from decouple import config

def verify_nvidia_setup():
    """Verify NVIDIA setup"""
    print("🔍 Verifying NVIDIA LLM Setup")
    print("=" * 40)
    
    # Check environment file
    env_file = "/Users/kcjagadeep/Rama-job_portalweb/.env"
    if os.path.exists(env_file):
        print("✅ .env file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "NVIDIA_API_KEY" in content:
                print("✅ NVIDIA_API_KEY found in .env")
                if "your_nvidia_api_key_here" in content:
                    print("❌ NVIDIA_API_KEY is placeholder - needs real key")
                else:
                    print("✅ NVIDIA_API_KEY appears to be set")
            else:
                print("❌ NVIDIA_API_KEY not found in .env")
    else:
        print("❌ .env file not found")
    
    # Check if key can be loaded
    try:
        api_key = config('NVIDIA_API_KEY')
        if api_key and api_key != "your_nvidia_api_key_here":
            print("✅ NVIDIA_API_KEY loaded successfully")
            print(f"🔑 Key starts with: {api_key[:10]}...")
        else:
            print("❌ NVIDIA_API_KEY is empty or placeholder")
    except Exception as e:
        print(f"❌ Error loading NVIDIA_API_KEY: {e}")
    
    # Check voice agent files
    files_to_check = [
        "/Users/kcjagadeep/Rama-job_portalweb/jobapp/voice_agent.py",
        "/Users/kcjagadeep/Rama-job_portalweb/jobapp/utils/interview_ai_nvidia.py",
        "/Users/kcjagadeep/Rama-job_portalweb/templates/jobapp/voice_agent_demo.html"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {os.path.basename(file_path)} exists")
        else:
            print(f"❌ {os.path.basename(file_path)} missing")
    
    print("\n🎯 Setup Status:")
    print("1. Add your real NVIDIA API key to .env file")
    print("2. Access voice agent at: http://127.0.0.1:8000/voice-agent/")
    print("3. System will use NVIDIA Llama-3.3-Nemotron-Super-49B-v1 only")

if __name__ == "__main__":
    verify_nvidia_setup()