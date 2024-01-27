import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import joblib

start_time = time.time()

# Read the dataset
data = pd.read_csv('data.csv')

# Drop rows with missing values
data.dropna(subset=['password', 'strength'], inplace=True)

# Features (passwords) and labels (strength)
features = data['password']
labels = data['strength']

# Map integer labels to descriptive string labels
label_mapping = {0: 'weak', 1: 'medium', 2: 'strong'}
labels = labels.map(label_mapping)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25, random_state=0)

# Create a pipeline for text feature extraction and Logistic Regression
classifier_model = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char')),
    ('logisticRegression', LogisticRegression(multi_class='multinomial', solver='sag')),
])

# Fit the model
classifier_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = classifier_model.predict(X_test)

# Calculate and print metrics
cm = confusion_matrix(y_test, y_pred)
print(classification_report(y_test, y_pred, digits=4))
print("Confusion Matrix: \n", cm)

# Calculate and print accuracy
accuracy = (cm[0][0] + cm[1][1] + cm[2][2]) / y_test.shape[0]
print("Testing Accuracy = ", accuracy)
print("Time Taken to train the model = %s seconds" % round(time.time() - start_time, 2))

# Save the trained model
joblib.dump(classifier_model, 'LogisticRegression_Model.joblib')
