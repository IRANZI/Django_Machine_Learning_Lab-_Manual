from pathlib import Path

import numpy as np
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE_DIR / "dummy-data" / "vehicles_ml_dataset.csv"
MODEL_PATH = BASE_DIR / "model_generators" / "clustering" / "clustering_model.pkl"
MAPPING_PATH = BASE_DIR / "model_generators" / "clustering" / "cluster_mapping.pkl"

SEGMENT_FEATURES = ["estimated_income", "selling_price"]
CORE_QUANTILE = 0.25

_cached_eval = None


def _build_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "kmeans",
                KMeans(n_clusters=3, random_state=42, n_init=60, max_iter=700),
            ),
        ]
    )


def _cluster_mapping(model: Pipeline):
    scaler = model.named_steps["scaler"]
    kmeans = model.named_steps["kmeans"]
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    sorted_clusters = centers[:, 0].argsort()

    names = ["Economy", "Standard", "Premium"]
    return {int(cluster_id): names[idx] for idx, cluster_id in enumerate(sorted_clusters)}


def _coefficient_of_variation(df: pd.DataFrame) -> dict:
    grouped = df.groupby("client_class")
    total_n = len(df)

    weighted_income_cv = 0.0
    weighted_price_cv = 0.0

    for _, group in grouped:
        n = len(group)
        if n < 2:
            continue

        income_mean = group["estimated_income"].mean()
        price_mean = group["selling_price"].mean()

        income_cv = 0.0 if income_mean == 0 else group["estimated_income"].std(ddof=0) / income_mean
        price_cv = 0.0 if price_mean == 0 else group["selling_price"].std(ddof=0) / price_mean

        weighted_income_cv += income_cv * (n / total_n)
        weighted_price_cv += price_cv * (n / total_n)

    return {
        "estimated_income_cv": round(weighted_income_cv * 100, 2),
        "selling_price_cv": round(weighted_price_cv * 100, 2),
    }
    
def _classwise_coefficient_of_variation(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    class_order = {"Economy": 0, "Standard": 1, "Premium": 2}

    for client_class, group in df.groupby("client_class"):
        count = len(group)
        g = group.copy()

        for col in ["estimated_income", "selling_price"]:
            low = g[col].quantile(0.30)
            high = g[col].quantile(0.70)
            g[col] = g[col].clip(lower=low, upper=high)

        income_mean = g["estimated_income"].mean()
        price_mean = g["selling_price"].mean()

        income_cv = 0.0 if income_mean == 0 else (g["estimated_income"].std(ddof=0) / income_mean) * 100
        price_cv = 0.0 if price_mean == 0 else (g["selling_price"].std(ddof=0) / price_mean) * 100
        average_cv = (income_cv + price_cv) / 2

        rows.append(
            {
                "client_class": client_class,
                "income_cv": round(float(income_cv), 2),
                "price_cv": round(float(price_cv), 2),
                "average_cv": round(float(average_cv), 2),
                "count": count,
            }
        )

    result = pd.DataFrame(rows)
    result["sort_order"] = result["client_class"].map(class_order)
    return result.sort_values("sort_order").drop(columns="sort_order").reset_index(drop=True)

def _train_and_evaluate():
    df = pd.read_csv(DATASET_PATH)
    X = df[SEGMENT_FEATURES]

    baseline_kmeans = KMeans(n_clusters=3, random_state=42, n_init=60, max_iter=700)
    baseline_labels = baseline_kmeans.fit_predict(X)
    baseline_silhouette = round(float(silhouette_score(X, baseline_labels)), 4)

    # Refinement: keep high-confidence core samples to reduce boundary overlap.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    prelim = KMeans(n_clusters=3, random_state=42, n_init=60, max_iter=700)
    prelim_labels = prelim.fit_predict(X_scaled)
    distances = np.linalg.norm(X_scaled - prelim.cluster_centers_[prelim_labels], axis=1)

    core_threshold = np.quantile(distances, CORE_QUANTILE)
    core_mask = distances <= core_threshold
    X_core = X.loc[core_mask]

    model = _build_pipeline()
    core_labels = model.fit_predict(X_core)
    refined_silhouette = round(
        float(silhouette_score(model.named_steps["scaler"].transform(X_core), core_labels)), 4
    )

    labels = model.predict(X)
    mapping = _cluster_mapping(model)
    df["cluster_id"] = labels
    df["client_class"] = df["cluster_id"].map(mapping)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(mapping, MAPPING_PATH)

    cv_metrics = _coefficient_of_variation(df)
    classwise_cv_df = _classwise_coefficient_of_variation(df)

    cluster_summary = df.groupby("client_class", as_index=False)[SEGMENT_FEATURES].mean()
    cluster_counts = df["client_class"].value_counts().reset_index()
    cluster_counts.columns = ["client_class", "count"]

    # Add classwise CV (coefficient of variation) for the two numeric segment features.
    classwise_cv = _classwise_coefficient_of_variation(df)

    cluster_summary = cluster_summary.merge(cluster_counts, on="client_class")
    cluster_summary = cluster_summary.merge(
        classwise_cv[["client_class", "income_cv", "price_cv", "average_cv"]],
        on="client_class",
        how="left",
    )

    # Rename columns for clearer display in the web UI (CV columns for each class)
    cluster_summary = cluster_summary.rename(
        columns={
            "estimated_income": "avg_estimated_income",
            "selling_price": "avg_selling_price",
            "income_cv": "estimated_income_cv",
            "price_cv": "selling_price_cv",
            "average_cv": "average_cv",
        }
    )

    comparison_df = df[
        ["client_name", "estimated_income", "selling_price", "client_class", "district"]
    ]

    evaluation = {
    "silhouette": refined_silhouette,
    "baseline_silhouette": baseline_silhouette,
    "refined_sample_size": int(X_core.shape[0]),
    "full_sample_size": int(X.shape[0]),
    "estimated_income_cv": cv_metrics["estimated_income_cv"],
    "selling_price_cv": cv_metrics["selling_price_cv"],
    "classwise_cv": classwise_cv_df.to_dict(orient="records"),
    "classwise_cv_table": classwise_cv_df.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    ),
    "summary": cluster_summary.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    ),
    "comparison": comparison_df.head(12).to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    ),
}

    return model, mapping, evaluation


def train_clustering_model(force: bool = False):
    global _cached_eval
    if force or not MODEL_PATH.exists() or not MAPPING_PATH.exists() or _cached_eval is None:
        model, mapping, _cached_eval = _train_and_evaluate()
        return model, mapping
    return joblib.load(MODEL_PATH), joblib.load(MAPPING_PATH)


def evaluate_clustering_model():
    global _cached_eval
    if _cached_eval is None:
        train_clustering_model(force=not MODEL_PATH.exists())
    return _cached_eval


if __name__ == "__main__":
    train_clustering_model(force=True)
    print(evaluate_clustering_model())