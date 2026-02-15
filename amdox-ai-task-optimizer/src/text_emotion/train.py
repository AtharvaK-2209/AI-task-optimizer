import pandas as pd 
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


''' ----------------- PATH ------------------'''
DATA_PATH = "data/processed/text_emotion_processed.csv"
MODEL_PATH = "models/text_model.pkl"
VECTOR_PATH = "models/vectorizer.pkl"


def train_test_emotion_model():
    df = pd.read_csv(DATA_PATH)

    df.dropna(subset = ['clean_text', 'label'], inplace = True)
    X = df['clean_text'].astype(str)
    y = df['label']
    print("Training Samples: ", len(df))

    # Train-test Split 
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # TF-IDF Vectorizer 
    vectorizer = TfidfVectorizer(
        ngram_range = (1,2),
        max_features = 5000,
        min_df = 2,
        max_df = 0.9
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Logistic Regression Model
    model = LogisticRegression(
        max_iter = 1000,
        solver = "lbfgs",
    )

    model.fit(X_train_vec, y_train)

    # Evaluation (Sanity Check)
    y_pred = model.predict(X_test_vec)
    
    print("Classification Report : \n")
    print(classification_report(y_test, y_pred))

    # Save model & vectorizer
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTOR_PATH)

    print("\n Text emotion model trained and saved successfully!")

if __name__ == "__main__": 
    train_test_emotion_model()