import cv2
import time

# Load Haar Cascade once
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def capture_face_frame():
    """
    Capture face from camera with improved detection parameters
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return None
    
    # Set camera properties for better quality
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Try multiple frames to increase detection chance
    max_attempts = 5
    
    for attempt in range(max_attempts):
        ret, frame = cap.read()
        
        if not ret:
            continue
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Try multiple detection parameters for better results
        detection_params = [
            {'scaleFactor': 1.1, 'minNeighbors': 3, 'minSize': (30, 30)},
            {'scaleFactor': 1.2, 'minNeighbors': 4, 'minSize': (50, 50)},
            {'scaleFactor': 1.3, 'minNeighbors': 5, 'minSize': (30, 30)},
        ]
        
        for params in detection_params:
            faces = FACE_CASCADE.detectMultiScale(
                gray,
                scaleFactor=params['scaleFactor'],
                minNeighbors=params['minNeighbors'],
                minSize=params['minSize']
            )
            
            if len(faces) > 0:
                # Found face! Get the largest one
                largest_face = max(faces, key=lambda face: face[2] * face[3])
                x, y, w, h = largest_face
                
                # Add some padding around the face
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(frame.shape[1] - x, w + 2 * padding)
                h = min(frame.shape[0] - y, h + 2 * padding)
                
                face_img = frame[y:y+h, x:x+w]
                cap.release()
                return face_img
        
        # Small delay between attempts
        time.sleep(0.1)
    
    cap.release()
    return None
