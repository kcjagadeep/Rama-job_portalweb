"""
WebRTC SIP Integration - Minimal Implementation
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

# SIP Configuration
SIP_USERNAME = "Ajtmv7fr"
SIP_DOMAIN = "pbx.voxbaysolutions.com"
SIP_PORT = 5260
SIP_PASSWORD = "@gV5LjvN@ZhMJH@"

class WebRTCSIPManager:
    def __init__(self):
        self.active_calls = {}
        self.connection_status = f"WebRTC Ready - {SIP_DOMAIN}:{SIP_PORT}"
    
    def get_sip_config(self):
        """Get SIP configuration for WebRTC client"""
        return {
            'username': SIP_USERNAME,
            'domain': SIP_DOMAIN,
            'port': SIP_PORT,
            'password': SIP_PASSWORD,
            'websocket_url': f'wss://{SIP_DOMAIN}:8089'
        }

webrtc_manager = WebRTCSIPManager()

@csrf_exempt
def webrtc_config(request):
    """Get WebRTC SIP configuration"""
    return JsonResponse({
        'success': True,
        'config': webrtc_manager.get_sip_config(),
        'status': webrtc_manager.connection_status
    })

@csrf_exempt
def webrtc_call_start(request):
    """Start WebRTC call"""
    if request.method == 'POST':
        data = json.loads(request.body)
        number = data.get('number')
        call_id = data.get('call_id')
        
        webrtc_manager.active_calls[call_id] = {
            'number': number,
            'status': 'calling'
        }
        
        return JsonResponse({
            'success': True,
            'message': f'WebRTC call started to {number}',
            'call_id': call_id
        })

@csrf_exempt
def webrtc_call_end(request):
    """End WebRTC call"""
    if request.method == 'POST':
        data = json.loads(request.body)
        call_id = data.get('call_id')
        
        if call_id in webrtc_manager.active_calls:
            del webrtc_manager.active_calls[call_id]
        
        return JsonResponse({
            'success': True,
            'message': 'Call ended'
        })