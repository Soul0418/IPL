import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# 1. LOAD SNAPSHOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "ipl_auction_master_snapshot.joblib"
)

snapshot = joblib.load(SNAPSHOT_PATH)

model = snapshot["final_auction_model"]
auction_features = snapshot["auction_features"]
feature_columns = snapshot["final_feature_columns"]


# ============================================================
# 2. PREPARE DATA
# ============================================================

df = auction_features.copy()

# Remove rows without an actual auction price
df = df.dropna(
    subset=["final_price_lakh"]
).copy()


# ============================================================
# 3. CREATE MODEL INPUT
# ============================================================

X = df.copy()

# The saved auction_features doesn't contain these three
# features, so use the same temporary values used in predict.py.

X["experience_years"] = 0

X["career_seasons_before"] = (
    X["batting_seasons_before"].fillna(0)
    +
    X["bowling_seasons_before"].fillna(0)
)

X["experience_known"] = 0


# Make sure every model feature exists
for column in feature_columns:

    if column not in X.columns:
        X[column] = 0


# Keep exact feature order
X = X[feature_columns]


# ============================================================
# 4. ACTUAL VALUES
# ============================================================

y = df["final_price_lakh"]


# ============================================================
# 5. PREDICT
# ============================================================

predictions = model.predict(X)


# ============================================================
# 6. METRICS
# ============================================================

mae = mean_absolute_error(
    y,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y,
        predictions
    )
)

r2 = r2_score(
    y,
    predictions
)


# ============================================================
# 7. RESULTS DATAFRAME
# ============================================================

results = df[
    [
        "player_name",
        "year",
        "role",
        "team",
        "final_price_lakh"
    ]
].copy()

results["predicted_price_lakh"] = predictions

results["error_lakh"] = (
    results["predicted_price_lakh"]
    -
    results["final_price_lakh"]
)

results["absolute_error_lakh"] = (
    results["error_lakh"]
    .abs()
)

results["actual_price_crore"] = (
    results["final_price_lakh"] / 100
)

results["predicted_price_crore"] = (
    results["predicted_price_lakh"] / 100
)


# ============================================================
# 8. DISPLAY MODEL PERFORMANCE
# ============================================================

print("\n========================================")
print("IPL AUCTION MODEL EVALUATION")
print("========================================")

print(
    f"\nNumber of auction records: {len(results)}"
)

print(
    f"\nMAE  : ₹{mae:.2f} Lakh"
)

print(
    f"RMSE : ₹{rmse:.2f} Lakh"
)

print(
    f"R²   : {r2:.4f}"
)


# ============================================================
# 9. BEST PREDICTIONS
# ============================================================

print("\n========================================")
print("BEST PREDICTIONS")
print("========================================")

best = results.sort_values(
    "absolute_error_lakh"
).head(10)

print(
    best[
        [
            "player_name",
            "year",
            "actual_price_crore",
            "predicted_price_crore",
            "absolute_error_lakh"
        ]
    ].to_string(index=False)
)


# ============================================================
# 10. LARGEST ERRORS
# ============================================================

print("\n========================================")
print("LARGEST PREDICTION ERRORS")
print("========================================")

worst = results.sort_values(
    "absolute_error_lakh",
    ascending=False
).head(10)

print(
    worst[
        [
            "player_name",
            "year",
            "actual_price_crore",
            "predicted_price_crore",
            "error_lakh"
        ]
    ].to_string(index=False)
)


# ============================================================
# 11. SAVE RESULTS
# ============================================================

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "model_evaluation_results.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nEvaluation results saved to:"
)

print(OUTPUT_PATH)