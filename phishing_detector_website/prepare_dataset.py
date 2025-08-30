import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Drop rows with missing values
df.dropna(inplace=True)

# Convert labels to binary (phishing = 1, legit = 0)
df['label'] = df['label'].map({'phishing': 1, 'legit': 0})

# Prepare features and labels
X = df['email']
y = df['label']

# Vectorize the email text
vectorizer = TfidfVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

# Save the vectorizer
joblib.dump(vectorizer, 'vectorizer.pkl')

# Split dataset (not required now but still good to have)
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Save the processed data
joblib.dump((X_train, y_train), 'train_data.pkl')
joblib.dump((X_test, y_test), 'test_data.pkl')

print("✅ Dataset prepared and saved.")
