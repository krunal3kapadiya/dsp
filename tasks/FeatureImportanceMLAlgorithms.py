import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import logging

# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

df = pd.read_csv("../data/Covid_data.csv")
logger.info("Dataset loaded for feature importance.")

# Example of feature importance using Random Forest
features = df[['Age', 'DaysOfStay']]  # Example features
target = df['Covid_Severity']  # Example target

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
logger.info("Dataset split into training and testing sets.")

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)
logger.info("Random Forest model trained.")

# Feature importance
importance = model.feature_importances_
logger.info(f"Feature importances: {importance}")

# Model evaluation
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
logger.info(f"Classification Report:\n{report}")
