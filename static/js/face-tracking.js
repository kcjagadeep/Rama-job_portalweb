class FaceTracker {
    constructor(videoElement) {
        this.video = videoElement;
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.isTracking = false;
        this.alertShown = false;
        this.lastDetectionTime = 0;
        this.detectionInterval = 2000; // Check every 2 seconds
        this.statusIndicator = document.getElementById('faceStatus');
        
        // Create overlay canvas
        this.overlay = document.createElement('canvas');
        this.overlay.style.position = 'absolute';
        this.overlay.style.top = '0';
        this.overlay.style.left = '0';
        this.overlay.style.pointerEvents = 'none';
        this.overlay.style.zIndex = '10';
        this.overlay.style.borderRadius = '12px';
        
        // Add overlay to video container
        const container = this.video.parentElement;
        if (container) {
            container.style.position = 'relative';
            this.overlay.style.width = '100%';
            this.overlay.style.height = '100%';
            container.appendChild(this.overlay);
            console.log('✅ Face tracking overlay added to video container');
        }
        
        // Wait for video to be ready
        this.waitForVideo();
    }
    
    waitForVideo() {
        if (this.video.videoWidth > 0 && this.video.videoHeight > 0) {
            console.log(`📹 Video ready: ${this.video.videoWidth}x${this.video.videoHeight}`);
            this.setupCanvas();
            if (this.isTracking) {
                this.updateStatus('ACTIVE', true);
                setTimeout(() => this.detectFaces(), 500);
            }
        } else {
            console.log('⏳ Waiting for video to load...');
            this.updateStatus('Waiting for camera...', false);
            setTimeout(() => this.waitForVideo(), 100);
        }
    }
    
    setupCanvas() {
        const rect = this.video.getBoundingClientRect();
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        this.overlay.width = rect.width;
        this.overlay.height = rect.height;
        console.log(`🎯 Canvas setup: ${this.canvas.width}x${this.canvas.height}`);
    }
    
    start() {
        this.isTracking = true;
        console.log('🎯 Face tracking started');
        this.updateStatus('STARTING...', false);
        this.detectFaces();
    }
    
    updateStatus(message, isActive) {
        if (this.statusIndicator) {
            this.statusIndicator.querySelector('span').textContent = `Face Detection: ${message}`;
            if (isActive) {
                this.statusIndicator.classList.add('active');
            } else {
                this.statusIndicator.classList.remove('active');
            }
        }
    }
    
    stop() {
        // Never actually stop - always keep tracking
        console.log('⚠️ Face tracking stop requested but keeping active');
    }
    
    async detectFaces() {
        if (!this.video || !this.video.videoWidth || !this.isTracking) {
            setTimeout(() => this.detectFaces(), 100);
            return;
        }
        
        const now = Date.now();
        if (now - this.lastDetectionTime < this.detectionInterval) {
            setTimeout(() => this.detectFaces(), 50);
            return;
        }
        
        this.lastDetectionTime = now;
        
        try {
            // Update canvas size if needed
            const rect = this.video.getBoundingClientRect();
            if (this.canvas.width !== this.video.videoWidth) {
                this.setupCanvas();
            }
            
            // Capture frame
            this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            const frameData = this.canvas.toDataURL('image/jpeg', 0.7);
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                             document.querySelector('input[name=csrfmiddlewaretoken]')?.value || 
                             (typeof TEMPLATE_DATA !== 'undefined' ? TEMPLATE_DATA.csrfToken : '') ||
                             document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
            
            if (!csrfToken) {
                console.warn('⚠️ No CSRF token found');
            }
            
            const response = await fetch('/api/face-detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ frame: frameData })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            if (result.error) {
                console.error('🚨 Face detection error:', result.error);
                this.updateStatus('ERROR', false);
            } else {
                console.log(`👤 Detected ${result.count} faces`);
                this.updateStatus(`${result.count} faces`, true);
                this.drawFaces(result.faces || []);
                
                if (result.alert && !this.alertShown) {
                    console.log('🚨 Multiple people detected!');
                    this.showAlert(`Alert: ${result.count} people detected!`);
                    this.alertShown = true;
                    setTimeout(() => { this.alertShown = false; }, 5000);
                }
            }
            
        } catch (error) {
            console.error('❌ Face detection request failed:', error);
            this.updateStatus('OFFLINE', false);
        }
        
        // Continue detection with longer delay
        setTimeout(() => this.detectFaces(), this.detectionInterval);
    }
    
    drawFaces(faces) {
        if (!faces || !Array.isArray(faces)) {
            console.warn('⚠️ Invalid faces data:', faces);
            return;
        }
        
        const overlayCtx = this.overlay.getContext('2d');
        overlayCtx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        
        if (faces.length === 0) {
            return;
        }
        
        // Scale factors to match overlay size to video display size
        const scaleX = this.overlay.width / this.video.videoWidth;
        const scaleY = this.overlay.height / this.video.videoHeight;
        
        faces.forEach((face, index) => {
            const color = index === 0 ? '#00ff00' : '#ff0000';
            const label = index === 0 ? 'Candidate' : `Person ${index + 1}`;
            
            // Scale coordinates
            const x = face.x * scaleX;
            const y = face.y * scaleY;
            const width = face.width * scaleX;
            const height = face.height * scaleY;
            
            // Draw rectangle with rounded corners
            overlayCtx.strokeStyle = color;
            overlayCtx.lineWidth = 2;
            overlayCtx.setLineDash([]);
            overlayCtx.strokeRect(x, y, width, height);
            
            // Draw label background
            overlayCtx.fillStyle = color;
            overlayCtx.fillRect(x, y - 25, 80, 20);
            
            // Draw label text
            overlayCtx.fillStyle = 'white';
            overlayCtx.font = 'bold 12px Arial';
            overlayCtx.fillText(label, x + 5, y - 10);
        });
        
        if (faces.length > 0) {
            console.log(`✅ Drew ${faces.length} face detection boxes`);
        }
    }
    
    showAlert(message) {
        // Remove existing alert
        const existing = document.querySelector('.face-alert');
        if (existing) existing.remove();
        
        // Create alert
        const alert = document.createElement('div');
        alert.className = 'face-alert';
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 9999;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        alert.textContent = message;
        
        document.body.appendChild(alert);
        
        // Auto remove
        setTimeout(() => {
            if (alert.parentNode) alert.remove();
        }, 5000);
    }
}

// Auto-initialize when video is ready
function initFaceTrackingOnVideo() {
    const video = document.getElementById('userVideo');
    
    if (video && video.videoWidth > 0 && !window.globalFaceTracker) {
        console.log('📹 userVideo found, starting ALWAYS-ON face tracking');
        window.globalFaceTracker = new FaceTracker(video);
        window.globalFaceTracker.start();
        return true;
    }
    return !!window.globalFaceTracker;
}

// Force start face tracking when video loads
function forceStartFaceTracking() {
    const video = document.getElementById('userVideo');
    if (video && !window.globalFaceTracker) {
        console.log('🔄 Force starting face tracking');
        window.globalFaceTracker = new FaceTracker(video);
        window.globalFaceTracker.start();
        return true;
    }
    return false;
}

// Keep trying every second
setInterval(() => {
    if (!window.globalFaceTracker) {
        forceStartFaceTracking();
    }
}, 1000);

// Global variable to ensure only one tracker runs
window.globalFaceTracker = null;