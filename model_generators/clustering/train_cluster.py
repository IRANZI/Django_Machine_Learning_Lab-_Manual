import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

SEGMENT_FEATURES = ["estimated_income", "selling_price"]

df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
X = df[SEGMENT_FEATURES]

# Standardize features for better clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal number of clusters using elbow method and silhouette analysis
silhouette_scores = []
cv_scores = []
k_range = range(2, 8)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    cluster_labels = kmeans.fit_predict(X_scaled)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    
    # Calculate coefficient of variation
    cluster_centers = kmeans.cluster_centers_
    overall_center = np.mean(cluster_centers, axis=0)
    distances = [np.linalg.norm(center - overall_center) for center in cluster_centers]
    cv = np.std(distances) / np.mean(distances) if np.mean(distances) != 0 else 0
    cv_scores.append(cv)

# Select best k based on silhouette score
best_k = np.argmax(silhouette_scores) + 2  
best_silhouette = max(silhouette_scores)
best_cv = cv_scores[best_k - 2]

# Use the best k for final model
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
df["cluster_id"] = kmeans.fit_predict(X_scaled)

centers = scaler.inverse_transform(kmeans.cluster_centers_)  

# Sort clusters by income
sorted_clusters = centers[:, 0].argsort()
cluster_mapping = {}
for i, cluster_idx in enumerate(sorted_clusters):
    cluster_mapping[cluster_idx] = f"Segment {i+1}"

df["client_class"] = df["cluster_id"].map(cluster_mapping)

joblib.dump(kmeans, "model_generators/clustering/clustering_model.pkl")
joblib.dump(scaler, "model_generators/clustering/scaler.pkl")
joblib.dump(cluster_mapping, "model_generators/clustering/cluster_mapping.pkl")

# Calculate final metrics
silhouette_avg = round(best_silhouette, 2)
coefficient_variation = round(best_cv, 2)

cluster_summary = df.groupby("client_class")[SEGMENT_FEATURES].mean()
cluster_counts = df["client_class"].value_counts().reset_index()
cluster_counts.columns = ["client_class", "count"]
cluster_summary = cluster_summary.merge(cluster_counts, on="client_class")

comparison_df = df[["client_name", "estimated_income", "selling_price", "client_class"]]

def evaluate_clustering_model():
    return {
        "silhouette": silhouette_avg,
        "coefficient_variation": coefficient_variation,
        "optimal_clusters": best_k,
        "summary": cluster_summary.to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
        "comparison": comparison_df.head(10).to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
    }
