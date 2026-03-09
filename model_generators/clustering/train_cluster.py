import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

# Configuration
SEGMENT_FEATURES = ["estimated_income", "selling_price"]

# Load data
df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
X = df[SEGMENT_FEATURES]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal number of clusters (2-7)
best_score = -1
best_k = 2
best_kmeans = None

for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    cluster_labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, cluster_labels)
    
    if score > best_score:
        best_score = score
        best_k = k
        best_kmeans = kmeans

# Use the best model
kmeans = best_kmeans
df["cluster_id"] = kmeans.fit_predict(X_scaled)
centers = kmeans.cluster_centers_

# Sort clusters by income (using original scale)
original_centers = scaler.inverse_transform(centers)
sorted_clusters = original_centers[:, 0].argsort()

if best_k == 3:
    cluster_mapping = {
        sorted_clusters[0]: "Economy",
        sorted_clusters[1]: "Standard", 
        sorted_clusters[2]: "Premium",
    }
elif best_k == 4:
    cluster_mapping = {
        sorted_clusters[0]: "Basic",
        sorted_clusters[1]: "Economy",
        sorted_clusters[2]: "Standard",
        sorted_clusters[3]: "Premium",
    }
else:
    # For other k values, use generic names
    cluster_mapping = {}
    for i, cluster_idx in enumerate(sorted_clusters):
        cluster_mapping[cluster_idx] = f"Segment_{i+1}"

df["client_class"] = df["cluster_id"].map(cluster_mapping)

# Save models
joblib.dump(kmeans, "model_generators/clustering/clustering_model.pkl")
joblib.dump(scaler, "model_generators/clustering/scaler.pkl")
joblib.dump(cluster_mapping, "model_generators/clustering/cluster_mapping.pkl")

# Calculate metrics
silhouette_avg = round(silhouette_score(X_scaled, df["cluster_id"]), 2)

# Calculate coefficient of variation for cluster sizes
cluster_sizes = df["cluster_id"].value_counts().values
cv = round(np.std(cluster_sizes) / np.mean(cluster_sizes), 3)

# Create summary tables
cluster_summary = df.groupby("client_class")[SEGMENT_FEATURES].mean()
cluster_counts = df["client_class"].value_counts().reset_index()
cluster_counts.columns = ["client_class", "count"]
cluster_summary = cluster_summary.merge(cluster_counts, on="client_class")

comparison_df = df[["client_name", "estimated_income", "selling_price", "client_class"]]

def evaluate_clustering_model():
    return {
        "silhouette": silhouette_avg,
        "cv": cv,
        "optimal_k": best_k,
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

if __name__ == "__main__":
    result = evaluate_clustering_model()
    print(f"Silhouette Score: {result['silhouette']}")
    print(f"Coefficient of Variation: {result['cv']}")
    print(f"Optimal clusters: {result['optimal_k']}")
    print("\nCluster Summary:")
    print(result['summary'])
