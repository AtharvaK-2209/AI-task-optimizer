from src.utils.label_mapping import PRIORITY_ORDER

def fuse_emotions(text_result, face_result):
    text_emotion, text_conf = text_result
    face_emotion, face_conf = face_result

    # If both agree
    if text_emotion == face_emotion:
        return text_emotion, max(text_conf, face_conf)

    # Stress priority
    if "stressed" in [text_emotion, face_emotion]:
        return "stressed", max(text_conf, face_conf)

    # Low confidence fallback
    if text_conf < 0.4 and face_conf < 0.4:
        return "neutral", max(text_conf, face_conf)

    # Apply emotion priority (safety-first)
    if text_emotion in PRIORITY_ORDER and face_emotion in PRIORITY_ORDER:
        text_priority = PRIORITY_ORDER.index(text_emotion)
        face_priority = PRIORITY_ORDER.index(face_emotion)
        if text_priority < face_priority:
            return text_emotion, text_conf
        elif face_priority < text_priority:
            return face_emotion, face_conf
        
    # Fallback: confidence-based decision
    if face_conf > text_conf:
        return face_emotion, face_conf
    else:
        return text_emotion, text_conf
    