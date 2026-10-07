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

df = df.dropna(
    subset=["final_price_lakh"]
).copy()

df = df.sort_values("year")


# ============================================================
# 3. TEMPORARY EXPERIENCE FEATURES
# ============================================================

df["experience_years"] = 0

df["career_seasons_before"] = (
    df["batting_seasons_before"].fillna(0)
    +
    df["bowling_seasons_before"].fillna(0)
)

df["experience_known"] = 0


# ============================================================
# 4. CREATE MODEL INPUT
# ============================================================

X = df.copy()

for column in feature_columns:

    if column not in X.columns:
        X[column] = 0

X = X[feature_columns]


# ============================================================
# 5. PREDICT ALL AUCTIONS
# ============================================================

df["predicted_price_lakh"] = model.predict(X)


# ============================================================
# 6. TRAIN / TEST PERIODS
# ============================================================

TRAIN_END_YEAR = 2022

train_df = df[
    df["year"] <= TRAIN_END_YEAR
].copy()

test_df = df[
    df["year"] > TRAIN_END_YEAR
].copy()


# ============================================================
# 7. EVALUATION FUNCTION
# ============================================================

def evaluate(data, label):

    actual = data["final_price_lakh"]
    predicted = data["predicted_price_lakh"]

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    r2 = r2_score(
        actual,
        predicted
    )

    print("\n========================================")
    print(label)
    print("========================================")

    print(
        f"Records : {len(data)}"
    )

    print(
        f"MAE     : ₹{mae:.2f} Lakh "
        f"(₹{mae / 100:.2f} Cr)"
    )

    print(
        f"RMSE    : ₹{rmse:.2f} Lakh "
        f"(₹{rmse / 100:.2f} Cr)"
    )

    print(
        f"R²      : {r2:.4f}"
    )

    return mae, rmse, r2


# ============================================================
# 8. TRAINING PERIOD PERFORMANCE
# ============================================================

evaluate(
    train_df,
    "TRAINING PERIOD: 2008–2022"
)


# ============================================================
# 9. FUTURE PERIOD PERFORMANCE
# ============================================================

evaluate(
    test_df,
    "FUTURE TEST PERIOD: 2023–2026"
)


# ============================================================
# 10. TEST PERFORMANCE BY YEAR
# ============================================================

print("\n========================================")
print("TEST PERFORMANCE BY YEAR")
print("========================================")

for year in sorted(test_df["year"].unique()):

    yearly = test_df[
        test_df["year"] == year
    ]

    actual = yearly["final_price_lakh"]
    predicted = yearly["predicted_price_lakh"]

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    r2 = (
        r2_score(actual, predicted)
        if len(yearly) > 1
        else float("nan")
    )

    print(
        f"{year}: "
        f"Records={len(yearly):3d} | "
        f"MAE=₹{mae:.2f}L | "
        f"RMSE=₹{rmse:.2f}L | "
        f"R²={r2:.3f}"
    )


# ============================================================
# 11. PERFORMANCE BY PRICE RANGE
# ============================================================

print("\n========================================")
print("TEST PERFORMANCE BY PRICE RANGE")
print("========================================")

test_df["price_category"] = pd.cut(
    test_df["final_price_lakh"],
    bins=[
        -np.inf,
        200,
        500,
        1000,
        np.inf
    ],
    labels=[
        "₹0–2 Cr",
        "₹2–5 Cr",
        "₹5–10 Cr",
        "₹10+ Cr"
    ]
)

for category in test_df["price_category"].dropna().unique():

    group = test_df[
        test_df["price_category"] == category
    ]

    actual = group["final_price_lakh"]
    predicted = group["predicted_price_lakh"]

    mae = mean_absolute_error(
        actual,
        predicted
    )

    print(
        f"{category}: "
        f"Records={len(group):3d} | "
        f"MAE=₹{mae:.2f}L "
        f"(₹{mae / 100:.2f} Cr)"
    )


# ============================================================
# 12. LARGEST FUTURE PREDICTION ERRORS
# ============================================================

test_df["error_lakh"] = (
    test_df["predicted_price_lakh"]
    -
    test_df["final_price_lakh"]
)

test_df["absolute_error_lakh"] = (
    test_df["error_lakh"].abs()
)

print("\n========================================")
print("LARGEST FUTURE PREDICTION ERRORS")
print("========================================")

worst = test_df.sort_values(
    "absolute_error_lakh",
    ascending=False
).head(15)

print(
    worst[
        [
            "player_name",
            "year",
            "final_price_lakh",
            "predicted_price_lakh",
            "error_lakh"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. SAVE TEST RESULTS
# ============================================================

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "chronological_evaluation.csv"
)

test_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    "\nResults saved to:"
)

print(OUTPUT_PATH)