from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from googletrans import Translator
import joblib
import nltk

# Force Render to download the required NLTK dictionaries on startup
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)

app = Flask(__name__)
# Allow your React frontend to connect
CORS(app)

# --- 1. LOAD MODELS & VECTORIZERS ---
twitter_model = joblib.load('twitter_acc_model.sav')
twitter_vectorizer = joblib.load('twitter_acc_vectorizer.sav')

yt_model = joblib.load('lr_model.sav')
yt_vectorizer = joblib.load('vectorizer.sav')

amazon_model = joblib.load('amazon_acc_model.sav')
amazon_vectorizer = joblib.load('amazon_acc_vectorizer.sav')

# --- 2. NLP SETUP ---
sentiments = SentimentIntensityAnalyzer()
translator = Translator()
stop_words = set(stopwords.words('english'))

# --- 3. CORE LOGIC (DRY Principle) ---
def process_and_predict(text, model, vectorizer):
    """Handles translation, cleaning, and dual-sentiment prediction."""
    try:
        # 1. Attempt Translation (Fails gracefully if Google blocks the IP)
        try:
            text = translator.translate(text, src='auto', dest='en').text
        except Exception as e:
            print(f"Translation failed/skipped: {e}")
        
        # 2. Clean Text (Lowercase, remove short words, remove stopwords)
        cleaned_text = ' '.join(
            [w.lower() for w in text.split() if len(w) > 3 and w.lower() not in stop_words]
        )
        
        # 3. Vectorize & Predict (ML Model)
        # Note: .toarray() is used because these models were trained on dense matrices
        text_vector = vectorizer.transform([cleaned_text]).toarray()
        sentiment_code = model.predict(text_vector)[0]
        
        sentiment_maps = {-1: "Negative", 0: "Neutral", 1: "Positive"}
        ml_label = sentiment_maps.get(sentiment_code, "Unknown")
        
        # 4. VADER Score (Rule-based)
        vader_scores = sentiments.polarity_scores(cleaned_text)
        
        return {'sentiment': ml_label, 'vader_score': vader_scores}
    
    except Exception as e:
        return {'error': str(e)}

# --- 4. API ROUTES ---
@app.route('/predictTweet', methods=['POST'])
def predict_tweet():
    data = request.get_json()
    result = process_and_predict(data.get('text', ''), twitter_model, twitter_vectorizer)
    return jsonify(result)

@app.route('/predictYT', methods=["POST"])
def predict_youtube():
    data = request.get_json()
    result = process_and_predict(data.get('comment', ''), yt_model, yt_vectorizer)
    return jsonify(result)

@app.route('/predictAmazon', methods=["POST"])
def predict_amazon():
    data = request.get_json()
    result = process_and_predict(data.get('review', ''), amazon_model, amazon_vectorizer)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
