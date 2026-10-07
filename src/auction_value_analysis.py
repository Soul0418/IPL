import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "chronological_evaluation.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

# Make sure required columns exist
required_columns = [
    "player_name",
    "year",
    "team",
    "role",
    "final_price_lakh",
    "predicted_price_lakh"
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )


# ============================================================
# 3. VALUE GAP
# ============================================================

df["value_gap_lakh"] = (
    df["predicted_price_lakh"]
    -
    df["final_price_lakh"]
)

df["value_gap_crore"] = (
    df["value_gap_lakh"] / 100
)


# ============================================================
# 4. VALUE RATIO
# ============================================================

df["value_ratio"] = np.where(
    df["final_price_lakh"] > 0,
    df["predicted_price_lakh"]
    /
    df["final_price_lakh"],
    np.nan
)


# ============================================================
# 5. VALUE CLASSIFICATION
# ============================================================

def classify_value(gap):

    if gap >= 100:
        return "Undervalued"

    elif gap <= -100:
        return "Overvalued"

    else:
        return "Fair Value"


df["value_class"] = (
    df["value_gap_lakh"]
    .apply(classify_value)
)


# ============================================================
# 6. TOP UNDERVALUED PLAYERS
# ============================================================

undervalued = df[
    df["value_gap_lakh"] > 0
].sort_values(
    "value_gap_lakh",
    ascending=False
).head(10)


print("\n========================================")
print("TOP 10 UNDERVALUED PLAYERS")
print("========================================")

print(
    undervalued[
        [
            "player_name",
            "year",
            "team",
            "role",
            "final_price_lakh",
            "predicted_price_lakh",
            "value_gap_crore",
            "value_ratio"
        ]
    ].to_string(index=False)
)


# ============================================================
# 7. TOP OVERVALUED PLAYERS
# ============================================================

overvalued = df[
    df["value_gap_lakh"] < 0
].sort_values(
    "value_gap_lakh"
).head(10)


print("\n========================================")
print("TOP 10 OVERVALUED PLAYERS")
print("========================================")

print(
    overvalued[
        [
            "player_name",
            "year",
            "team",
            "role",
            "final_price_lakh",
            "predicted_price_lakh",
            "value_gap_crore",
            "value_ratio"
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. BEST VALUE PLAYERS
# ============================================================

# We don't want extremely cheap players with tiny absolute
# differences dominating the ranking.

best_value = df[
    (df["final_price_lakh"] >= 100)
    &
    (df["value_ratio"] >= 1.25)
].sort_values(
    "value_ratio",
    ascending=False
).head(10)


print("\n========================================")
print("BEST VALUE PLAYERS")
print("========================================")

print(
    best_value[
        [
            "player_name",
            "year",
            "team",
            "role",
            "final_price_lakh",
            "predicted_price_lakh",
            "value_gap_crore",
            "value_ratio"
        ]
    ].to_string(index=False)
)


# ============================================================
# 9. VALUE CLASS DISTRIBUTION
# ============================================================

print("\n========================================")
print("VALUE CLASS DISTRIBUTION")
print("========================================")

print(
    df["value_class"]
    .value_counts()
    .to_string()
)


# ============================================================
# 10. TEAM-WISE VALUE ANALYSIS
# ============================================================

team_analysis = (
    df.groupby("team")
    .agg(
        players=("player_name", "count"),
        total_spend_lakh=("final_price_lakh", "sum"),
        predicted_spend_lakh=(
            "predicted_price_lakh",
            "sum"
        ),
        average_actual_price=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted_price=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)

team_analysis["team_value_gap_lakh"] = (
    team_analysis["predicted_spend_lakh"]
    -
    team_analysis["total_spend_lakh"]
)

team_analysis["team_value_gap_crore"] = (
    team_analysis["team_value_gap_lakh"]
    / 100
)

team_analysis = team_analysis.sort_values(
    "team_value_gap_lakh",
    ascending=False
)


print("\n========================================")
print("TEAM-WISE VALUE ANALYSIS")
print("========================================")

print(
    team_analysis.to_string(index=False)
)


# ============================================================
# 11. ROLE-WISE VALUE ANALYSIS
# ============================================================

role_analysis = (
    df.groupby("role")
    .agg(
        players=("player_name", "count"),
        total_spend_lakh=(
            "final_price_lakh",
            "sum"
        ),
        predicted_spend_lakh=(
            "predicted_price_lakh",
            "sum"
        ),
        average_actual_price=(
            "final_price_lakh",
            "mean"
        ),
        average_predicted_price=(
            "predicted_price_lakh",
            "mean"
        )
    )
    .reset_index()
)

role_analysis["value_gap_lakh"] = (
    role_analysis["predicted_spend_lakh"]
    -
    role_analysis["total_spend_lakh"]
)


print("\n========================================")
print("ROLE-WISE VALUE ANALYSIS")
print("========================================")

print(
    role_analysis.to_string(index=False)
)


# ============================================================
# 12. SAVE RESULTS
# ============================================================

df.to_csv(
    OUTPUT_DIR / "auction_value_analysis.csv",
    index=False
)

undervalued.to_csv(
    OUTPUT_DIR / "top_undervalued_players.csv",
    index=False
)

overvalued.to_csv(
    OUTPUT_DIR / "top_overvalued_players.csv",
    index=False
)

best_value.to_csv(
    OUTPUT_DIR / "best_value_players.csv",
    index=False
)

team_analysis.to_csv(
    OUTPUT_DIR / "team_value_analysis.csv",
    index=False
)

role_analysis.to_csv(
    OUTPUT_DIR / "role_value_analysis.csv",
    index=False
)


print("\n========================================")
print("FILES SAVED")
print("========================================")

print(
    OUTPUT_DIR / "auction_value_analysis.csv"
)

print(
    OUTPUT_DIR / "top_undervalued_players.csv"
)

print(
    OUTPUT_DIR / "top_overvalued_players.csv"
)

print(
    OUTPUT_DIR / "best_value_players.csv"
)

print(
    OUTPUT_DIR / "team_value_analysis.csv"
)

print(
    OUTPUT_DIR / "role_value_analysis.csv"
)