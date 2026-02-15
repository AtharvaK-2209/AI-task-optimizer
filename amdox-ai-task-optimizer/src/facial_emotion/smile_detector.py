"""
Real-time smile and emotion detection using OpenCV
No TensorFlow, no mutex issues, actual facial feature analysis
"""

import cv2
import numpy as np

def detect_smile_and_emotion(face_img):
    """
    Detect smile and emotion using OpenCV facial features
    Returns: (emotion, confidence)
    
    Uses:
    - Smile detection (Haar Cascade)
    - Eye detection
    - Brightness/contrast analysis
    - Facial geometry
    """
    if face_img is None:
        return "neutral", 0.0
    
    try:
        # Load cascades
        smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )
        eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        # Convert to grayscale
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast for better detection
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # Detect smiles with STRICT parameters to reduce false positives
        smiles = smile_cascade.detectMultiScale(
            gray,
            scaleFactor=1.7,
            minNeighbors=22,  # Higher = fewer false positives
            minSize=(25, 25)
        )
        
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        # Additional validation: Check if detected "smile" is in lower face region
        valid_smiles = []
        for (sx, sy, sw, sh) in smiles:
            # Smile should be in bottom 40% of face
            if sy > height * 0.6:
                valid_smiles.append((sx, sy, sw, sh))
        
        smiles = valid_smiles
        
        # Analyze brightness and contrast
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        # Calculate face metrics
        height, width = gray.shape
        face_area = height * width
        
        # Analyze edge density (angry/stressed faces have more edges/tension)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / face_area
        
        # Analyze vertical gradients (frowns have strong downward patterns)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_intensity = np.mean(np.abs(sobely))
        
        # SMILE DETECTION LOGIC
        smile_detected = len(smiles) > 0
        smile_strength = 0.0
        
        if smile_detected:
            # Calculate smile strength based on size and position
            for (sx, sy, sw, sh) in smiles:
                smile_area = sw * sh
                smile_ratio = smile_area / face_area
                
                # Smiles in lower half of face are more reliable
                if sy > height * 0.5:
                    smile_strength = max(smile_strength, smile_ratio * 100)
        
        # EYE ANALYSIS
        eyes_open = len(eyes) >= 2
        eye_brightness = 0.0
        
        if eyes_open:
            for (ex, ey, ew, eh) in eyes[:2]:
                eye_region = gray[ey:ey+eh, ex:ex+ew]
                eye_brightness += np.mean(eye_region)
            eye_brightness /= min(len(eyes), 2)
        
        # EMOTION CLASSIFICATION
        emotion = "neutral"
        confidence = 0.5
        
        # ANGRY/STRESSED: High edge density + high gradient (tense face)
        if edge_density > 0.15 and gradient_intensity > 15:
            if contrast > 60:
                emotion = "angry"
                confidence = 0.70
            else:
                emotion = "stressed"
                confidence = 0.68
        
        # HAPPY: Strong smile detected AND not high tension
        elif smile_strength > 0.4 and edge_density < 0.15:
            emotion = "happy"
            confidence = min(0.75 + (smile_strength / 8), 0.92)
        
        # HAPPY: Moderate smile with bright eyes AND low tension
        elif smile_strength > 0.15 and eye_brightness > 100 and edge_density < 0.12:
            emotion = "happy"
            confidence = 0.68
        
        # ANGRY: High tension, low brightness, no smile
        elif edge_density > 0.12 and brightness < 100 and not smile_detected:
            emotion = "angry"
            confidence = 0.65
        
        # STRESSED: High tension with moderate brightness
        elif edge_density > 0.13 and brightness > 100:
            emotion = "stressed"
            confidence = 0.62
        
        # SAD: Low brightness, low contrast, low tension (flat/down expression)
        elif brightness < 95 and contrast < 50 and edge_density < 0.10:
            emotion = "sad"
            confidence = 0.60
        
        # HAPPY: Weak smile but very bright face (likely smiling)
        elif smile_strength > 0.05 and brightness > 135 and edge_density < 0.10:
            emotion = "happy"
            confidence = 0.62
        
        # NEUTRAL: Default case
        else:
            emotion = "neutral"
            confidence = 0.55
        
        print(f"🔍 Smile Analysis:")
        print(f"   - Smiles detected: {len(smiles)}")
        print(f"   - Smile strength: {smile_strength:.2f}")
        print(f"   - Eyes detected: {len(eyes)}")
        print(f"   - Brightness: {brightness:.1f}")
        print(f"   - Contrast: {contrast:.1f}")
        print(f"   - Edge density: {edge_density:.3f} (tension)")
        print(f"   - Gradient: {gradient_intensity:.1f}")
        print(f"   - Result: {emotion} ({confidence:.2%})")
        
        return emotion, confidence
        
    except Exception as e:
        print(f"❌ Smile detection error: {e}")
        return "neutral", 0.5
