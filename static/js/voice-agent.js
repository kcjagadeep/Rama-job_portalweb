/**
 * Real-time Voice Agent - One Button Activation
 * Provides telephone-like conversation experience
 */

class RealTimeVoiceAgent {
    constructor(options = {}) {
        this.sessionId = null;
        this.isActive = false;
        this.isListening = false;
        this.isSpeaking = false;
        this.recognition = null;
        this.audioElement = null;
        this.currentText = '';
        this.speechTimeout = null;
        this.userStream = null;
        
        // Configuration
        this.config = {
            autoStart: options.autoStart || false,
            speechTimeout: options.speechTimeout || 2000,
            maxSilence: options.maxSilence || 3000,
            ...options
        };
        
        // UI Elements
        this.button = null;
        this.statusDisplay = null;
        this.transcriptDisplay = null;
        
        this.init();
    }
    
    init() {
        this.setupUI();
        this.setupSpeechRecognition();
        this.setupAudio();
        
        if (this.config.autoStart) {
            this.startSession();
        }
    }
    
    async getUserMedia() {
        try {
            this.userStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            return true;
        } catch (error) {
            console.error('Microphone access error:', error);
            this.showStatus('❌ Microphone access required');
            return false;
        }
    }
    
    setupUI() {
        // Create main button
        this.button = document.createElement('button');
        this.button.id = 'voice-agent-btn';
        this.button.innerHTML = `
            <div class="voice-btn-content">
                <div class="voice-icon">🎤</div>
                <div class="voice-text">Talk to Agent</div>
            </div>
        `;
        this.button.onclick = () => this.toggleSession();
        
        // Create status display
        this.statusDisplay = document.createElement('div');
        this.statusDisplay.id = 'voice-status';
        this.statusDisplay.className = 'voice-status hidden';
        
        // Create transcript display
        this.transcriptDisplay = document.createElement('div');
        this.transcriptDisplay.id = 'voice-transcript';
        this.transcriptDisplay.className = 'voice-transcript hidden';
        
        // Add to page
        document.body.appendChild(this.button);
        document.body.appendChild(this.statusDisplay);
        document.body.appendChild(this.transcriptDisplay);
        
        // Load metrics display
        this.loadMetrics();
        
        this.addStyles();
    }
    
