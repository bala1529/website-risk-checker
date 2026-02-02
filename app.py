from flask import Flask, request, jsonify, render_template
import joblib
import re
import os

app = Flask(__name__)

# Load ML model
model = joblib.load("phishing_model.pkl")

# Feature extraction
def extract_features(url):
    features = []

    features.append(len(url))                 # URL length
    features.append(url.count('.'))           # Dots count
    features.append(len(re.findall(r'[@?&=]', url)))  # Special chars
    features.append(1 if url.startswith('https') else 0)  # HTTPS
    features.append(sum(char.isdigit() for char in url))  # Digits

    suspicious_words = ['login', 'verify', 'free', 'win', 'secure', 'account']
    features.append(sum(word in url.lower() for word in suspicious_words))

    return features

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# API route
@app.route('/check', methods=['POST'])
def check_website():
    data = request.get_json()
    url = data.get('url')

    features = extract_features(url)
    risk_probability = model.predict_proba([features])[0][1]

    if risk_probability < 0.3:
        verdict = "SAFE"
    elif risk_probability < 0.7:
        verdict = "WARNING"
    else:
        verdict = "UNSAFE"

    return jsonify({
        "url": url,
        "risk_probability": round(risk_probability * 100, 2),
        "verdict": verdict
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
