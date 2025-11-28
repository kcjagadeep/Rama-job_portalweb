# Malayalam Voice Agent Integration

## Overview
Successfully integrated a new Malayalam Voice Agent page with IndicF5 TTS and NVIDIA Llama-3.3-Nemotron integration.

## 🚀 Features Implemented

### 1. Malayalam IndicF5 TTS Service
- **File**: `jobapp/malayalam_tts.py`
- **API Endpoint**: `http://34.232.76.115:8021/v2/tts`
- **Features**:
  - Malayalam text-to-speech using IndicF5 v2 API
  - Audio caching for performance
  - Error handling with fallback mechanisms
  - Duration estimation for Malayalam text

### 2. Malayalam Voice Agent System
- **File**: `jobapp/malayalam_voice_agent.py`
- **Features**:
  - Session management for Malayalam conversations
  - Integration with NVIDIA Llama-3.3-Nemotron
  - Bilingual support (Malayalam + English)
  - Real-time conversation handling
  - Performance metrics tracking

### 3. Malayalam Voice Agent Views
- **File**: `jobapp/malayalam_voice_views.py`
- **Features**:
  - Main Malayalam voice agent page
  - System status checking
  - Test endpoints for debugging

### 4. Malayalam Voice Agent Template
- **File**: `templates/jobapp/malayalam_voice_agent.html`
- **Features**:
  - Beautiful Malayalam-themed UI
  - Bilingual instructions (Malayalam + English)
  - Real-time voice interaction
  - Speech recognition for Malayalam
  - Responsive design
  - Technical specifications display

### 5. URL Routing
- **File**: `jobapp/malayalam_voice_urls.py`
- **Endpoints**:
  - `/malayalam-voice/` - Main page
  - `/malayalam-voice/start/` - Start session
  - `/malayalam-voice/chat/` - Chat endpoint
  - `/malayalam-voice/stop/` - Stop session
  - `/malayalam-voice/status/` - System status
  - `/malayalam-voice/test/` - Test endpoint

## 🔧 Technical Specifications

### API Integration
- **TTS Service**: IndicF5 v2 API
- **Endpoint**: `http://34.232.76.115:8021/v2/tts`
- **Language**: Malayalam (മലയാളം)
- **Voice Model**: IndicF5
- **Audio Format**: WAV

### LLM Integration
- **Model**: NVIDIA Llama-3.3-Nemotron-70B-Instruct
- **Features**: Bilingual conversation support
- **Context**: Maintains conversation history
- **Fallback**: Graceful error handling

### Frontend Features
- **Speech Recognition**: Malayalam (ml-IN) + English
- **Audio Playback**: High-quality Malayalam TTS
- **UI Language**: Bilingual (Malayalam + English)
- **Responsive**: Mobile and desktop optimized

## 🌐 Access URLs

### Development
- **Malayalam Voice Agent**: `http://localhost:8000/malayalam-voice/`
- **Voice Agent Demo**: `http://localhost:8000/voice/demo/`
- **Home Page**: `http://localhost:8000/`

### Navigation
- Added to main navigation under "Pages" dropdown
- Direct access from home page menu

## 📋 API Endpoints

### Malayalam Voice Agent
```
POST /malayalam-voice/start/     # Start new session
POST /malayalam-voice/chat/      # Send message
POST /malayalam-voice/stop/      # Stop session
GET  /malayalam-voice/status/    # System status
GET  /malayalam-voice/test/      # Test endpoint
```

### Request/Response Format
```json
// Start Session
POST /malayalam-voice/start/
Response: {
  "success": true,
  "session_id": "malayalam_session_1234567890",
  "text": "നമസ്കാരം! ഞാൻ സാറയാണ്...",
  "audio_url": "/media/tts/malayalam_abc123.wav",
  "model": "nvidia/llama-3.3-nemotron-70b-instruct",
  "language": "malayalam"
}

// Chat
POST /malayalam-voice/chat/
Body: {
  "session_id": "malayalam_session_1234567890",
  "text": "എനിക്ക് ഒരു ജോലി വേണം"
}
Response: {
  "success": true,
  "text": "ഞാൻ നിങ്ങളെ സഹായിക്കാം...",
  "audio_url": "/media/tts/malayalam_def456.wav",
  "tts_latency": 1200,
  "llm_latency": 800
}
```

## 🧪 Testing

### Test Script
- **File**: `test_malayalam_voice.py`
- **Usage**: `python test_malayalam_voice.py`
- **Tests**: API connectivity, TTS generation, system status

### Manual Testing
1. Navigate to `http://localhost:8000/malayalam-voice/`
2. Click the green voice button
3. Allow microphone access
4. Speak in Malayalam or English
5. Listen to AI responses in Malayalam

## 🔄 Updates Made to Existing Code

### 1. Updated Voice Agent Model
- **File**: `jobapp/voice_agent.py`
- **Change**: Updated model name to `nvidia/llama-3.3-nemotron-70b-instruct`

### 2. Updated Voice Agent Demo Template
- **File**: `templates/jobapp/voice_agent_demo.html`
- **Change**: Updated model references to NVIDIA Llama-3.3-Nemotron

### 3. Added Navigation Links
- **File**: `templates/jobapp/home.html`
- **Change**: Added Malayalam Voice Agent link to Pages dropdown

### 4. Updated Main URLs
- **File**: `job_platform/urls.py`
- **Change**: Added Malayalam voice agent URL routing

## 🚨 Important Notes

### API Dependency
- The Malayalam TTS requires the IndicF5 API at `http://34.232.76.115:8021/`
- If API is unavailable, the system will gracefully handle errors
- Consider implementing fallback TTS if needed

### Browser Compatibility
- Requires modern browser with Web Speech API support
- Chrome/Edge recommended for best speech recognition
- Safari has limited Malayalam speech recognition

### Performance Considerations
- Audio files are cached in `/media/tts/` directory
- Session data stored in memory (consider Redis for production)
- TTS latency depends on API response time

## 🔮 Future Enhancements

1. **Offline TTS**: Implement local Malayalam TTS fallback
2. **Voice Cloning**: Add custom voice options
3. **Conversation Export**: Save Malayalam conversations
4. **Analytics**: Track usage metrics and performance
5. **Multi-dialect**: Support different Malayalam dialects

## 🎯 Success Criteria

✅ **Completed**:
- Malayalam IndicF5 TTS integration
- NVIDIA Llama-3.3-Nemotron integration
- Bilingual conversation support
- Real-time voice interaction
- Beautiful Malayalam-themed UI
- Complete URL routing and navigation
- Error handling and fallbacks
- Performance metrics tracking

The Malayalam Voice Agent is now fully integrated and ready for use!