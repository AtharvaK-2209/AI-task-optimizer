# Final unified emotion classes
FINAL_EMOTION_CLASSES = ["happy","sad","angry","stressed","neutral"]

# Text dataset label mapping
TEXT_TO_FINAL = {
    #HAPPY LABELS
    "joy" : "happy",
    # "happiness" : "happy",
    "ammusement" : "happy",
    "love" : "happy",
    "excitement" : "happy",
    "pride" : "happy",
    "gratitude" : "happy",
    "relief" : "happy",

    # NEUTRAL LABELS
    "neutral" : "neutral",
    "realization" : "neutral",
    "confusion" : "neutral",
    "curiosity" : "neutral",
    "surprise" : "neutral",

    # SAD LABELS
    "sadness" : "sad",
    "disappointment" : "sad",
    "grief" : "sad",
    "remorse" : "sad",
    "embarrassment" : "sad",

    # ANGRY LABELS
    "anger" : "angry",
    "annoyance" : "angry",
    "disapproval" : "angry",

    # STRESSED LABELS
    "stress" : "stressed",
    "nervousness" : "stressed",
    "fear" : "stressed",
    "anxiety" : "stressed",
}
PRIORITY_ORDER = ["stressed","angry","sad","neutral", "happy"]

# DeepFace dataset label mapping
DEEPFACE_TO_FINAL = {
    "happy": "happy",
    "neutral": "neutral",
    "sad": "sad",
    "angry": "angry",
    "fear": "stressed",
    "disgust": "stressed",
    "surprise": "neutral"
}
