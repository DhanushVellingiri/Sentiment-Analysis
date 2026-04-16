from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.stem import PorterStemmer, WordNetLemmatizer
import joblib

app = Flask(__name__)
# Leaving CORS open for development, lock this down to your frontend URL in production
CORS(app) 

# --- 1. LOAD SPECIFIC MODELS AND VECTORIZERS ---
try:
    amazon_model = joblib.load('amazon_model.sav')
    amazon_vectorizer = joblib.load('amazon_vectorizer.sav')

    twitter_model = joblib.load('twitter_acc_model.sav')
    twitter_vectorizer = joblib.load('twitter_acc_vectorizer.sav')

    # Using lr_model2 as the default/YouTube model based on your original code
    yt_model = joblib.load('lr_model2.sav')
    yt_vectorizer = joblib.load('vectorizer2.sav')
except Exception as e:
    print(f"Error loading models. Ensure all .sav files are in the same directory: {e}")

# --- 2. NLP SETUP ---
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """Cleans text using both stemming and lemmatization to match training pipeline."""
    if not text:
        return ""
    words = text.split()
    # Apply stemming then lemmatization sequentially in a single pass
    processed_words = [lemmatizer.lemmatize(stemmer.stem(word)) for word in words]
    return ' '.join(processed_words)

# --- 3. CORE PREDICTION LOGIC (DRY Principle) ---
def get_prediction(text, model, vectorizer):
    """Helper function to handle preprocessing, predicting, and formatting."""
    try:
        clean_text = preprocess_text(text)
        user_input_vector = vectorizer.transform([clean_text])
        
        sentiment_code = model.predict(user_input_vector)[0]
        
        sentiment_mapping = {0: 'Negative', 2: 'Neutral', 4: 'Positive'}
        sentiment_label = sentiment_mapping.get(sentiment_code, "Unknown")
        
        return {'sentiment': sentiment_label}
    except Exception as e:
        return {'error': str(e)}

# --- 4. API ROUTES ---
@app.route('/predictTweet', methods=['POST'])
def predict_tweet():
    data = request.get_json()
    result = get_prediction(data.get('text', ''), twitter_model, twitter_vectorizer)
    return jsonify(result)

@app.route('/predictYT', methods=['POST'])
def predict_youtube():
    data = request.get_json()
    # Note: Your original code looked for 'comment' here instead of 'text'
    result = get_prediction(data.get('comment', ''), yt_model, yt_vectorizer)
    return jsonify(result)

@app.route('/predictAmazon', methods=['POST'])
def predict_amazon():
    data = request.get_json()
    result = get_prediction(data.get('text', ''), amazon_model, amazon_vectorizer)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
