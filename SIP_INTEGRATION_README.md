# SIP Trunk Integration with Voice Agent

This implementation integrates SIP trunk functionality with the existing voice agent system, allowing you to make outbound calls and connect them to the AI voice agent.

## Features

- **Outbound Calling**: Dial phone numbers through SIP trunk
- **Voice Agent Integration**: Connect calls to AI voice agent
- **Real-time Status**: Monitor call status and connection
- **Mock Mode**: Development mode when pjsua is not installed

## Installation

### Option 1: Full SIP Installation (Production)

#### For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install libpjproject-dev python3-pjproject
pip install pjsua2
```

#### For macOS:
```bash
brew install pjproject
pip install pjsua2
```

#### For CentOS/RHEL:
```bash
sudo yum install pjproject-devel
pip install pjsua2
```

### Option 2: Development Mode (Mock SIP)

If you don't have pjsua installed, the system will automatically use mock mode for development and testing.

## Configuration

1. **SIP Credentials**: Update the SIP configuration in `jobapp/sip_trunk.py`:
   ```python
   SIP_USERNAME = "your_username"
   SIP_DOMAIN = "your_sip_domain.com"
   SIP_PORT = 5060  # or your SIP port
   SIP_PASSWORD = "your_password"
   ```

2. **Django Settings**: Add SIP password to your settings:
   ```python
   # In settings.py
   SIP_PASSWORD = "your_actual_sip_password"
   ```

## Usage

### Accessing the SIP Trunk Test Page

1. Navigate to: `http://your-domain/sip/`
2. Or use the navigation menu: **Pages > SIP Trunk Test**

### Making Calls

1. **Enter Number**: Use the dialer pad or type directly
2. **Call**: Click the green call button or press Enter
3. **Voice Agent**: The voice agent will automatically start when call connects
4. **Hangup**: Click the red hangup button or press Enter during call

### Quick Dial Presets

- Test Number 1: `1234567890`
- Test Number 2: `0987654321`
- You can modify these in the template

## API Endpoints

- `POST /sip/dial/` - Make outbound call
- `POST /sip/hangup/` - End current call
- `GET /sip/call-status/` - Get call status
- `GET /sip/status/` - Get system status

## Integration with Voice Agent

The SIP trunk automatically integrates with the existing voice agent system:

- **Auto-start**: Voice agent starts when call connects
- **Audio Bridge**: SIP audio is bridged to voice agent
- **Auto-stop**: Voice agent stops when call ends

## Troubleshooting

### pjsua Installation Issues

If you encounter issues installing pjsua:

1. **Check Dependencies**: Ensure you have the required system libraries
2. **Use Mock Mode**: The system works in development mode without pjsua
3. **Alternative Installation**: Try `pip install pjsua` (older version)

### SIP Connection Issues

1. **Check Credentials**: Verify SIP username, password, and domain
2. **Network**: Ensure SIP ports are not blocked by firewall
3. **Provider Settings**: Confirm settings with your SIP provider

### Audio Issues

1. **Permissions**: Ensure microphone permissions are granted
2. **Browser**: Use Chrome or Edge for best compatibility
3. **HTTPS**: Some audio features require HTTPS in production

## Development Notes

- **Mock Mode**: When pjsua is not available, the system uses mock calls for testing
- **Logging**: Check Django logs for SIP connection status
- **Testing**: Use the test endpoints to verify functionality

## Security Considerations

1. **Credentials**: Never commit SIP passwords to version control
2. **Environment Variables**: Use environment variables for sensitive data
3. **Network**: Secure SIP traffic with TLS when possible
4. **Access Control**: Restrict access to SIP functionality as needed

## File Structure

```
jobapp/
├── sip_trunk.py          # Core SIP functionality
├── sip_views.py          # Django views for SIP pages
├── sip_urls.py           # URL routing for SIP endpoints
└── templates/jobapp/
    └── sip_trunk_test.html  # SIP test interface
```

## Next Steps

1. **Production Setup**: Install pjsua and configure real SIP credentials
2. **Audio Quality**: Optimize audio settings for your use case
3. **Call Recording**: Add call recording functionality if needed
4. **Analytics**: Track call metrics and usage statistics
5. **Security**: Implement proper authentication and authorization

## Support

For issues or questions:
1. Check the Django logs for error messages
2. Verify SIP provider settings
3. Test with mock mode first
4. Ensure all dependencies are installed correctly