import joblib
import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD MODEL SNAPSHOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "ipl_auction_master_snapshot.joblib"
)

snapshot = joblib.load(SNAPSHOT_PATH)

model = snapshot["final_auction_model"]
feature_columns = snapshot["final_feature_columns"]

auction_features = snapshot["auction_features"]
batting_season = snapshot["batting_season"]
bowling_season = snapshot["bowling_season"]


# ============================================================
# 2. FIND PLAYER
# ============================================================

def find_player(player_name):

    matches = auction_features[
        auction_features["player_name"]
        .astype(str)
        .str.lower()
        .str.contains(
            player_name.lower(),
            na=False
        )
    ]

    if matches.empty:
        raise ValueError(
            f"Player '{player_name}' was not found."
        )

    return matches


# ============================================================
# 3. PRE-AUCTION BATTING FEATURES
# ============================================================

def get_batting_features(player_id, auction_year):

    data = batting_season[
        (batting_season["player_id"] == player_id)
        &
        (batting_season["season"] < auction_year)
    ].copy()

    if data.empty:
        return {
            "career_runs_before": 0,
            "career_balls_before": 0,
            "career_innings_before": 0,
            "career_hundreds_before": 0,
            "career_fifties_before": 0,
            "career_fours_before": 0,
            "career_sixes_before": 0,
            "career_batting_sr_before": 0,
            "last_season_runs": 0,
            "last_season_balls": 0,
            "last_season_sr": 0,
            "last_season_fifties": 0,
            "last_season_hundreds": 0,
            "recent3_runs": 0,
            "recent3_fifties": 0,
            "recent3_hundreds": 0,
            "recent3_sr": 0,
            "batting_seasons_before": 0,
            "has_batting_history": 0,
        }

    data = data.sort_values("season")

    last = data.iloc[-1]
    recent3 = data.tail(3)

    career_runs = data["runs_scored"].sum()
    career_balls = data["balls_faced"].sum()
    career_innings = data["innings"].sum()

    career_fours = data["fours"].sum()
    career_sixes = data["sixes"].sum()

    career_hundreds = data["hundreds"].sum()
    career_fifties = data["fifties"].sum()

    career_sr = (
        career_runs / career_balls * 100
        if career_balls > 0
        else 0
    )

    recent3_runs = recent3["runs_scored"].sum()
    recent3_balls = recent3["balls_faced"].sum()

    recent3_sr = (
        recent3_runs / recent3_balls * 100
        if recent3_balls > 0
        else 0
    )

    return {
        "career_runs_before": career_runs,
        "career_balls_before": career_balls,
        "career_innings_before": career_innings,
        "career_hundreds_before": career_hundreds,
        "career_fifties_before": career_fifties,
        "career_fours_before": career_fours,
        "career_sixes_before": career_sixes,
        "career_batting_sr_before": career_sr,

        "last_season_runs": last["runs_scored"],
        "last_season_balls": last["balls_faced"],
        "last_season_sr": last["batting_strike_rate"],
        "last_season_fifties": last["fifties"],
        "last_season_hundreds": last["hundreds"],

        "recent3_runs": recent3_runs,
        "recent3_fifties": recent3["fifties"].sum(),
        "recent3_hundreds": recent3["hundreds"].sum(),
        "recent3_sr": recent3_sr,

        "batting_seasons_before": data["season"].nunique(),
        "has_batting_history": 1,
    }


# ============================================================
# 4. PRE-AUCTION BOWLING FEATURES
# ============================================================

