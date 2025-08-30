from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():
    email_address = request.form.get('email_address', '')
    email_content = request.form.get('email_content', '')
    frequency = request.form.get('frequency', '')
    user_guess = request.form.get('user_guess', '')

    # Prepare text for prediction (combine address + content)
    text_for_pred = email_content

    # Transform text using vectorizer
    X = vectorizer.transform([text_for_pred])

    # Get probability of phishing class (1)
    proba = model.predict_proba(X)[0][1]

    # Print phishing probability in terminal for debugging
    print(f"Phishing probability: {proba}")

    threshold = 0.8  # stricter threshold to reduce false positives
    prediction = 1 if proba >= threshold else 0

    # Convert prediction to text
    if prediction == 1:
        prediction_text = "This is a phishing attempt."
    else:
        prediction_text = "This email looks legit—no suspicious information was found."

    # Calculate guess accuracy
    guess_map = {'No': 0, 'Yes': 1, 'Not Sure': -1}
    user_label = guess_map.get(user_guess, -1)

    if user_label == -1:
        accuracy_percent = "N/A (user was not sure)"
    else:
        accuracy_percent = "100%" if user_label == prediction else "0%"

    # Highlight suspicious parts if phishing
    highlight_text = ""
    if prediction == 1:
        highlight_text = highlight_phishing(email_content)
        prediction_text += " Please be careful!"
    elif prediction == 0:
        highlight_text = email_content
    else:
        highlight_text = "This email looks suspicious."

    return render_template('index.html',
                           email_address=email_address,
                           email_content=email_content,
                           frequency=frequency,
                           user_guess=user_guess,
                           prediction_text=prediction_text,
                           accuracy_percent=accuracy_percent,
                           highlight_text=highlight_text)


def highlight_phishing(text):
    suspicious_keywords = [
        "http://", "https://", "www.", "click here", "urgent", "verify", "account",
        "password", "login", "bank", "security", "update", "confirm", "suspend"
    ]

    def escape_html(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    escaped_text = escape_html(text)

    for kw in suspicious_keywords:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        escaped_text = pattern.sub(f'<mark>{kw}</mark>', escaped_text)

    url_pattern = re.compile(r'(http[s]?://\S+)', re.IGNORECASE)
    escaped_text = url_pattern.sub(r'<mark>\1</mark>', escaped_text)

    return escaped_text


if __name__ == "__main__":
    app.run(debug=True)
