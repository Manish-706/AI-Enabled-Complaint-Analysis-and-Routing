import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load the cleaned complaints CSV
input_file = "data/cleaned_complaints.csv"
df = pd.read_csv(input_file)

# Convert text data into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned_complaint'])

# Train a K-Means Clustering Model
num_clusters = 10  # You can tune this based on your data
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Save the trained model and vectorizer
joblib.dump(kmeans, 'models/kmeans_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

print("Training complete. Model and vectorizer saved.")

# Define cluster-to-category mapping
cluster_mapping = {
    0: "Roads & Infrastructure",
    1: "Electricity Issues",
    2: "Water Supply",
    3: "Garbage Collection",
    4: "Public Transport",
    5: "Traffic Management",
    6: "Healthcare Services",
    7: "Education & Schools",
    8: "Law & Order",
    9: "Municipal Services"
}

# Trial: Predict cluster for a new complaint
new_complaint = "The streetlights are not working, and the road has many potholes."
new_X = vectorizer.transform([new_complaint])
predicted_cluster = kmeans.predict(new_X)[0]
predicted_category = cluster_mapping.get(predicted_cluster, "Unknown Category")

print(f"New complaint: '{new_complaint}' belongs to cluster: {predicted_cluster} ({predicted_category})")
