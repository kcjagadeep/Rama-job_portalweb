"""
Views for SIP Trunk Test page
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def sip_trunk_test(request):
    """SIP Trunk Test page with voice agent integration"""
    return render(request, 'jobapp/webrtc_sip_test.html')

def sip_trunk_test_old(request):
    """Old SIP Trunk Test page"""
    from .sip_trunk import PJSUA_AVAILABLE, sip_manager
    
    # Initialize to get connection status
    sip_manager.initialize()
    
    context = {
        'title': 'SIP Trunk Test - Voice Agent',
        'page_description': 'Test SIP trunk integration with voice agent functionality',
        'pjsua_available': PJSUA_AVAILABLE,
        'sip_mode': 'Production' if PJSUA_AVAILABLE else 'Development (Mock)',
        'connection_status': sip_manager.connection_status
    }
    return render(request, 'jobapp/sip_trunk_test.html', context)

@csrf_exempt
def sip_test_status(request):
    """Test endpoint for SIP functionality"""
    return JsonResponse({
        'success': True,
        'status': 'SIP Trunk system operational',
        'features': [
            'Outbound calling',
            'Voice agent integration',
            'Real-time status monitoring',
            'Audio bridging'
        ]
    })