def get_bowling_features(player_id, auction_year):

    data = bowling_season[
        (bowling_season["player_id"] == player_id)
        &
        (bowling_season["season"] < auction_year)
    ].copy()

    if data.empty:
        return {
            "career_wickets_before": 0,
            "career_balls_bowled_before": 0,
            "career_runs_conceded_before": 0,
            "career_3w_before": 0,
            "career_4w_before": 0,
            "career_5w_before": 0,
            "career_economy_before": 0,
            "last_season_wickets": 0,
            "last_season_economy": 0,
            "last_season_balls_bowled": 0,
            "recent3_wickets": 0,
            "recent3_balls_bowled": 0,
            "recent3_economy": 0,
            "bowling_seasons_before": 0,
            "has_bowling_history": 0,
        }

    data = data.sort_values("season")

    last = data.iloc[-1]
    recent3 = data.tail(3)

    career_wickets = data["total_wickets"].sum()
    career_balls = data["balls_bowled"].sum()
    career_runs = data["total_runs_conceded"].sum()

    career_economy = (
        career_runs / career_balls * 6
        if career_balls > 0
        else 0
    )

    recent3_balls = recent3["balls_bowled"].sum()
    recent3_runs = recent3["total_runs_conceded"].sum()

    recent3_economy = (
        recent3_runs / recent3_balls * 6
        if recent3_balls > 0
        else 0
    )

    return {
        "career_wickets_before": career_wickets,
        "career_balls_bowled_before": career_balls,
        "career_runs_conceded_before": career_runs,
        "career_3w_before": data["three_wicket_hauls"].sum(),
        "career_4w_before": data["four_wicket_hauls"].sum(),
        "career_5w_before": data["five_wicket_hauls"].sum(),
        "career_economy_before": career_economy,

        "last_season_wickets": last["total_wickets"],
        "last_season_economy": last["economy_rate"],
        "last_season_balls_bowled": last["balls_bowled"],

        "recent3_wickets": recent3["total_wickets"].sum(),
        "recent3_balls_bowled": recent3_balls,
        "recent3_economy": recent3_economy,

        "bowling_seasons_before": data["season"].nunique(),
        "has_bowling_history": 1,
    }


# ============================================================
# 5. PREVIOUS AUCTION FEATURES
# ============================================================

def get_previous_auction_features(
    player_name,
    auction_year
):

    data = auction_features[
        auction_features["player_name"]
        .astype(str)
        .str.lower()
        ==
        player_name.lower()
    ].copy()

    data = data[
        data["year"] < auction_year
    ]

    if data.empty:

        return {
            "previous_auction_price": 0,
            "previous_auction_count": 0,
        }

    data = data.sort_values("year")

    return {
        "previous_auction_price":
            data.iloc[-1]["final_price_lakh"],

        "previous_auction_count":
            len(data),
    }


# ============================================================
# 6. BUILD COMPLETE PRE-AUCTION FEATURE ROW
# ============================================================

def build_prediction_features(
    player_name,
    auction_year
):

    matches = find_player(player_name)

    # Most recent known player record
    player = matches.sort_values("year").iloc[-1]

    player_id = player["player_id"]

    # ----------------------------------------
    # Basic information
    # ----------------------------------------

    row = {
        "role": player["role"],
        "nationality": player["nationality"],
    }

    # ----------------------------------------
    # Batting
    # ----------------------------------------

    row.update(
        get_batting_features(
            player_id,
            auction_year
        )
    )

    # ----------------------------------------
    # Bowling
    # ----------------------------------------

    row.update(
        get_bowling_features(
            player_id,
            auction_year
        )
    )

    # ----------------------------------------
    # Previous auction
    # ----------------------------------------

    row.update(
        get_previous_auction_features(
            player_name,
            auction_year
        )
    )

    # ----------------------------------------
    # Temporary experience features
    # ----------------------------------------

    row["experience_years"] = 0
    row["career_seasons_before"] = (
        row["batting_seasons_before"]
        + row["bowling_seasons_before"]
    )
    row["experience_known"] = 0

    # ----------------------------------------
    # Create DataFrame
    # ----------------------------------------

    df = pd.DataFrame([row])

    # Add missing model features
    for column in feature_columns:

        if column not in df.columns:
            df[column] = 0

    # Keep EXACT model order
    df = df[feature_columns]

    return df


# ============================================================
# 7. PREDICT
# ============================================================

def predict_auction_price(
    player_name,
    auction_year
):

    features = build_prediction_features(
        player_name,
        auction_year
    )

    prediction = model.predict(features)[0]

    return {
        "player": player_name,
        "auction_year": auction_year,
        "predicted_price_lakh": round(
            float(prediction),
            2
        ),
        "predicted_price_crore": round(
            float(prediction) / 100,
            2
        ),
    }


# ============================================================
# 8. TEST
# ============================================================

if __name__ == "__main__":

    result = predict_auction_price(
        player_name="Virat Kohli",
        auction_year=2026
    )

    print("\n===================================")
    print("IPL AUCTION PRICE PREDICTION")
    print("===================================")

    print(
        f"Player: {result['player']}"
    )

    print(
        f"Auction Year: {result['auction_year']}"
    )

    print(
        f"Predicted Price: "
        f"₹{result['predicted_price_crore']} Cr"
    )

    print(
        f"Predicted Price: "
        f"₹{result['predicted_price_lakh']} Lakh"
    )