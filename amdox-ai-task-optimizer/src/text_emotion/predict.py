import numpy as np
import joblib

# Paths 
MODEL_PATH =  "models/text_model.pkl"
VECTOR_PATH = "models/vectorizer.pkl"

# Load model and Tf-idf Vectorizer 
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTOR_PATH)

def predict_text_emotion(text):
    # Predicts the confidence and emotion from input text 
    # emotion(str) : predicted emotion label
    # confidence (float): confidence score in range 0–1

    if not text or not isinstance (text, str):
        return "neutral",0.0

    text_vector = vectorizer.transform([text])

    probabilities = model.predict_proba(text_vector)[0]

    best_idx = np.argmax(probabilities)
    emotion = model.classes_[best_idx]

    confidence = float(probabilities[best_idx])

    return emotion, confidence


# Sample testing
# if __name__ == "__main__":
#    test_texts = [
#     'I am so happy and excited today!',
#     'I feel really sad and depressed',
#     'This makes me so angry and frustrated',
#     'I am worried and anxious about tomorrow',
#     'Everything is fine and normal'
# ]

# for text in test_texts:
#     emotion, confidence = predict_text_emotion(text)
#     print(f'Text: \"{text}\"')
#     print(f'Emotion: {emotion} (confidence: {confidence:.1%})')
#     print('-' * 30)
