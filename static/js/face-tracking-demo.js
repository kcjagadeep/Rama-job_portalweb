// Simple demo page to test face tracking
class FaceTrackingDemo {
    constructor() {
        this.video = null;
        this.canvas = null;
        this.ctx = null;
        this.isTracking = false;
        this.faceCount = 0;
        
        this.init();
    }
    
    async init() {
        // Create demo interface
        document.body.innerHTML = `
            <div style="font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0;">
                <h1>🎯 Face Tracking Demo</h1>
                <div style="display: flex; gap: 20px; margin: 20px 0;">
                    <button id="startBtn" onclick="demo.start()">Start Camera</button>
                    <button id="stopBtn" onclick="demo.stop()" disabled>Stop</button>
                    <div id="status" style="padding: 10px; background: #fff; border-radius: 5px;">
                        Status: Ready
                    </div>
                </div>
                
                <div style="position: relative; display: inline-block;">
                    <video id="demoVideo" width="640" height="480" style="border: 2px solid #333;"></video>
                    <canvas id="overlay" width="640" height="480" 
                            style="position: absolute; top: 0; left: 0; pointer-events: none;"></canvas>
                </div>
                
                <div id="results" style="margin-top: 20px; padding: 15px; background: #fff; border-radius: 5px;">
                    <h3>Detection Results:</h3>
                    <div id="faceInfo">No faces detected</div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: #e8f5e8; border-radius: 5px;">
                    <h3>How it works:</h3>
                    <ul>
                        <li>🟢 <strong>Green box</strong> = Person 1 (primary person)</li>
                        <li>🔴 <strong>Red box</strong> = Additional people detected</li>
                        <li>🚨 <strong>Alert</strong> appears when multiple people are detected</li>
                        <li>Detection runs every 500ms for performance</li>
                    </ul>
                </div>
            </div>
        `;
        
        this.video = document.getElementById('demoVideo');
        this.canvas = document.getElementById('overlay');
        this.ctx = this.canvas.getContext('2d');
    }
    
    async start() {
        try {
            this.updateStatus('Requesting camera access...');
            
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 }
            });
            
            this.video.srcObject = stream;
            this.video.play();
            
            this.updateStatus('Camera active - Starting face detection...');
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            
            this.isTracking = true;
            this.detectFaces();
            
        } catch (error) {
            this.updateStatus(`Error: ${error.message}`);
            console.error('Camera error:', error);
        }
    }
    
    stop() {
        this.isTracking = false;
        
        if (this.video.srcObject) {
            this.video.srcObject.getTracks().forEach(track => track.stop());
            this.video.srcObject = null;
        }
        
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.updateStatus('Stopped');
        
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('faceInfo').textContent = 'No faces detected';
    }
    
    async detectFaces() {
        if (!this.isTracking) return;
        
        try {
            // Capture frame from video
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = this.video.videoWidth;
            tempCanvas.height = this.video.videoHeight;
            const tempCtx = tempCanvas.getContext('2d');
            tempCtx.drawImage(this.video, 0, 0);
            
            // Convert to base64
            const frameData = tempCanvas.toDataURL('image/jpeg', 0.8);
            
            // Send to backend for face detection
            const response = await fetch('/api/face-detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ frame: frameData })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.updateStatus(`Detection error: ${result.error}`);
            } else {
                this.drawFaces(result.faces);
                this.updateResults(result);
                
                if (result.alert) {
                    this.showAlert(`🚨 ALERT: ${result.count} people detected!`);
                }
            }
            
        } catch (error) {
            console.error('Detection error:', error);
            this.updateStatus(`Network error: ${error.message}`);
        }
        
        // Continue detection
        setTimeout(() => this.detectFaces(), 500);
    }
    
    drawFaces(faces) {
        // Clear previous drawings
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        faces.forEach((face, index) => {
            const color = index === 0 ? '#00ff00' : '#ff0000'; // Green for Person 1, Red for others
            const label = index === 0 ? 'Person 1' : `Person ${index + 1}`;
            
            // Draw rectangle
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 3;
            this.ctx.strokeRect(face.x, face.y, face.width, face.height);
            
            // Draw label background
            this.ctx.fillStyle = color;
            this.ctx.fillRect(face.x, face.y - 25, 100, 20);
            
            // Draw label text
            this.ctx.fillStyle = 'white';
            this.ctx.font = '14px Arial';
            this.ctx.fillText(label, face.x + 5, face.y - 10);
            
            // Draw confidence
            this.ctx.fillStyle = color;
            this.ctx.font = '12px Arial';
            this.ctx.fillText(`${(face.confidence * 100).toFixed(0)}%`, 
                            face.x, face.y + face.height + 15);
        });
    }
    
    updateResults(result) {
        const faceInfo = document.getElementById('faceInfo');
        
        if (result.count === 0) {
            faceInfo.innerHTML = '❌ No faces detected';
        } else if (result.count === 1) {
            faceInfo.innerHTML = '✅ 1 person detected (Person 1)';
        } else {
            faceInfo.innerHTML = `🚨 ${result.count} people detected! Alert triggered.`;
        }
        
        this.faceCount = result.count;
    }
    
    showAlert(message) {
        // Create temporary alert
        const alert = document.createElement('div');
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff4444;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-weight: bold;
            z-index: 9999;
            animation: fadeIn 0.3s ease;
        `;
        alert.textContent = message;
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            if (alert.parentNode) alert.remove();
        }, 3000);
    }
    
    updateStatus(message) {
        document.getElementById('status').textContent = `Status: ${message}`;
    }
    
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Initialize demo when page loads
let demo;
document.addEventListener('DOMContentLoaded', () => {
    demo = new FaceTrackingDemo();
});