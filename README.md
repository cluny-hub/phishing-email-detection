Phishing Email Detection Website

This is a class project web app that detects phishing emails.

Project Files

- **app.py** → Main backend code
- **index.html** → Frontend page
- **train_model.py** → Trains the phishing detection model
- **test_model.py** → Tests the model
- **prepare_dataset.py** → Prepares the CSV dataset
- **dataset.csv** → Dataset of emails

Features
- Enter **email address** and **email content**
- Make a **guess** if the email is phishing or safe
- Scan the email with the system
- Shows **result**, **confidence %**, and highlights suspicious text
- Educational tips included

How to Run (Simple)
1. Download or clone the repo
2. Make sure Python 3 is installed
3. Install dependencies:


pip install flask pandas scikit-learn numpy joblib

4. Run the app:
   python app.py

5. Open your browser at:
   http://127.0.0.1:5000

Author
- GitHub: [cluny-hub](https://github.com/cluny-hub)

