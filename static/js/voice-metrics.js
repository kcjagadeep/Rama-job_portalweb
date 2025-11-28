/**
 * Real-time Voice Agent Metrics Display
 */

class VoiceMetrics {
    constructor() {
        this.metrics = {
            ttsLatency: 0,
            llmLatency: 0,
            totalLatency: 0,
            model: 'nvidia/llama-3.3-nemotron-super-49b-v1',
            voice: 'Daisy Studious',
            avgTtsLatency: 0,
            avgLlmLatency: 0,
            avgTotalLatency: 0,
            sessionCount: 0
        };
        this.createMetricsDisplay();
    }
    
    createMetricsDisplay() {
        const display = document.createElement('div');
        display.id = 'voice-metrics';
        display.innerHTML = `
            <div class="metrics-header">🎤 Real-time Voice Call Agent</div>
            <div class="model-info">
                <div class="model-item">
                    <span class="model-label">🤖 AI Model:</span>
                    <span class="model-name" id="model-name">nvidia/llama-3.3-nemotron-super-49b-v1</span>
                </div>
                <div class="model-item">
                    <span class="model-label">🔊 Voice:</span>
                    <span class="voice-name" id="voice-name">Daisy Studious (Female)</span>
                </div>
            </div>
            <div class="metrics-grid">
                <div class="metric-item">
                    <span class="metric-label">TTS Latency:</span>
                    <span class="metric-value" id="tts-latency">${this.metrics.ttsLatency}ms</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">LLM Latency:</span>
                    <span class="metric-value" id="llm-latency">${this.metrics.llmLatency}ms</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Total Latency:</span>
                    <span class="metric-value" id="total-latency">${this.metrics.totalLatency}ms</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Avg Total:</span>
                    <span class="metric-value" id="avg-total">${this.metrics.avgTotalLatency}ms</span>
                </div>
            </div>
        `;
        
        document.body.appendChild(display);
        this.addMetricsStyles();
    }
    
    addMetricsStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #voice-metrics {
                position: fixed;
                top: 20px;
                left: 20px;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                z-index: 10000;
                min-width: 280px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .metrics-header {
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
                color: #00ff88;
                font-size: 14px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                padding-bottom: 8px;
            }
            
            .model-info {
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .model-item {
                display: flex;
                flex-direction: column;
                margin-bottom: 8px;
            }
            
            .model-label {
                color: #aaa;
                font-size: 11px;
                margin-bottom: 2px;
            }
            
            .model-name, .voice-name {
                color: #00ff88;
                font-weight: bold;
                font-size: 12px;
                word-break: break-all;
            }
            
            .metrics-grid {
                display: grid;
                gap: 5px;
            }
            
            .metric-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .metric-label {
                color: #ccc;
            }
            
            .metric-value {
                color: #00ff88;
                font-weight: bold;
                min-width: 80px;
                text-align: right;
            }
            
            .metric-value.high-latency {
                color: #ff6b6b;
            }
            
            .metric-value.medium-latency {
                color: #ffa500;
            }
            
            @media (max-width: 768px) {
                #voice-metrics {
                    top: 10px;
                    left: 10px;
                    right: 10px;
                    min-width: auto;
                    font-size: 11px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    updateMetrics(data) {
        const { ttsLatency, llmLatency, totalLatency } = data;
        
        this.metrics.ttsLatency = ttsLatency || 0;
        this.metrics.llmLatency = llmLatency || 0;
        this.metrics.totalLatency = totalLatency || 0;
        this.metrics.sessionCount++;
        
        // Calculate averages
        this.metrics.avgTtsLatency = Math.round(
            (this.metrics.avgTtsLatency * (this.metrics.sessionCount - 1) + this.metrics.ttsLatency) / this.metrics.sessionCount
        );
        this.metrics.avgLlmLatency = Math.round(
            (this.metrics.avgLlmLatency * (this.metrics.sessionCount - 1) + this.metrics.llmLatency) / this.metrics.sessionCount
        );
        this.metrics.avgTotalLatency = Math.round(
            (this.metrics.avgTotalLatency * (this.metrics.sessionCount - 1) + this.metrics.totalLatency) / this.metrics.sessionCount
        );
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('tts-latency').textContent = `${this.metrics.ttsLatency}ms`;
        document.getElementById('llm-latency').textContent = `${this.metrics.llmLatency}ms`;
        document.getElementById('total-latency').textContent = `${this.metrics.totalLatency}ms`;
        document.getElementById('avg-total').textContent = `${this.metrics.avgTotalLatency}ms`;
        
        // Color coding for latency
        this.setLatencyColor('tts-latency', this.metrics.ttsLatency);
        this.setLatencyColor('llm-latency', this.metrics.llmLatency);
        this.setLatencyColor('total-latency', this.metrics.totalLatency);
        this.setLatencyColor('avg-total', this.metrics.avgTotalLatency);
    }
    
    setLatencyColor(elementId, latency) {
        const element = document.getElementById(elementId);
        element.classList.remove('high-latency', 'medium-latency');
        
        if (latency > 3000) {
            element.classList.add('high-latency');
        } else if (latency > 1500) {
            element.classList.add('medium-latency');
        }
    }
}

// Initialize metrics display
window.voiceMetrics = new VoiceMetrics();