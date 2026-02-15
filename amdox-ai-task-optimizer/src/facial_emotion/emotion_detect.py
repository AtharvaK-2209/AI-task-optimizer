import cv2
from deepface import DeepFace
from src.utils.label_mapping import DEEPFACE_TO_FINAL


def detect_face_emotion(face_img):
    if face_img is None:
        return "neutral", 0.0
    try:
        result = DeepFace.analyze(
            face_img,
            actions=['emotion'],
            enforce_detection=False
        )

        raw_emotion = result[0]["dominant_emotion"]
        raw_confidence = result[0][raw_emotion]  # outputs between 0-100

        final_emotion = DEEPFACE_TO_FINAL.get(raw_emotion, "neutral")
        confidence  = float(raw_confidence)/100.0

        return final_emotion, confidence

    except Exception:
        return "neutral", 0.0
