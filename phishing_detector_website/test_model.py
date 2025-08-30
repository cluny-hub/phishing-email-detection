import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

safe_email = "Hello, your account balance is $1000. Have a great day!"
phishing_email = "URGENT: Your account will be suspended! Click http://bad-link.com to verify."

def predict_email(text):
    X = vectorizer.transform([text])
    proba = model.predict_proba(X)[0][1]
    print(f"Phishing probability: {proba}")
    threshold = 0.8
    prediction = 1 if proba >= threshold else 0
    print("Prediction:", "Phishing" if prediction == 1 else "Legit")

print("Testing safe email:")
predict_email(safe_email)

print("\nTesting phishing email:")
predict_email(phishing_email)
