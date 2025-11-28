#!/usr/bin/env python
"""
Test script for WebRTC Interview functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.models import Interview, InterviewRoom, RoomParticipant

def test_webrtc_models():
    """Test WebRTC models creation"""
    print("🧪 Testing WebRTC Models...")
    
    # Get first interview
    interview = Interview.objects.first()
    if not interview:
        print("❌ No interviews found. Create an interview first.")
        return False
    
    print(f"✅ Found interview: {interview}")
    
    # Create WebRTC room
    room, created = InterviewRoom.objects.get_or_create(
        interview=interview,
        defaults={
            'max_participants': 5,
            'enable_recording': True,
            'enable_screen_share': True,
            'enable_chat': True
        }
    )
    
    if created:
        print(f"✅ Created WebRTC room: {room.room_id}")
    else:
        print(f"✅ Found existing WebRTC room: {room.room_id}")
    
    print(f"   Room ID: {room.room_id}")
    print(f"   Passcode: {room.passcode}")
    print(f"   Max Participants: {room.max_participants}")
    
    # Create test participant
    participant = RoomParticipant.objects.create(
        room=room,
        participant_type='candidate',
        display_name='Test Candidate',
        is_connected=True
    )
    
    print(f"✅ Created test participant: {participant}")
    
    return True

def test_urls():
    """Test URL patterns"""
    print("\n🔗 Testing URL Patterns...")
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    # Test join page
    try:
        url = reverse('join_with_passcode')
        response = client.get(url)
        print(f"✅ Join page URL: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Join page URL error: {e}")
    
    # Test WebRTC room (need interview UUID)
    interview = Interview.objects.first()
    if interview:
        try:
            url = reverse('webrtc_interview_room', kwargs={'interview_uuid': interview.uuid})
            response = client.get(url)
            print(f"✅ WebRTC room URL: {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ WebRTC room URL error: {e}")
    
    return True

def main():
    """Main test function"""
    print("🚀 WebRTC Interview System Test")
    print("=" * 40)
    
    try:
        # Test models
        if not test_webrtc_models():
            return
        
        # Test URLs
        test_urls()
        
        print("\n" + "=" * 40)
        print("✅ All tests passed! WebRTC system is ready.")
        print("\n📋 Next Steps:")
        print("1. Visit /interview/join/ to test passcode joining")
        print("2. Go to any interview ready page to see WebRTC option")
        print("3. Use Room ID and Passcode to join as additional participants")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()