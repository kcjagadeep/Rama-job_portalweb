// Test script to verify face tracking is working
// Paste this in browser console on the interview page

console.log('🎯 Testing Face Tracking...');

// Check if video exists
const video = document.getElementById('userVideo');
console.log('Video element:', video);
console.log('Video dimensions:', video?.videoWidth, 'x', video?.videoHeight);

// Check if face tracker is initialized
console.log('Global face tracker:', window.globalFaceTracker);

// Force initialize if not running
if (!window.globalFaceTracker && video) {
    console.log('🚀 Force starting face tracking...');
    window.globalFaceTracker = new FaceTracker(video);
    window.globalFaceTracker.start();
}

// Test API directly
async function testFaceAPI() {
    if (!video || !video.videoWidth) {
        console.log('❌ Video not ready');
        return;
    }
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    const frameData = canvas.toDataURL('image/jpeg', 0.8);
    
    try {
        const response = await fetch('/api/face-detect/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': TEMPLATE_DATA?.csrfToken || ''
            },
            body: JSON.stringify({ frame: frameData })
        });
        
        const result = await response.json();
        console.log('🎯 Face API Result:', result);
        
        if (result.faces && result.faces.length > 0) {
            console.log('✅ FACES DETECTED!', result.faces.length);
        } else {
            console.log('ℹ️ No faces detected');
        }
        
    } catch (error) {
        console.error('❌ API Error:', error);
    }
}

// Test immediately and every 2 seconds
testFaceAPI();
setInterval(testFaceAPI, 2000);