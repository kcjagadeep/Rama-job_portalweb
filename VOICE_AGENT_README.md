# 🎤 Real-time Voice Agent System

A telephone-like conversation system with one-button activation for seamless AI interactions.

## ✨ Features

- **One-Button Activation**: Press once to start, press again to end
- **Real-time Speech Recognition**: Instant voice-to-text conversion
- **Natural AI Responses**: Context-aware conversation flow
- **High-Quality TTS**: Natural-sounding voice synthesis
- **Minimal Latency**: Optimized for real-time conversations
- **Mobile Responsive**: Works on all devices

## 🚀 Quick Start

### 1. Access the Demo
Visit: `http://your-domain/voice/demo/`

### 2. Test the System
Visit: `http://your-domain/voice/test-page/`

### 3. Add to Any Page
Include the widget in any template:
```html
{% include 'jobapp/voice_agent_widget.html' %}
```

## 📱 How to Use

1. **Click the floating voice button** (bottom-right corner)
2. **Allow microphone access** when prompted
3. **Start speaking naturally** - the AI will respond
4. **Wait for AI to finish** before speaking again
5. **Click button again** to end conversation

## 🔧 Technical Details

### Backend Components
- `voice_agent.py` - Core session management and AI integration
- `voice_views.py` - Demo and test views
- `voice_urls.py` - URL routing

### Frontend Components
- `voice-agent.js` - Main JavaScript class
- `voice_agent_widget.html` - Reusable widget template
- `voice_agent_demo.html` - Full demo page

### API Endpoints
- `POST /voice/start/` - Start new session
- `POST /voice/chat/` - Send message and get response
- `POST /voice/stop/` - End session
- `GET /voice/status/` - System status

## 🎯 Integration Examples

### Basic Integration
```html
<!-- Add to any template -->
{% load static %}
{% include 'jobapp/voice_agent_widget.html' %}
```

### Custom Integration
```javascript
// Initialize with custom options
const voiceAgent = new RealTimeVoiceAgent({
    autoStart: false,
    speechTimeout: 2000,
    maxSilence: 3000
});

// Manual control
voiceAgent.startSession();
voiceAgent.stopSession();
```

### Interview Integration
The voice agent is already integrated into:
- `interview_simple.html` - Main interview template

## 🔊 Audio Requirements

### Browser Support
- **Chrome** (recommended) - Best speech recognition
- **Edge** - Good speech recognition
- **Firefox** - Limited speech recognition
- **Safari** - Basic support

### Permissions Needed
- **Microphone access** - For speech input
- **Audio playback** - For AI responses

## 🛠️ Configuration

### Environment Variables
```bash
# TTS Configuration (already configured)
NEW_TTS_API_KEY=your_tts_api_key
NEW_TTS_API_URL=your_tts_endpoint
NEW_TTS_VOICE_ID=Daisy Studious

# AI Configuration (already configured)
NVIDIA_API_KEY=your_nvidia_api_key
```

### Customization Options
```javascript
// Voice agent configuration
{
    autoStart: false,        // Auto-start on page load
    speechTimeout: 2000,     // Silence before sending (ms)
    maxSilence: 3000,       // Max silence duration (ms)
}
```

## 🎨 UI Customization

### Button Styles
The voice button automatically changes appearance:
- **🎤 Blue gradient** - Ready to start
- **📞 Red gradient** - Active session
- **🔊 Orange gradient** - AI speaking
- **🎤 Blue pulsing** - Listening

### Status Indicators
- **Top notification** - Current status
- **Bottom transcript** - Conversation text
- **Button animation** - Visual feedback

## 🔍 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Try refreshing the page
   - Use Chrome or Edge

2. **No audio output**
   - Check speaker/headphone connection
   - Verify browser audio settings
   - Test with `/voice/test-page/`

3. **AI not responding**
   - Check network connection
   - Verify API keys in environment
   - Check browser console for errors

### Debug Mode
```javascript
// Enable debug logging
window.voiceAgent.debug = true;
```

## 📊 Performance

### Optimizations
- **Audio caching** - Reuses generated TTS files
- **Session management** - Efficient memory usage
- **Timeout handling** - Prevents hanging requests
- **Error recovery** - Graceful fallbacks

### Metrics
- **Speech recognition latency**: ~100-300ms
- **AI response time**: ~1-3 seconds
- **TTS generation**: ~500ms-2s
- **Total conversation turn**: ~2-5 seconds

## 🔐 Security

### Data Handling
- **No audio storage** - Speech processed in real-time
- **Session isolation** - Each conversation is separate
- **CSRF protection** - All API calls protected
- **Input validation** - Sanitized user inputs

## 🚀 Deployment

### Production Checklist
- [ ] Set environment variables
- [ ] Configure TTS service
- [ ] Test microphone permissions
- [ ] Verify HTTPS (required for microphone)
- [ ] Test on target browsers

### Scaling Considerations
- Use Redis for session storage in production
- Implement rate limiting for API calls
- Monitor TTS usage and costs
- Consider WebSocket for lower latency

## 📈 Future Enhancements

### Planned Features
- **WebSocket support** - Even lower latency
- **Voice interruption** - Stop AI mid-sentence
- **Multiple languages** - International support
- **Voice cloning** - Custom AI voices
- **Conversation analytics** - Usage metrics

### Integration Ideas
- **Customer support** - Help desk automation
- **Education** - Interactive tutoring
- **Healthcare** - Patient intake
- **Sales** - Lead qualification

## 🤝 Support

For issues or questions:
1. Check the test page: `/voice/test-page/`
2. Review browser console logs
3. Verify environment configuration
4. Test with different browsers

---

**Ready to talk to AI? Just press the button! 🎤**