    loadMetrics() {
        const script = document.createElement('script');
        script.src = '/static/js/voice-metrics.js';
        document.head.appendChild(script);
    }
    
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #voice-agent-btn {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                transition: all 0.3s ease;
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            #voice-agent-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
            }
            
            #voice-agent-btn.active {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                animation: pulse 2s infinite;
            }
            
            #voice-agent-btn.listening {
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                animation: listening-pulse 1.5s infinite;
            }
            
            #voice-agent-btn.speaking {
                background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
                animation: speaking-wave 1s infinite;
            }
            
            #voice-agent-btn.muted {
                background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                opacity: 0.7;
            }
            
            .voice-btn-content {
                text-align: center;
            }
            
            .voice-icon {
                font-size: 24px;
                margin-bottom: 2px;
            }
            
            .voice-text {
                font-size: 10px;
                font-weight: 500;
                opacity: 0.9;
            }
            
            .voice-status {
                position: fixed;
                top: 30px;
                right: 30px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                font-size: 14px;
                font-weight: 500;
                z-index: 999;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            
            .voice-status.hidden {
                opacity: 0;
                transform: translateY(-20px);
                pointer-events: none;
            }
            
            .voice-transcript {
                position: fixed;
                bottom: 130px;
                right: 30px;
                left: 30px;
                max-width: 500px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 15px;
                padding: 20px;
                font-size: 16px;
                line-height: 1.5;
                z-index: 998;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }
            
            .voice-transcript.hidden {
                opacity: 0;
                transform: translateY(20px);
                pointer-events: none;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes listening-pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 8px 25px rgba(58, 123, 213, 0.3); }
                50% { transform: scale(1.1); box-shadow: 0 12px 35px rgba(58, 123, 213, 0.6); }
            }
            
            @keyframes speaking-wave {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.05) rotate(1deg); }
                75% { transform: scale(1.05) rotate(-1deg); }
            }
            
            @media (max-width: 768px) {
                #voice-agent-btn {
                    bottom: 20px;
                    right: 20px;
                    width: 70px;
                    height: 70px;
                }
                
                .voice-transcript {
                    bottom: 110px;
                    right: 20px;
                    left: 20px;
                }
                
                .voice-status {
                    top: 20px;
                    right: 20px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    setupSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            return;
        }
        
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI();
            this.showStatus('🎤 Listening... (Mic active)');
        };
        
        this.recognition.onend = () => {
            if (this.isActive && !this.isSpeaking) {
                // Restart recognition if session is active
                setTimeout(() => {
                    if (this.isActive && !this.isSpeaking) {
                        this.startListening();
                    }
                }, 100);
            } else {
                this.isListening = false;
                this.updateUI();
            }
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Show interim results
            if (interimTranscript) {
                this.showTranscript(`You: ${interimTranscript}`, true);
            }
            
            // Process final transcript
            if (finalTranscript.trim()) {
                this.currentText += finalTranscript;
                this.showTranscript(`You: ${finalTranscript}`);
                
                // Clear existing timeout
                if (this.speechTimeout) {
                    clearTimeout(this.speechTimeout);
                }
                
                // Set new timeout to send response
                this.speechTimeout = setTimeout(() => {
                    this.sendToAgent(this.currentText.trim());
                    this.currentText = '';
                }, this.config.speechTimeout);
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error === 'not-allowed') {
                this.showStatus('❌ Microphone access denied');
            }
        };
    }
    
    setupAudio() {
        this.audioElement = document.createElement('audio');
        this.audioElement.preload = 'auto';
        this.audioElement.volume = 1.0; // Maximum volume for louder AI voice
        
        this.audioElement.onplay = () => {
            this.isSpeaking = true;
            this.muteUserMicrophone();
            this.stopListening();
            this.updateUI();
            this.showStatus('🔊 Agent speaking... (Mic muted)');
        };
        
        this.audioElement.onended = () => {
            this.isSpeaking = false;
            this.unmuteUserMicrophone();
            this.updateUI();
            
            // Resume listening after agent finishes speaking
            if (this.isActive) {
                setTimeout(() => {
                    this.startListening();
                }, 300);
            }
        };
    }
    
    async toggleSession() {
        if (this.isActive) {
            await this.stopSession();
        } else {
            await this.startSession();
        }
    }
    
    async startSession() {
        try {
            this.showStatus('🔄 Starting session...');
            
            // Get user media for microphone control
            await this.getUserMedia();
            
            const response = await fetch('/voice/start/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    session_id: `session_${Date.now()}`
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.sessionId = data.session_id;
                this.isActive = true;
                this.updateUI();
                
                // Play welcome message
                if (data.audio_url) {
                    this.playAudio(data.audio_url);
                }
                
                this.showTranscript(`Agent: ${data.text}`);
                this.showStatus('✅ Session active');
                
                // Start listening after welcome message
                setTimeout(() => {
                    if (this.isActive) {
                        this.startListening();
                    }
                }, (data.audio_duration || 3) * 1000 + 500);
                
            } else {
                this.showStatus('❌ Failed to start session');
                console.error('Failed to start session:', data.error);
            }
            
        } catch (error) {
            this.showStatus('❌ Connection error');
            console.error('Session start error:', error);
        }
    }
    
    async stopSession() {
        try {
            this.isActive = false;
            this.stopListening();
            this.updateUI();
            
            // Stop user media stream
            if (this.userStream) {
                this.userStream.getTracks().forEach(track => track.stop());
                this.userStream = null;
            }
            
            if (this.sessionId) {
                await fetch('/voice/stop/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({
                        session_id: this.sessionId
                    })
                });
            }
            
            this.sessionId = null;
            this.hideStatus();
            this.hideTranscript();
            
        } catch (error) {
            console.error('Session stop error:', error);
        }
    }
    
    async sendToAgent(text) {
        if (!this.sessionId || !text.trim()) return;
        
        const startTime = performance.now();
        
        try {
            this.showStatus('🤔 Agent thinking...');
            
            // Get selected voice from radio buttons
            const selectedVoiceRadio = document.querySelector('input[name="voice"]:checked');
            const selectedVoice = selectedVoiceRadio ? selectedVoiceRadio.value : 'Ana Florence';
            
            const response = await fetch('/voice/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    text: text,
                    voice: selectedVoice
                })
            });
            
            const data = await response.json();
            const totalLatency = Math.round(performance.now() - startTime);
            
            if (data.success) {
                this.showTranscript(`Agent: ${data.text}`);
                
                // Update metrics
                if (window.voiceMetrics) {
                    window.voiceMetrics.updateMetrics({
                        ttsLatency: data.tts_latency || 0,
                        llmLatency: data.llm_latency || 0,
                        totalLatency: totalLatency,
                        model: data.model || 'nvidia/llama-3.3-nemotron-super-49b-v1'
                    });
                }
                
                if (data.audio_url) {
                    this.playAudio(data.audio_url);
                }
            } else {
                this.showStatus('❌ NVIDIA Model Error');
                console.error('NVIDIA Llama-3.3-Nemotron error:', data.error);
                // Show model info in error
                if (data.model) {
                    console.log('Model used:', data.model);
                }
            }
            
        } catch (error) {
            this.showStatus('❌ Connection error');
            console.error('Send to agent error:', error);
        }
    }
    
    startListening() {
        if (this.recognition && !this.isListening && !this.isSpeaking) {
            try {
                this.unmuteUserMicrophone();
                this.recognition.start();
            } catch (error) {
                if (error.name !== 'InvalidStateError') {
                    console.error('Start listening error:', error);
                }
            }
        }
    }
    
    muteUserMicrophone() {
        if (this.userStream) {
            this.userStream.getAudioTracks().forEach(track => {
                track.enabled = false;
            });
        }
    }
    
    unmuteUserMicrophone() {
        if (this.userStream) {
            this.userStream.getAudioTracks().forEach(track => {
                track.enabled = true;
            });
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
        }
    }
    
    playAudio(audioUrl) {
        if (this.audioElement) {
            this.audioElement.src = audioUrl.startsWith('/') ? audioUrl : `/media/${audioUrl}`;
            this.audioElement.volume = 1.0; // Ensure maximum volume
            this.audioElement.play().catch(error => {
                console.error('Audio play error:', error);
            });
        }
    }
    
    updateUI() {
        this.button.className = '';
        
        if (this.isActive) {
            this.button.classList.add('active');
            this.button.innerHTML = `
                <div class="voice-btn-content">
                    <div class="voice-icon">📞</div>
                    <div class="voice-text">End Call</div>
                </div>
            `;
        }
        
        if (this.isListening) {
            this.button.classList.add('listening');
        }
        
        if (this.isSpeaking) {
            this.button.classList.add('speaking');
            this.button.classList.add('muted');
        } else {
            this.button.classList.remove('muted');
        }
        
        if (!this.isActive) {
            this.button.innerHTML = `
                <div class="voice-btn-content">
                    <div class="voice-icon">🎤</div>
                    <div class="voice-text">Talk to Agent</div>
                </div>
            `;
        }
    }
    
    showStatus(message) {
        this.statusDisplay.textContent = message;
        this.statusDisplay.classList.remove('hidden');
        
        // Auto-hide after 3 seconds for non-persistent messages
        if (!message.includes('Listening') && !message.includes('speaking')) {
            setTimeout(() => {
                if (this.statusDisplay.textContent === message) {
                    this.hideStatus();
                }
            }, 3000);
        }
    }
    
    hideStatus() {
        this.statusDisplay.classList.add('hidden');
    }
    
    showTranscript(text, isInterim = false) {
        if (isInterim) {
            this.transcriptDisplay.innerHTML = `<div style="opacity: 0.7; font-style: italic;">${text}</div>`;
        } else {
            this.transcriptDisplay.innerHTML = text;
        }
        
        this.transcriptDisplay.classList.remove('hidden');
        
        // Auto-hide transcript after 5 seconds
        setTimeout(() => {
            if (!isInterim) {
                this.hideTranscript();
            }
        }, 5000);
    }
    
    hideTranscript() {
        this.transcriptDisplay.classList.add('hidden');
    }
    
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        
        // Fallback: try to get from meta tag
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            return csrfMeta.getAttribute('content');
        }
        
        // Fallback: try to get from form
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            return csrfInput.value;
        }
        
        return '';
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if not already present
    if (!window.voiceAgent) {
        window.voiceAgent = new RealTimeVoiceAgent({
            autoStart: false,
            speechTimeout: 2000
        });
    }
});

// Export for manual initialization
window.RealTimeVoiceAgent = RealTimeVoiceAgent;