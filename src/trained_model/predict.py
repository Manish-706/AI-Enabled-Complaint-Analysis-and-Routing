import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and vectorizer
svm_model = joblib.load('../../models/svm_complaint_classifier.pkl')
vectorizer = joblib.load('../../models/tfidf_vectorizer.pkl')

# Define category-to-department mapping
category_department_mapping = {
    "Roads & Infrastructure": "Public Works Department",
    "Electricity Issues": "Electricity Department",
    "Water Supply": "Water Department",
    "Garbage Collection": "Sanitation Department",
    "Public Transport": "Transport Department",
    "Traffic Management": "Traffic Police Department",
    "Healthcare Services": "Health Department",
    "Education & Schools": "Education Department",
    "Law & Order": "Police Department",
    "Municipal Services": "Municipal Corporation"
}

def predict_complaint_category(complaint_text):
    """Predicts the category and department of a new complaint using the trained model."""
    new_X = vectorizer.transform([complaint_text])
    predicted_category = svm_model.predict(new_X)[0]
    department = category_department_mapping.get(predicted_category, "Unknown Department")
    return predicted_category, department

# Example usage
if __name__ == "__main__":
    test_complaint = "I saw potholes on the road"
    category, department = predict_complaint_category(test_complaint)
    print(f"Complaint: '{test_complaint}' belongs to category: {category}, Department: {department}")