# SIP Testing Guide - Where Calls Land

## 🎯 Call Flow Overview

When you make a call through this SIP integration:

```
Your App → VoxBay SIP Server → Destination Phone
```

## 📞 Where Calls Land

### Current Configuration:
- **SIP Server**: `pbx.voxbaysolutions.com:5260`
- **Account**: `vwfQTeyF@pbx.voxbaysolutions.com`
- **Provider**: VoxBay Solutions

### Call Destinations:
1. **Outbound Calls**: Go to real phone numbers via VoxBay's network
2. **Test Numbers**: Use these for safe testing:
   - `1234567890` - Mock test number
   - Your own mobile number for real testing

## 🧪 Testing Methods

### 1. Web Interface Testing
```bash
# Start Django server
python manage.py runserver

# Navigate to: http://localhost:8000/sip/
# Use the web interface to dial numbers
```

### 2. API Testing
```bash
# Test dial endpoint
curl -X POST http://localhost:8000/sip/dial/ \
  -H "Content-Type: application/json" \
  -d '{"number": "YOUR_PHONE_NUMBER"}'

# Check call status
curl http://localhost:8000/sip/call-status/

# Hangup call
curl -X POST http://localhost:8000/sip/hangup/
```

### 3. Python Script Testing
```bash
python test_sip_integration.py
```

## ⚠️ Important Notes

### Mock Mode (Current):
- Calls are simulated (pjsua not installed)
- No real calls are made
- Safe for development testing

### Production Mode:
- Install: `pip install pjsua`
- Real calls will be made to actual phone numbers
- **Charges apply** through VoxBay Solutions

## 🔧 Real Testing Steps

### Step 1: Install Production Library
```bash
# For real SIP calls (optional)
pip install pjsua
```

### Step 2: Test with Your Phone
1. Use your own mobile number for testing
2. Call should ring on your phone
3. Answer to test audio quality

### Step 3: Monitor Call Logs
- Check VoxBay Solutions dashboard for call logs
- Monitor billing/usage

## 🚨 Safety Measures

1. **Always test with your own number first**
2. **Check VoxBay billing before bulk testing**
3. **Use mock mode for development**
4. **Implement rate limiting for production**

## 📊 Call Status Meanings

- `idle` - No active call
- `calling` - Call being initiated
- `connected` - Call answered
- `disconnected` - Call ended
- `failed` - Call failed to connect

## 🔍 Troubleshooting

### Common Issues:
1. **"Mock calling"** - pjsua not installed (development mode)
2. **Connection failed** - Check VoxBay credentials
3. **No audio** - Check firewall/NAT settings
4. **Call drops** - Network connectivity issues

### Debug Commands:
```bash
# Check SIP registration
python -c "from jobapp.sip_trunk import sip_manager; sip_manager.initialize(); print(sip_manager.connection_status)"

# Test call without web interface
python -c "from jobapp.sip_trunk import sip_manager; print(sip_manager.make_call('YOUR_NUMBER'))"
```