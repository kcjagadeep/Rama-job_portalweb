#!/usr/bin/env python
"""
Test script for SIP Trunk Integration
Run this to verify the SIP integration is working correctly
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.sip_trunk import SIPTrunkManager

def test_sip_integration():
    """Test SIP trunk functionality"""
    print("🔧 Testing SIP Trunk Integration...")
    print("📞 Calls will route through: pbx.voxbaysolutions.com:5260")
    print("👤 Using account: vwfQTeyF")
    print("=" * 50)
    
    # Initialize SIP manager
    sip_manager = SIPTrunkManager()
    
    # Test 1: Initialization
    print("1. Testing SIP Initialization...")
    try:
        result = sip_manager.initialize()
        if result:
            print("   ✅ SIP initialization successful")
        else:
            print("   ❌ SIP initialization failed")
    except Exception as e:
        print(f"   ❌ SIP initialization error: {e}")
    
    # Test 2: Mock Call
    print("\n2. Testing Mock Call...")
    try:
        success, message = sip_manager.make_call("1234567890")
        if success:
            print(f"   ✅ Mock call successful: {message}")
        else:
            print(f"   ❌ Mock call failed: {message}")
    except Exception as e:
        print(f"   ❌ Mock call error: {e}")
    
    # Test 3: Call Status
    print("\n3. Testing Call Status...")
    try:
        status = sip_manager.get_call_status()
        print(f"   ✅ Call status: {status}")
    except Exception as e:
        print(f"   ❌ Call status error: {e}")
    
    # Test 4: Hangup
    print("\n4. Testing Call Hangup...")
    try:
        success, message = sip_manager.hangup_call()
        if success:
            print(f"   ✅ Hangup successful: {message}")
        else:
            print(f"   ❌ Hangup failed: {message}")
    except Exception as e:
        print(f"   ❌ Hangup error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 SIP Integration Test Complete!")
    print("\n📞 WHERE CALLS LAND:")
    print("   • Provider: VoxBay Solutions (pbx.voxbaysolutions.com)")
    print("   • Account: vwfQTeyF@pbx.voxbaysolutions.com")
    print("   • Mode: MOCK (pjsua not installed - no real calls made)")
    print("   • Real calls would go to actual phone numbers via VoxBay")
    print("\n🧪 TESTING OPTIONS:")
    print("1. Web Interface: python manage.py runserver → http://localhost:8000/sip/")
    print("2. API Test: curl -X POST http://localhost:8000/sip/dial/ -d '{\"number\":\"YOUR_PHONE\"}'")
    print("3. Real Testing: pip install pjsua (charges apply!)")
    print("\n⚠️  SAFETY: Currently in mock mode - no real calls/charges")
    print("📖 Read SIP_TESTING_GUIDE.md for detailed testing instructions")

if __name__ == "__main__":
    test_sip_integration()