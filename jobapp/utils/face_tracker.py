import cv2
import numpy as np
from typing import List, Dict
import base64
import logging

logger = logging.getLogger(__name__)

class FaceTracker:
    def __init__(self):
        try:
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
            
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
            
            if self.face_cascade.empty() or self.eye_cascade.empty():
                logger.error("Failed to load cascades")
                raise Exception("Cascades not loaded")
            
            logger.info("Face tracker with eye detection initialized")
            
        except Exception as e:
            logger.error(f"Face tracker initialization failed: {e}")
            self.face_cascade = None
            self.eye_cascade = None
        
    def process_frame(self, frame_data: str) -> Dict:
        """Process base64 frame and return face detection results"""
        try:
            if self.face_cascade is None:
                return {'error': 'Face detector not initialized', 'faces': [], 'count': 0, 'alert': False}
            
            if not frame_data or 'data:image' not in frame_data:
                return {'error': 'Invalid frame format', 'faces': [], 'count': 0, 'alert': False}
            
            try:
                image_data = frame_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as decode_error:
                logger.error(f"Image decode error: {decode_error}")
                return {'error': 'Image decode failed', 'faces': [], 'count': 0, 'alert': False}
            
            if frame is None or frame.size == 0:
                return {'error': 'Invalid image data', 'faces': [], 'count': 0, 'alert': False}
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces with realistic distance constraints
            faces_detected = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=8,
                minSize=(80, 80),   # Minimum realistic face size for laptop
                maxSize=(500, 500), # Maximum realistic face size for laptop
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Validate faces by checking for eyes
            valid_faces = []
            for (x, y, w, h) in faces_detected:
                # Extract face region
                face_roi = gray[y:y+h, x:x+w]
                
                # Detect eyes in face region (more lenient)
                eyes = self.eye_cascade.detectMultiScale(
                    face_roi,
                    scaleFactor=1.05,
                    minNeighbors=3,
                    minSize=(5, 5),
                    maxSize=(60, 60)
                )
                
                # Accept faces with eyes OR reasonable face characteristics
                has_eyes = len(eyes) >= 1
                reasonable_size = 80 <= w <= 500 and 80 <= h <= 500
                good_aspect_ratio = 0.7 <= w/h <= 1.4
                
                if has_eyes or (reasonable_size and good_aspect_ratio):
                    valid_faces.append((x, y, w, h))
            
            # Keep max 2 faces, prefer those with eyes
            if len(valid_faces) > 2:
                # Sort by eye detection first, then by size
                scored_faces = []
                for face in valid_faces:
                    x, y, w, h = face
                    face_roi = gray[y:y+h, x:x+w]
                    eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.05, minNeighbors=3)
                    score = len(eyes) * 1000 + (w * h)  # Prioritize faces with eyes
                    scored_faces.append((score, face))
                
                scored_faces.sort(reverse=True)
                faces_detected = [face for score, face in scored_faces[:2]]
            else:
                faces_detected = valid_faces
            
            faces = []
            for i, (x, y, w, h) in enumerate(faces_detected):
                faces.append({
                    'id': i,
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'confidence': 0.85
                })
            
            logger.info(f"Detected {len(faces)} faces")
            
            return {
                'faces': faces,
                'count': len(faces),
                'alert': len(faces) > 1,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Face detection error: {e}")
            return {'error': str(e), 'faces': [], 'count': 0, 'alert': False}