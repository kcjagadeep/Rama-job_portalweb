import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Interview, InterviewRoom, RoomParticipant

def webrtc_interview_room(request, interview_uuid):
    """Main WebRTC interview room"""
    interview = get_object_or_404(Interview, uuid=interview_uuid)
    
    # Create or get WebRTC room
    room, created = InterviewRoom.objects.get_or_create(
        interview=interview,
        defaults={
            'max_participants': 10,
            'enable_recording': True,
            'enable_screen_share': True,
            'enable_chat': True
        }
    )
    
    # Determine participant type
    participant_type = 'guest'
    display_name = 'Guest User'
    
    if request.user.is_authenticated:
        if request.user == interview.candidate:
            participant_type = 'candidate'
            display_name = interview.candidate_name
        elif request.user == interview.job.posted_by:
            participant_type = 'recruiter'
            display_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        else:
            participant_type = 'observer'
            display_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
    else:
        if interview.candidate_name:
            participant_type = 'candidate'
            display_name = interview.candidate_name
    
    # Create participant record for video/audio tracking
    participant, created = RoomParticipant.objects.get_or_create(
        room=room,
        user=request.user if request.user.is_authenticated else None,
        participant_type=participant_type,
        display_name=display_name,
        defaults={
            'is_connected': True,
            'audio_enabled': True,
            'video_enabled': True
        }
    )
    if not created:
        participant.is_connected = True
        participant.save()
    
    context = {
        'interview': interview,
        'room': room,
        'participant_type': participant_type,
        'display_name': display_name,
        'room_config': {
            'room_id': room.room_id,
            'passcode': room.passcode,
            'max_participants': room.max_participants,
            'enable_recording': room.enable_recording,
            'enable_screen_share': room.enable_screen_share,
            'enable_chat': room.enable_chat,
        }
    }
    
    return render(request, 'jobapp/webrtc_interview.html', context)

def join_with_passcode(request):
    """Join room with passcode"""
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        passcode = request.POST.get('passcode')
        display_name = request.POST.get('display_name', 'Guest')
        
        try:
            room = InterviewRoom.objects.get(room_id=room_id, passcode=passcode)
            
            # Check if room is full (exclude disconnected participants)
            active_participants = room.participants.filter(is_connected=True).count()
            if active_participants >= room.max_participants:
                return JsonResponse({'error': f'Room is full ({active_participants}/{room.max_participants})'}, status=400)
            
            # Create participant
            participant = RoomParticipant.objects.create(
                room=room,
                user=request.user if request.user.is_authenticated else None,
                participant_type='guest',
                display_name=display_name,
                is_connected=True
            )
            
            return JsonResponse({
                'success': True,
                'room_url': f'/interview/webrtc/{room.interview.uuid}/',
                'participant_id': participant.id
            })
            
        except InterviewRoom.DoesNotExist:
            return JsonResponse({'error': 'Invalid room ID or passcode'}, status=400)
    
    return render(request, 'jobapp/join_interview.html')

@csrf_exempt
@require_http_methods(["POST"])
def webrtc_signaling(request):
    """WebRTC signaling server"""
    try:
        data = json.loads(request.body)
        message_type = data.get('type')
        room_id = data.get('room_id')
        
        room = get_object_or_404(InterviewRoom, room_id=room_id)
        
        if message_type == 'join':
            return handle_join(request, room, data)
        elif message_type == 'leave':
            return handle_leave(request, room, data)
        
        return JsonResponse({'success': True, 'message': f'{message_type} handled'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def handle_join(request, room, data):
    """Handle participant joining"""
    display_name = data.get('display_name', 'Guest')
    participant_type = data.get('participant_type', 'guest')
    
    # Check for existing participant
    existing_participant = room.participants.filter(
        display_name=display_name,
        participant_type=participant_type
    ).first()
    
    if existing_participant:
        existing_participant.is_connected = True
        existing_participant.save()
        participant = existing_participant
    else:
        # Create new participant
        participant = RoomParticipant.objects.create(
            room=room,
            user=request.user if request.user.is_authenticated else None,
            participant_type=participant_type,
            display_name=display_name,
            is_connected=True
        )
    
    # Get ALL connected participants (including self for verification)
    all_participants = room.participants.filter(
        is_connected=True
    ).values('id', 'display_name', 'participant_type')
    
    return JsonResponse({
        'success': True,
        'participant_id': participant.id,
        'participants': list(all_participants)
    })

def handle_leave(request, room, data):
    """Handle participant leaving"""
    participant_id = data.get('participant_id')
    
    try:
        participant = RoomParticipant.objects.get(id=participant_id, room=room)
        participant.is_connected = False
        participant.left_at = timezone.now()
        participant.save()
        
        return JsonResponse({'success': True})
        
    except RoomParticipant.DoesNotExist:
        return JsonResponse({'error': 'Participant not found'}, status=404)

@csrf_exempt
def get_room_info(request, room_id):
    """Get room information"""
    try:
        room = InterviewRoom.objects.get(room_id=room_id)
        participants = room.participants.filter(is_connected=True)
        
        return JsonResponse({
            'room_id': room.room_id,
            'interview_title': room.interview.job.title,
            'candidate_name': room.interview.candidate_name,
            'participants_count': participants.count(),
            'max_participants': room.max_participants,
            'is_active': room.is_active,
            'participants': [
                {
                    'id': p.id,
                    'display_name': p.display_name,
                    'participant_type': p.participant_type,
                    'joined_at': p.joined_at.isoformat(),
                    'audio_enabled': p.audio_enabled,
                    'video_enabled': p.video_enabled
                }
                for p in participants
            ]
        })
        
    except InterviewRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)