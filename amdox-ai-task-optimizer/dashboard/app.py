"""
AI Task Optimizer
Privacy-first emotion detection and task recommendation system
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules
from src.text_emotion.predict import predict_text_emotion
from src.facial_emotion.face_detect import capture_face_frame
from src.facial_emotion.smile_detector import detect_smile_and_emotion
from src.fusion.emotion_fusion import fuse_emotions
from src.recommendations.task_recommender import recommend_task

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion and return recommendations"""
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        use_face = data.get('use_face', False)
        
        # Text emotion analysis
        text_emotion, text_conf = "neutral", 0.0
        if user_text:
            text_emotion, text_conf = predict_text_emotion(user_text)
            print(f"📝 Text emotion: {text_emotion} (confidence: {text_conf:.2f})")
        
        # Facial emotion analysis (simulated for production stability)
        face_emotion, face_conf = "neutral", 0.0
        face_analysis_note = ""
        
        if use_face:
            try:
                print("🎥 Capturing face for analysis...")
                face_img = capture_face_frame()
                
                if face_img is not None:
                    print(f"✅ Face captured: shape={face_img.shape}")
                    
                    # Use real smile detection (OpenCV-based, no TensorFlow)
                    face_emotion, face_conf = detect_smile_and_emotion(face_img)
                    face_analysis_note = f"Face detected and analyzed: {face_emotion} ({face_conf:.1%} confidence)"
                    
                    print(f"🎭 Face emotion result: {face_emotion} (confidence: {face_conf:.2f})")
                else:
                    face_analysis_note = "No face detected in camera frame"
                    print("❌ No face detected")
                
            except Exception as e:
                face_analysis_note = f"Face analysis failed: {str(e)}"
                print(f"❌ Face detection error: {e}")
        
        # Emotion fusion
        print(f"🔄 Fusion input: text=({text_emotion}, {text_conf:.2f}), face=({face_emotion}, {face_conf:.2f})")
        final_emotion, final_conf = fuse_emotions(
            (text_emotion, text_conf),
            (face_emotion, face_conf)
        )
        print(f"🎯 Fusion output: {final_emotion} (confidence: {final_conf:.2f})")
        
        # Task recommendation
        recommendation = recommend_task(final_emotion, final_conf)
        
        # Prepare response
        response = {
            'success': True,
            'text_emotion': text_emotion,
            'text_confidence': round(text_conf, 3),
            'face_emotion': face_emotion,
            'face_confidence': round(face_conf, 3),
            'final_emotion': recommendation['emotion'],
            'final_confidence': round(recommendation['confidence'], 3),
            'recommendation_level': recommendation['recommendation_level'],
            'tasks': recommendation.get('tasks', []),
            'used_face': use_face,
            'face_analysis_note': face_analysis_note
        }
        
        print(f"📊 Final result: {final_emotion} ({final_conf:.2f})")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/test_camera')
def test_camera():
    """Test camera access endpoint"""
    try:
        face_img = capture_face_frame()
        
        if face_img is not None:
            return jsonify({
                'success': True,
                'message': 'Camera working, face detected',
                'face_shape': face_img.shape,
                'note': 'Production version uses optimized emotion detection'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Camera working but no face detected'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Camera test failed: {str(e)}'
        })

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("🚀 Starting AI Task Optimizer...")
    print("📝 Text emotion analysis: ENABLED (Real ML)")
    print("📷 Face detection: ENABLED (Real OpenCV)")
    print("😊 Smile detection: ENABLED (Real OpenCV - No TensorFlow)")
    print("⚡ Fast and accurate - No mutex issues")
    print("🌐 Access at: http://localhost:8080")
    print("\n✅ Server ready!")
    
    app.run(debug=False, host='127.0.0.1', port=8080)