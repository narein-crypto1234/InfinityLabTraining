import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score

# Load the data
df = pd.read_csv('dummy_mold_data.csv')

# Features & Target
X = df[['temperature', 'humidity', 'storage_days', 'surface_type']]
y = df['label']

# One-hot encode the 'surface_type' column
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['surface_type'])
    ],
    remainder='passthrough'
)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipeline: OneHotEncoder + Logistic Regression
#//model = make_pipeline(preprocessor, LogisticRegression())
model = make_pipeline(preprocessor, LogisticRegression(max_iter=200))


# Train the model
model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
print(f"✅ Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# === Predict on new input (simulate real-world input) ===
def predict_mold_risk(temp, humidity, storage_days, surface):
    sample = pd.DataFrame([{
        'temperature': temp,
        'humidity': humidity,
        'storage_days': storage_days,
        'surface_type': surface
    }])
    
    prob = model.predict_proba(sample)[0][1]  # Probability of mold (label=1)
    label = model.predict(sample)[0]
    
    print("\n🔍 Prediction for New Sample:")
    print(f"Temperature: {temp}°C, Humidity: {humidity}%, Storage: {storage_days} days, Surface: {surface}")
    print(f"📊 Mold Risk Score: {prob*100:.1f}%")
    print(f"🧠 Final Prediction: {'Mold Detected' if label == 1 else 'Clean'}")

# === Test the function ===
predict_mold_risk(temp=30, humidity=90, storage_days=7, surface='bread')
