import tldextract
import re
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Step 1: Feature extraction function
def extract_features(url):
    ext = tldextract.extract(url)
    return {
        'url_length': len(url),
        'has_ip': bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)),
        'num_dots': url.count('.'),
        'is_https': url.startswith("https"),
        'domain_length': len(ext.domain),
        'suspicious_words': int(any(word in url.lower() for word in ["login", "secure", "update", "verify", "account"]))
    }

# Step 2: Load dataset and preprocess
def load_data(filepath):
    df = pd.read_csv(filepath)
    df['features'] = df['url'].apply(extract_features)
    features_df = pd.DataFrame(df['features'].tolist())
    return features_df, df['label']

# Step 3: Train model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    print("Model Accuracy:", model.score(X_test, y_test))
    return model

# Step 4: Predict function using the trained model
def predict_url(model, url):
    features = pd.DataFrame([extract_features(url)])
    prediction = model.predict(features)[0]
    return "Phishing Link" if prediction == 1 else "Real Link"

# ---- Main Script Execution ----
if __name__ == "__main__":
    # Load and train
    X, y = load_data("C:/Users/sajid/Desktop/CYBER_SECURITY(FINAL PROJ)/SMS/detect_link/phishing_data.csv") # don't use this path because .CSV file is present in my different location and your CSV file will be in different location so you copy user .CSV file path and paste here.
    model = train_model(X, y)

    # Test prediction
    test_url = input("Enter url : ")
    result = predict_url(model, test_url)
    print(f"URL: {test_url} → Prediction: {result}")
