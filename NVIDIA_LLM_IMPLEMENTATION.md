# NVIDIA Llama-3.3-Nemotron-Super-49B-v1 Implementation

## Overview
This voice agent system is powered by NVIDIA's Llama-3.3-Nemotron-Super-49B-v1 model, providing intelligent conversational AI without any fallback or mock data.

## Model Details
- **Model**: `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Parameters**: 49 billion parameters
- **Provider**: NVIDIA AI Foundation Models
- **API Endpoint**: `https://integrate.api.nvidia.com/v1`

## Implementation Features

### ✅ No Fallback Data
- System requires valid NVIDIA API key
- Throws proper errors if API key is missing or invalid
- No mock responses or fallback mechanisms

### ✅ Real-time Voice Agent
- Accessible at: `http://127.0.0.1:8000/voice-agent/`
- One-button activation for telephone-like conversations
- Real-time speech recognition and TTS integration

### ✅ Performance Metrics
- Live latency monitoring for LLM and TTS
- Model information displayed in UI
- Performance tracking and optimization

## Configuration

### Environment Variables
Add to your `.env` file:
```
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### API Configuration
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Max Tokens**: 100 (concise responses)
- **Timeout**: 10 seconds
- **Stop Sequences**: Prevents unwanted formatting

## Usage

### 1. Access the Voice Agent
Navigate to: `http://127.0.0.1:8000/voice-agent/`

### 2. Start Conversation
- Click the floating microphone button
- Allow microphone access when prompted
- Start speaking naturally

### 3. Real-time Interaction
- AI responds using NVIDIA Llama-3.3-Nemotron model
- Conversation context is maintained
- Performance metrics shown in real-time

## API Endpoints

### Voice Session Management
- `POST /voice/start/` - Start new voice session
- `POST /voice/chat/` - Send message to AI
- `POST /voice/stop/` - End voice session
- `GET /voice/status/` - Check system status

### Response Format
```json
{
  "success": true,
  "text": "AI response text",
  "audio_url": "/media/tts/response.mp3",
  "audio_duration": 3.5,
  "session_active": true,
  "tts_latency": 850,
  "llm_latency": 1200,
  "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
  "voice": "Daisy Studious"
}
```

## Error Handling

### Missing API Key
```python
ValueError: "NVIDIA_API_KEY is required for LLM functionality"
```

### API Errors
```python
RuntimeError: "Failed to get response from NVIDIA Llama-3.3-Nemotron model: [error details]"
```

## Testing

### Run Test Script
```bash
python test_nvidia_llm.py
```

### Expected Output
```
🧪 Testing NVIDIA Llama-3.3-Nemotron-Super-49B-v1 Integration
============================================================
📝 Input: Hello, I'm a software developer with 5 years of Python experience.
🔄 Calling NVIDIA API...
✅ Success! Response: [AI response]
📊 Model: nvidia/llama-3.3-nemotron-super-49b-v1
🎯 Integration working correctly!
```

## File Structure

### Core Implementation
- `jobapp/utils/interview_ai_nvidia.py` - NVIDIA API integration
- `jobapp/voice_agent.py` - Voice session management
- `jobapp/voice_views.py` - Voice agent views
- `jobapp/voice_urls.py` - URL routing

### Frontend
- `templates/jobapp/voice_agent_demo.html` - Main UI
- `static/js/voice-agent.js` - Voice interaction logic
- `static/js/voice-metrics.js` - Performance monitoring

## Security Notes
- API key stored securely in environment variables
- CSRF protection enabled for all endpoints
- Proper error handling without exposing sensitive data

## Performance Optimization
- Optimized prompt engineering for concise responses
- Efficient conversation context management
- Real-time latency monitoring and optimization