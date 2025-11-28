#!/usr/bin/env python
"""
Demo: WebRTC Multi-Participant Video/Audio Support
Shows how Recruiter, Observer, and Guest can join with video/audio
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from jobapp.models import Interview, InterviewRoom, RoomParticipant

def demo_participants():
    """Demo showing all participant types with video/audio"""
    print("🎥 WebRTC Multi-Participant Video/Audio Demo")
    print("=" * 50)
    
    # Get or create interview room
    interview = Interview.objects.first()
    if not interview:
        print("❌ No interviews found. Create an interview first.")
        return
    
    room, created = InterviewRoom.objects.get_or_create(
        interview=interview,
        defaults={'max_participants': 8}
    )
    
    print(f"🏠 Room: {room.room_id}")
    print(f"🔑 Passcode: {room.passcode}")
    print(f"📋 Interview: {interview.job.title}")
    print()
    
    # Clear existing participants for demo
    room.participants.all().delete()
    
    # Create different participant types
    participants = [
        {
            'type': 'candidate',
            'name': 'John Smith',
            'description': '✅ Main candidate - Full video/audio access'
        },
        {
            'type': 'recruiter', 
            'name': 'Sarah Johnson (HR)',
            'description': '✅ Job poster/HR - Full video/audio access'
        },
        {
            'type': 'observer',
            'name': 'Mike Chen (Tech Lead)',
            'description': '✅ Team member - Full video/audio access'
        },
        {
            'type': 'observer',
            'name': 'Lisa Wang (Manager)',
            'description': '✅ Additional observer - Full video/audio access'
        },
        {
            'type': 'guest',
            'name': 'Alex Brown (Consultant)',
            'description': '✅ External guest - Full video/audio access'
        }
    ]
    
    print("👥 PARTICIPANTS WITH VIDEO/AUDIO:")
    print("-" * 40)
    
    for i, p in enumerate(participants, 1):
        participant = RoomParticipant.objects.create(
            room=room,
            participant_type=p['type'],
            display_name=p['name'],
            is_connected=True,
            audio_enabled=True,
            video_enabled=True
        )
        
        print(f"{i}. {p['description']}")
        print(f"   Name: {p['name']}")
        print(f"   Type: {p['type'].upper()}")
        print(f"   Video: ✅ Enabled")
        print(f"   Audio: ✅ Enabled")
        print()
    
    print("🎯 HOW TO JOIN:")
    print("-" * 20)
    print("1. CANDIDATE:")
    print(f"   → Direct link: /interview/webrtc/{interview.uuid}/")
    print()
    print("2. RECRUITER/HR:")
    print(f"   → Login as job poster, visit: /interview/webrtc/{interview.uuid}/")
    print()
    print("3. OBSERVERS & GUESTS:")
    print("   → Visit: /interview/join/")
    print(f"   → Enter Room ID: {room.room_id}")
    print(f"   → Enter Passcode: {room.passcode}")
    print("   → Enter your name")
    print("   → Click 'Join Interview'")
    print()
    
    print("📱 FEATURES FOR ALL PARTICIPANTS:")
    print("-" * 35)
    print("✅ See everyone's video streams")
    print("✅ Hear everyone's audio")
    print("✅ Mute/unmute their own microphone")
    print("✅ Turn their video on/off")
    print("✅ Share their screen (if enabled)")
    print("✅ See participant list")
    print("✅ Leave the meeting")
    print()
    
    print("🎨 VISUAL INDICATORS:")
    print("-" * 20)
    print("🟢 Candidate - Green border")
    print("🔵 AI Interviewer - Blue border") 
    print("🟠 Recruiter/HR - Orange border")
    print("🟣 Observer - Purple border")
    print("⚫ Guest - Gray border")
    print()
    
    print("🚀 READY TO TEST!")
    print("Open multiple browser tabs/windows and join as different participants")

if __name__ == '__main__':
    demo_participants()