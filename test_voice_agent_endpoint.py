#!/usr/bin/env python3
"""
Test script to verify voice agent endpoint is using NVIDIA LLM
"""
import requests
import json

def test_voice_agent_endpoints():
    """Test voice agent endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Voice Agent Endpoints")
    print("=" * 50)
    
    # Test 1: Check voice agent page loads
    try:
        response = requests.get(f"{base_url}/voice-agent/")
        print(f"✅ Voice Agent Page: {response.status_code}")
        if "NVIDIA Llama-3.3-Nemotron" in response.text:
            print("✅ Page shows NVIDIA model")
        else:
            print("❌ Page doesn't mention NVIDIA model")
    except Exception as e:
        print(f"❌ Voice Agent Page Error: {e}")
    
    # Test 2: Start voice session
    try:
        session_data = {"session_id": "test_session_123"}
        response = requests.post(
            f"{base_url}/voice/start/",
            json=session_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Start Session: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("model") == "nvidia/llama-3.3-nemotron-super-49b-v1":
                print("✅ Session returns correct NVIDIA model")
            else:
                print(f"❌ Session returns wrong model: {data.get('model')}")
        
    except Exception as e:
        print(f"❌ Start Session Error: {e}")
    
    # Test 3: Send chat message
    try:
        chat_data = {
            "session_id": "test_session_123",
            "text": "Hello, what model are you using?"
        }
        response = requests.post(
            f"{base_url}/voice/chat/",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Chat Message: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ Chat Response: {data.get('text', 'No text')[:100]}...")
                if data.get("model") == "nvidia/llama-3.3-nemotron-super-49b-v1":
                    print("✅ Chat returns correct NVIDIA model")
                else:
                    print(f"❌ Chat returns wrong model: {data.get('model')}")
            else:
                print(f"❌ Chat failed: {data.get('error')}")
        
    except Exception as e:
        print(f"❌ Chat Message Error: {e}")
    
    print("\n🎯 Test Complete!")
    print("If you see 'I understand you mentioned' responses, the system is using fallbacks.")
    print("Proper NVIDIA responses should be more natural and conversational.")

if __name__ == "__main__":
    test_voice_agent_endpoints()