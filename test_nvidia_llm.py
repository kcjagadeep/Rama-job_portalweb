#!/usr/bin/env python3
"""
Test script to verify NVIDIA Llama-3.3-Nemotron-Super-49B-v1 integration
"""
import os
import sys
import django

# Setup Django
sys.path.append('/Users/kcjagadeep/Rama-job_portalweb')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.utils.interview_ai_nvidia import ask_ai_question

def test_nvidia_llm():
    """Test NVIDIA LLM integration"""
    print("🧪 Testing NVIDIA Llama-3.3-Nemotron-Super-49B-v1 Integration")
    print("=" * 60)
    
    # Test prompt
    test_prompt = "Hello, I'm a software developer with 5 years of Python experience."
    
    try:
        print(f"📝 Input: {test_prompt}")
        print("🔄 Calling NVIDIA API...")
        
        response = ask_ai_question(
            prompt=test_prompt,
            candidate_name="Test User",
            job_title="Software Developer",
            company_name="Test Company"
        )
        
        print(f"✅ Success! Response: {response}")
        print(f"📊 Model: nvidia/llama-3.3-nemotron-super-49b-v1")
        print("🎯 Integration working correctly!")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Please set NVIDIA_API_KEY in your .env file")
        
    except RuntimeError as e:
        print(f"❌ Runtime Error: {e}")
        print("💡 Check your NVIDIA API key and network connection")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_nvidia_llm()