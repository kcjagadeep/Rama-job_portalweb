"""
SIP Trunk Integration with Voice Agent
Minimal implementation for dialing and connecting to numbers
"""
try:
    import pjsua as pj
    PJSUA_AVAILABLE = True
except ImportError:
    # Mock pjsua for development when not installed
    PJSUA_AVAILABLE = False
    class MockPJ:
        class Lib:
            def init(self): pass
            def create_transport(self, *args): pass
            def start(self): pass
            def create_account(self, config): return MockAccount()
        
        class TransportConfig:
            def __init__(self): self.port = None
        
        class TransportType:
            UDP = 'udp'
        
        class AccountConfig:
            def __init__(self):
                self.id = None
                self.reg_uri = None
                self.auth_cred = []
        
        class AuthCred:
            def __init__(self, *args): pass
    
    class MockAccount:
        def make_call(self, uri): return MockCall()
    
    class MockCall:
        def hangup(self): pass
        def info(self): 
            class Info:
                state_text = "Connected"
            return Info()
    
    pj = MockPJ()

import threading
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

logger = logging.getLogger(__name__)

# SIP Configuration
SIP_USERNAME = "vwfQTeyF"  # Reg Number
SIP_DOMAIN = "pbx.voxbaysolutions.com"  # SIP Server
SIP_PORT = 5260  # SIP Port Number
SIP_PASSWORD = "@gV5LjvN@ZhMJH@"  # Password

class SIPTrunkManager:
    def __init__(self):
        self.lib = None
        self.account = None
        self.current_call = None
        self.is_initialized = False
        self.connection_status = "Not connected"
        
    def initialize(self):
        """Initialize SIP library and account"""
        try:
            if self.is_initialized:
                return True
            
            if not PJSUA_AVAILABLE:
                self.connection_status = f"Mock Connected to {SIP_DOMAIN}:{SIP_PORT} (User: {SIP_USERNAME})"
                logger.info(f"Mock SIP - Connected to {SIP_DOMAIN}:{SIP_PORT}")
                self.is_initialized = True
                return True
                
            self.lib = pj.Lib()
            self.lib.init()
            
            # Create UDP transport
            transport_cfg = pj.TransportConfig()
            transport_cfg.port = SIP_PORT
            self.lib.create_transport(pj.TransportType.UDP, transport_cfg)
            
            self.lib.start()
            
            # Create account
            acc_cfg = pj.AccountConfig()
            acc_cfg.id = f"sip:{SIP_USERNAME}@{SIP_DOMAIN}"
            acc_cfg.reg_uri = f"sip:{SIP_DOMAIN}"
            acc_cfg.auth_cred = [pj.AuthCred("*", SIP_USERNAME, SIP_PASSWORD)]
            
            self.account = self.lib.create_account(acc_cfg)
            self.is_initialized = True
            self.connection_status = f"Connected to {SIP_DOMAIN}:{SIP_PORT} (User: {SIP_USERNAME})"
            
            logger.info(f"SIP Trunk connected to {SIP_DOMAIN}:{SIP_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"SIP initialization failed: {e}")
            self.connection_status = f"Failed to connect to {SIP_DOMAIN}:{SIP_PORT}"
            return False
    
    def make_call(self, number):
        """Make outbound call to specified number"""
        try:
            if not self.is_initialized:
                if not self.initialize():
                    return False, "SIP not initialized"
            
            if self.current_call:
                return False, "Call already in progress"
            
            if not PJSUA_AVAILABLE:
                # Mock call for development
                self.current_call = f"mock_call_{number}"
                logger.info(f"Mock call initiated to {number}")
                return True, f"Mock calling {number}... (pjsua not installed)"
            
            # Make the real call
            call_uri = f"sip:{number}@{SIP_DOMAIN}"
            self.current_call = self.account.make_call(call_uri)
            
            logger.info(f"Call initiated to {number}")
            return True, f"Calling {number}..."
            
        except Exception as e:
            logger.error(f"Call failed: {e}")
            return False, str(e)
    
    def hangup_call(self):
        """End current call"""
        try:
            if self.current_call:
                if not PJSUA_AVAILABLE:
                    # Mock hangup
                    logger.info(f"Mock hangup for call: {self.current_call}")
                else:
                    self.current_call.hangup()
                self.current_call = None
                return True, "Call ended"
            return False, "No active call"
        except Exception as e:
            logger.error(f"Hangup failed: {e}")
            return False, str(e)
    
    def get_call_status(self):
        """Get current call status"""
        try:
            if not self.current_call:
                return "idle"
            
            if not PJSUA_AVAILABLE:
                return "connected"  # Mock status
            
            call_info = self.current_call.info()
            return call_info.state_text.lower()
        except:
            return "unknown"

# Global SIP manager instance
sip_manager = SIPTrunkManager()

@csrf_exempt
def sip_dial(request):
    """Dial a number via SIP trunk"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number = data.get('number', '').strip()
            
            if not number:
                return JsonResponse({
                    'success': False,
                    'message': 'Phone number is required'
                })
            
            success, message = sip_manager.make_call(number)
            
            return JsonResponse({
                'success': success,
                'message': message,
                'number': number
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'POST method required'})

@csrf_exempt
def sip_hangup(request):
    """Hangup current call"""
    if request.method == 'POST':
        success, message = sip_manager.hangup_call()
        return JsonResponse({
            'success': success,
            'message': message
        })
    
    return JsonResponse({'success': False, 'message': 'POST method required'})

@csrf_exempt
def sip_status(request):
    """Get SIP call status"""
    status = sip_manager.get_call_status()
    return JsonResponse({
        'success': True,
        'status': status,
        'has_active_call': sip_manager.current_call is not None
    })