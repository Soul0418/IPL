import pandas as pd
import numpy as np
from pathlib import Path
import joblib


# ============================================================
# 1. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "ipl_auction_master_snapshot.joblib"
)

OUTPUT_DIR = PROJECT_ROOT / "data"


# ============================================================
# 2. LOAD SNAPSHOT
# ============================================================

bundle = joblib.load(SNAPSHOT_PATH)

model = bundle["final_auction_model"]
feature_columns = bundle["final_feature_columns"]

auction_features = bundle["auction_features"].copy()


# ============================================================
# 3. PREPARE FEATURES
# ============================================================

X = auction_features.copy()

# Temporary experience features
X["experience_years"] = 0

X["career_seasons_before"] = (
    X["batting_seasons_before"]
    +
    X["bowling_seasons_before"]
)

X["experience_known"] = 0


# Add any missing features
for column in feature_columns:

    if column not in X.columns:
        X[column] = 0


X = X[feature_columns]


# ============================================================
# 4. PREDICT
# ============================================================

predictions = model.predict(X)

auction_features["predicted_price_lakh"] = predictions

auction_features["error_lakh"] = (
    auction_features["predicted_price_lakh"]
    -
    auction_features["final_price_lakh"]
)

auction_features["absolute_error_lakh"] = (
    auction_features["error_lakh"]
    .abs()
)


# ============================================================
# 5. DUPLICATE PREDICTIONS
# ============================================================

prediction_counts = (
    auction_features[
        "predicted_price_lakh"
    ]
    .round(2)
    .value_counts()
)


print("\n========================================")
print("MOST COMMON PREDICTIONS")
print("========================================")

print(
    prediction_counts.head(15)
)


# ============================================================
# 6. UNKNOWN ROLE ANALYSIS
# ============================================================

unknown_role = auction_features[
    auction_features["role"]
    .astype(str)
    .str.lower()
    .eq("unknown")
]

known_role = auction_features[
    ~auction_features["role"]
    .astype(str)
    .str.lower()
    .eq("unknown")
]


print("\n========================================")
print("ROLE QUALITY")
print("========================================")

print(
    f"Total records       : {len(auction_features)}"
)

print(
    f"Known role records  : {len(known_role)}"
)

print(
    f"Unknown role records: {len(unknown_role)}"
)

print(
    f"Unknown role %      : "
    f"{len(unknown_role) / len(auction_features) * 100:.2f}%"
)


# ============================================================
# 7. ERROR BY ROLE
# ============================================================

role_analysis = (
    auction_features
    .groupby("role")
    .agg(
        records=("player_name", "count"),
        mae_lakh=(
            "absolute_error_lakh",
            "mean"
        ),
        average_actual=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)


role_analysis = role_analysis.sort_values(
    "mae_lakh",
    ascending=False
)


print("\n========================================")
print("ERROR BY ROLE")
print("========================================")

print(
    role_analysis.to_string(index=False)
)


# ============================================================
# 8. ERROR BY YEAR
# ============================================================

year_analysis = (
    auction_features
    .groupby("year")
    .agg(
        records=("player_name", "count"),
        mae_lakh=(
            "absolute_error_lakh",
            "mean"
        ),
        average_actual=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)


print("\n========================================")
print("ERROR BY YEAR")
print("========================================")

print(
    year_analysis.to_string(index=False)
)


# ============================================================
# 9. ERROR BY PRICE RANGE
# ============================================================

def price_range(price):

    if price < 100:
        return "< ₹1 Cr"

    elif price < 200:
        return "₹1–2 Cr"

    elif price < 500:
        return "₹2–5 Cr"

    elif price < 1000:
        return "₹5–10 Cr"

    else:
        return "₹10+ Cr"


auction_features["price_range"] = (
    auction_features["final_price_lakh"]
    .apply(price_range)
)


price_analysis = (
    auction_features
    .groupby("price_range")
    .agg(
        records=("player_name", "count"),
        mae_lakh=(
            "absolute_error_lakh",
            "mean"
        ),
        average_actual=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)


print("\n========================================")
print("ERROR BY PRICE RANGE")
print("========================================")

print(
    price_analysis.to_string(index=False)
)


# ============================================================
# 10. LARGEST ERRORS
# ============================================================

largest_errors = (
    auction_features
    .sort_values(
        "absolute_error_lakh",
        ascending=False
    )
    .head(20)
)


print("\n========================================")
print("20 LARGEST MODEL ERRORS")
print("========================================")

print(
    largest_errors[
        [
            "player_name",
            "year",
            "team",
            "role",
            "final_price_lakh",
            "predicted_price_lakh",
            "error_lakh",
            "absolute_error_lakh"
        ]
    ].to_string(index=False)
)


# ============================================================
# 11. 2023 VS 2026
# ============================================================

recent = auction_features[
    auction_features["year"].isin([2023, 2026])
]


recent_analysis = (
    recent
    .groupby("year")
    .agg(
        records=("player_name", "count"),
        mae_lakh=(
            "absolute_error_lakh",
            "mean"
        ),
        average_actual=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)


print("\n========================================")
print("2023 VS 2026")
print("========================================")

print(
    recent_analysis.to_string(index=False)
)


# ============================================================
# 12. SAVE DIAGNOSTICS
# ============================================================

auction_features.to_csv(
    OUTPUT_DIR / "model_diagnostics_predictions.csv",
    index=False
)

role_analysis.to_csv(
    OUTPUT_DIR / "diagnostics_by_role.csv",
    index=False
)

year_analysis.to_csv(
    OUTPUT_DIR / "diagnostics_by_year.csv",
    index=False
)

price_analysis.to_csv(
    OUTPUT_DIR / "diagnostics_by_price_range.csv",
    index=False
)

largest_errors.to_csv(
    OUTPUT_DIR / "largest_model_errors.csv",
    index=False
)


print("\n========================================")
print("DIAGNOSTIC FILES SAVED")
print("========================================")

print(
    OUTPUT_DIR / "model_diagnostics_predictions.csv"
)

print(
    OUTPUT_DIR / "diagnostics_by_role.csv"
)

print(
    OUTPUT_DIR / "diagnostics_by_year.csv"
)

print(
    OUTPUT_DIR / "diagnostics_by_price_range.csv"
)

print(
    OUTPUT_DIR / "largest_model_errors.csv"
)