#!/usr/bin/env python
"""
Test script to verify face detection is working
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.utils.face_tracker import FaceTracker
import cv2
import base64
import numpy as np

def test_face_detection():
    print("🧪 Testing Face Detection System")
    print("=" * 50)
    
    # Test 1: Initialize tracker
    print("1. Initializing FaceTracker...")
    tracker = FaceTracker()
    
    if tracker.face_cascade is None:
        print("❌ Face cascade not loaded")
        return False
    else:
        print("✅ Face cascade loaded successfully")
    
    # Test 2: Create a test image with a face-like pattern
    print("\n2. Creating test image...")
    
    # Create a simple test image (100x100 pixels)
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    test_img.fill(128)  # Gray background
    
    # Add a simple face-like pattern (rectangle for face, circles for eyes)
    cv2.rectangle(test_img, (30, 30), (70, 80), (200, 200, 200), -1)  # Face
    cv2.circle(test_img, (40, 45), 3, (0, 0, 0), -1)  # Left eye
    cv2.circle(test_img, (60, 45), 3, (0, 0, 0), -1)  # Right eye
    cv2.rectangle(test_img, (45, 60), (55, 65), (0, 0, 0), -1)  # Mouth
    
    # Convert to base64
    _, buffer = cv2.imencode('.jpg', test_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    frame_data = f"data:image/jpeg;base64,{img_base64}"
    
    print("✅ Test image created")
    
    # Test 3: Process the frame
    print("\n3. Processing frame...")
    result = tracker.process_frame(frame_data)
    
    print(f"Result: {result}")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    else:
        print(f"✅ Processed successfully - Found {result['count']} faces")
        return True

def test_api_endpoint():
    print("\n🌐 Testing API Endpoint")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.contrib.auth import get_user_model
        
        client = Client()
        
        # Create test data
        test_img = np.zeros((50, 50, 3), dtype=np.uint8)
        test_img.fill(128)
        
        _, buffer = cv2.imencode('.jpg', test_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        frame_data = f"data:image/jpeg;base64,{img_base64}"
        
        # Test API call
        response = client.post('/api/face-detect/', 
                             data={'frame': frame_data},
                             content_type='application/json')
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API working - Response: {result}")
            return True
        else:
            print(f"❌ API failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Face Detection System Test")
    print("=" * 60)
    
    # Run tests
    backend_ok = test_face_detection()
    api_ok = test_api_endpoint()
    
    print("\n📊 Test Results")
    print("=" * 30)
    print(f"Backend Face Detection: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"API Endpoint: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if backend_ok and api_ok:
        print("\n🎉 Face detection system is working correctly!")
        print("\n📝 To test in browser:")
        print("1. Start server: python manage.py runserver")
        print("2. Go to interview page")
        print("3. Check browser console for face detection logs")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")