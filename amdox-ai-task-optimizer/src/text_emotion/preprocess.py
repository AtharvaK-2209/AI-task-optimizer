import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from src.utils.label_mapping import TEXT_TO_FINAL, PRIORITY_ORDER

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text  =re.sub(r"[^a-z\s]", "" , text)
    tokens = text.split()                 # Tokenization
    tokens = [                            # Lemmatization and Stopword Removal(Remove high freq meaningless words)
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words
    ]
    return " ".join(tokens)

def get_dominant_emotion(row, emotion_columns):
    active_emotions = [ e for e in emotion_columns if row[e] == 1]
    mapped = [
        TEXT_TO_FINAL[e]
        for e in active_emotions
        if e in TEXT_TO_FINAL
    ]
    for emotion in PRIORITY_ORDER:
        if emotion in mapped:
            return emotion
    return None

def preprocess_dataset(input_path, output_path):
    df = pd.read_csv(input_path)
    #rename columns to standard names if needed
    emotion_columns = [
        col for col in df.columns
        if col in TEXT_TO_FINAL
    ]
    # map labels to final emotion classes
    df["label"] = df.apply(lambda row: get_dominant_emotion(row, emotion_columns), axis = 1)
    # drop unmapped labels
    df = df.dropna(subset = ["label"])
    # clean text data
    df["clean_text"] = df["text"].apply(clean_text)
    df[["clean_text", "label"]].to_csv(output_path, index = False)
    print("Text Emotion dataset preprocessed and saved to", output_path)

if __name__ == "__main__":
    preprocess_dataset( "data/raw/text_emotion.csv", "data/processed/text_emotion_processed.csv" )