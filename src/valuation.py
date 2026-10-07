import numpy as np
import pandas as pd


# ============================================================
# NAME NORMALIZATION
# ============================================================

def normalize_name(x):
    if pd.isna(x):
        return ""

    return (
        str(x)
        .strip()
        .lower()
        .replace(".", "")
        .replace("-", " ")
        .replace("'", "")
        .replace("  ", " ")
    )


# ============================================================
# SAFE CONVERSION HELPERS
# ============================================================

def safe_float(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


# ============================================================
# PRE-AUCTION PERFORMANCE FEATURES
# ============================================================

def get_pre_auction_features(bundle, player_id, auction_year):

    batting_season = bundle["batting_season"]
    bowling_season = bundle["bowling_season"]

    auction_year = int(auction_year)

    features = {}

    # --------------------------------------------------------
    # BATTING
    # --------------------------------------------------------

    bat = batting_season[
        (batting_season["player_id"] == player_id)
        & (batting_season["season"] < auction_year)
    ].sort_values("season")

    if len(bat) > 0:

        features["career_runs_before"] = bat["runs_scored"].sum()
        features["career_balls_before"] = bat["balls_faced"].sum()
        features["career_innings_before"] = bat["innings"].sum()

        features["career_hundreds_before"] = bat["hundreds"].sum()
        features["career_fifties_before"] = bat["fifties"].sum()
        features["career_fours_before"] = bat["fours"].sum()
        features["career_sixes_before"] = bat["sixes"].sum()

        total_balls = bat["balls_faced"].sum()

        features["career_batting_sr_before"] = (
            bat["runs_scored"].sum() / total_balls * 100
            if total_balls > 0
            else 0
        )

        # Last season

        last = bat.iloc[-1]

        features["last_season_runs"] = safe_float(
            last["runs_scored"]
        )

        features["last_season_balls"] = safe_float(
            last["balls_faced"]
        )

        features["last_season_sr"] = safe_float(
            last["batting_strike_rate"]
        )

        features["last_season_fifties"] = safe_float(
            last["fifties"]
        )

        features["last_season_hundreds"] = safe_float(
            last["hundreds"]
        )

        # Recent 3 seasons

        recent3 = bat.tail(3)

        features["recent3_runs"] = recent3["runs_scored"].sum()
        features["recent3_fifties"] = recent3["fifties"].sum()
        features["recent3_hundreds"] = recent3["hundreds"].sum()

        recent3_balls = recent3["balls_faced"].sum()

        features["recent3_sr"] = (
            recent3["runs_scored"].sum()
            / recent3_balls
            * 100
            if recent3_balls > 0
            else 0
        )

        features["batting_seasons_before"] = len(bat)

    else:

        batting_defaults = [
            "career_runs_before",
            "career_balls_before",
            "career_innings_before",
            "career_hundreds_before",
            "career_fifties_before",
            "career_fours_before",
            "career_sixes_before",
            "career_batting_sr_before",
            "last_season_runs",
            "last_season_balls",
            "last_season_sr",
            "last_season_fifties",
            "last_season_hundreds",
            "recent3_runs",
            "recent3_fifties",
            "recent3_hundreds",
            "recent3_sr",
        ]

        for column in batting_defaults:
            features[column] = 0

        features["batting_seasons_before"] = 0

    # --------------------------------------------------------
    # BOWLING
    # --------------------------------------------------------

    bowl = bowling_season[
        (bowling_season["player_id"] == player_id)
        & (bowling_season["season"] < auction_year)
    ].sort_values("season")

    if len(bowl) > 0:

        features["career_wickets_before"] = bowl[
            "total_wickets"
        ].sum()

        features["career_balls_bowled_before"] = bowl[
            "balls_bowled"
        ].sum()

        features["career_runs_conceded_before"] = bowl[
            "total_runs_conceded"
        ].sum()

        features["career_3w_before"] = bowl[
            "three_wicket_hauls"
        ].sum()

        features["career_4w_before"] = bowl[
            "four_wicket_hauls"
        ].sum()

        features["career_5w_before"] = bowl[
            "five_wicket_hauls"
        ].sum()

        total_balls = bowl["balls_bowled"].sum()

        features["career_economy_before"] = (
            bowl["total_runs_conceded"].sum()
            / total_balls
            * 6
            if total_balls > 0
            else 0
        )

        # Last season

        last = bowl.iloc[-1]

        features["last_season_wickets"] = safe_float(
            last["total_wickets"]
        )

        features["last_season_economy"] = safe_float(
            last["economy_rate"]
        )

        features["last_season_balls_bowled"] = safe_float(
            last["balls_bowled"]
        )

        # Recent 3 seasons

        recent3 = bowl.tail(3)

        features["recent3_wickets"] = recent3[
            "total_wickets"
        ].sum()

        features["recent3_balls_bowled"] = recent3[
            "balls_bowled"
        ].sum()

        recent3_balls = recent3[
            "balls_bowled"
        ].sum()

        features["recent3_economy"] = (
            recent3["total_runs_conceded"].sum()
            / recent3_balls
            * 6
            if recent3_balls > 0
            else 0
        )

        features["bowling_seasons_before"] = len(bowl)

    else:

        bowling_defaults = [
            "career_wickets_before",
            "career_balls_bowled_before",
            "career_runs_conceded_before",
            "career_3w_before",
            "career_4w_before",
            "career_5w_before",
            "career_economy_before",
            "last_season_wickets",
            "last_season_economy",
            "last_season_balls_bowled",
            "recent3_wickets",
            "recent3_balls_bowled",
            "recent3_economy",
        ]

        for column in bowling_defaults:
            features[column] = 0

        features["bowling_seasons_before"] = 0

    return features


# ============================================================
# BUILD PLAYER NAME → PLAYER ID
# ============================================================

def build_player_name_to_id(bundle):

    player_lookup = bundle["player_lookup"].copy()

    if "name_norm" not in player_lookup.columns:

        if "player_name" not in player_lookup.columns:
            raise KeyError(
                "player_lookup must contain 'player_name'."
            )

        player_lookup["name_norm"] = (
            player_lookup["player_name"]
            .apply(normalize_name)
        )

    mapping = {}

    for _, row in player_lookup.iterrows():

        player_id = row.get("player_id")
        name_norm = row.get("name_norm")

        if pd.notna(player_id) and name_norm:

            mapping[name_norm] = player_id

    return mapping


# ============================================================
# GET DEBUT YEAR
# ============================================================

def get_debut_year(bundle, player_id):

    player_lookup = bundle["player_lookup"]
    players = bundle["players"]

    # First try player_lookup

    if "debut_year" in player_lookup.columns:

        rows = player_lookup[
            player_lookup["player_id"] == player_id
        ]

        if len(rows) > 0:

            value = rows.iloc[0]["debut_year"]

            if pd.notna(value):

                try:
                    return int(value)
                except (TypeError, ValueError):
                    pass

    # Fallback to players table

    if (
        "player_name" in player_lookup.columns
        and "player_name" in players.columns
        and "debut_year" in players.columns
    ):

        rows = player_lookup[
            player_lookup["player_id"] == player_id
        ]

        if len(rows) > 0:

            player_name = rows.iloc[0]["player_name"]

            player_rows = players[
                players["player_name"] == player_name
            ]

            if len(player_rows) > 0:

                value = player_rows.iloc[0][
                    "debut_year"
                ]

                if pd.notna(value):

                    try:
                        return int(value)
                    except (TypeError, ValueError):
                        pass

    return None


# ============================================================
# VALUATION RANGE
# ============================================================

def get_valuation_range(
    bundle,
    predicted_price_lakh,
):

    predicted_price_lakh = max(
        0,
        safe_float(predicted_price_lakh),
    )

    # Empirical errors from the official temporal
    # holdout evaluation.

    median_error = safe_float(
        bundle.get("median_absolute_error", 106.45),
        106.45,
    )

    percentile_75_error = safe_float(
        bundle.get("error_75th_percentile", 206.06),
        206.06,
    )

    typical_low = max(
        0,
        predicted_price_lakh - median_error,
    )

    typical_high = (
        predicted_price_lakh + median_error
    )

    wider_low = max(
        0,
        predicted_price_lakh - percentile_75_error,
    )

    wider_high = (
        predicted_price_lakh + percentile_75_error
    )

    return {
        "predicted_price_lakh": round(
            predicted_price_lakh,
            2,
        ),

        "predicted_price_crore": round(
            predicted_price_lakh / 100,
            2,
        ),

        "typical_low_lakh": round(
            typical_low,
            2,
        ),

        "typical_high_lakh": round(
            typical_high,
            2,
        ),

        "typical_low_crore": round(
            typical_low / 100,
            2,
        ),

        "typical_high_crore": round(
            typical_high / 100,
            2,
        ),

        "wider_low_lakh": round(
            wider_low,
            2,
        ),

        "wider_high_lakh": round(
            wider_high,
            2,
        ),

        "wider_low_crore": round(
            wider_low / 100,
            2,
        ),

        "wider_high_crore": round(
            wider_high / 100,
            2,
        ),
    }


# ============================================================
# VALUATION SEGMENT
# ============================================================

def get_valuation_segment(predicted_price_lakh):

    price = safe_float(predicted_price_lakh)

    if price < 50:
        return "Lower Value"

    if price < 250:
        return "Mid Value"

    if price < 500:
        return "Upper-Mid Value"

    if price < 1000:
        return "High Value"

    return "Premium / Elite"


# ============================================================
# PLAYER PREDICTION
# ============================================================

def predict_player_valuation(
    bundle,
    player_name,
    auction_year,
    role,
    nationality,
):

    model = bundle["model"]

    feature_columns = bundle["feature_columns"]

    auction_features = bundle["auction_features"]

    player_lookup = bundle["player_lookup"]

    # --------------------------------------------------------
    # PLAYER ID
    # --------------------------------------------------------

    player_name_to_id = bundle.get(
        "player_name_to_id"
    )

    if player_name_to_id is None:

        player_name_to_id = build_player_name_to_id(
            bundle
        )

    normalized_name = normalize_name(
        player_name
    )

    player_id = player_name_to_id.get(
        normalized_name
    )

    if player_id is None:

        raise ValueError(
            f"Player '{player_name}' was not found "
            "in the player registry."
        )

    auction_year = int(auction_year)

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    performance = get_pre_auction_features(
        bundle,
        player_id,
        auction_year,
    )

    row = performance.copy()

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    valid_roles = [
        "Batsman",
        "Bowler",
        "All-Rounder",
        "Wicket-Keeper",
        "Unknown",
    ]

    if pd.isna(role) or role not in valid_roles:
        role = "Unknown"

    row["role"] = role

    # --------------------------------------------------------
    # NATIONALITY
    # --------------------------------------------------------

    if pd.isna(nationality) or not nationality:
        nationality = "Unknown"

    row["nationality"] = nationality

    # --------------------------------------------------------
    # PREVIOUS AUCTION HISTORY
    # --------------------------------------------------------

    previous_auctions = auction_features[
        (auction_features["player_id"] == player_id)
        & (
            auction_features["year"]
            < auction_year
        )
    ].sort_values("year")

    if len(previous_auctions) > 0:

        row["previous_auction_price"] = (
            previous_auctions.iloc[-1][
                "final_price_lakh"
            ]
        )

        row["previous_auction_count"] = (
            len(previous_auctions)
        )

    else:

        row["previous_auction_price"] = 0
        row["previous_auction_count"] = 0

    # --------------------------------------------------------
    # HISTORY FLAGS
    # --------------------------------------------------------

    row["has_batting_history"] = int(
        row["batting_seasons_before"] > 0
    )

    row["has_bowling_history"] = int(
        row["bowling_seasons_before"] > 0
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    debut_year = get_debut_year(
        bundle,
        player_id,
    )

    if debut_year is not None:

        experience_years = max(
            0,
            auction_year - debut_year,
        )

        experience_known = 1

    else:

        experience_years = 0
        experience_known = 0

    row["experience_years"] = (
        experience_years
    )

    row["experience_known"] = (
        experience_known
    )

    # --------------------------------------------------------
    # CAREER SEASONS
    # --------------------------------------------------------

    batting_season = bundle["batting_season"]
    bowling_season = bundle["bowling_season"]

    bat_seasons = batting_season[
        batting_season["player_id"] == player_id
    ][["season"]]

    bowl_seasons = bowling_season[
        bowling_season["player_id"] == player_id
    ][["season"]]

    all_seasons = pd.concat(
        [
            bat_seasons,
            bowl_seasons,
        ],
        ignore_index=True,
    ).drop_duplicates()

    career_seasons_before = all_seasons[
        all_seasons["season"] < auction_year
    ].shape[0]

    row["career_seasons_before"] = (
        career_seasons_before
    )

    # --------------------------------------------------------
    # PREPARE MODEL INPUT
    # --------------------------------------------------------

    prediction_df = pd.DataFrame([row])

    # Ensure every expected feature exists.

    for column in feature_columns:

        if column not in prediction_df.columns:
            prediction_df[column] = 0

    prediction_df = prediction_df[
        feature_columns
    ]

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predicted_price = model.predict(
        prediction_df
    )[0]

    predicted_price = max(
        0,
        float(predicted_price),
    )

    return {
        "player_name": player_name,
        "player_id": player_id,
        "auction_year": auction_year,
        "role": role,
        "nationality": nationality,
        "predicted_price_lakh": round(
            predicted_price,
            2,
        ),
        "predicted_price_crore": round(
            predicted_price / 100,
            2,
        ),
        "experience_years": (
            experience_years
            if experience_known
            else None
        ),
        "experience_known": experience_known,
    }


# ============================================================
# COMPLETE VALUATION REPORT
# ============================================================

def generate_valuation_report(
    player_name,
    auction_year,
    role,
    nationality,
):

    # Import here to avoid circular imports.

    from src.model_loader import load_model_bundle

    bundle = load_model_bundle()

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    prediction = predict_player_valuation(
        bundle=bundle,
        player_name=player_name,
        auction_year=auction_year,
        role=role,
        nationality=nationality,
    )

    # --------------------------------------------------------
    # RANGE
    # --------------------------------------------------------

    valuation = get_valuation_range(
        bundle,
        prediction["predicted_price_lakh"],
    )

    player_id = prediction["player_id"]

    auction_year = int(auction_year)

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    performance = get_pre_auction_features(
        bundle,
        player_id,
        auction_year,
    )

    # --------------------------------------------------------
    # DEBUT / EXPERIENCE
    # --------------------------------------------------------

    debut_year = get_debut_year(
        bundle,
        player_id,
    )

    if debut_year is not None:

        experience_years = max(
            0,
            auction_year - debut_year,
        )

    else:

        experience_years = None

    # --------------------------------------------------------
    # PREVIOUS AUCTIONS
    # --------------------------------------------------------

    auction_features = bundle[
        "auction_features"
    ]

    previous_auctions = auction_features[
        (auction_features["player_id"] == player_id)
        & (
            auction_features["year"]
            < auction_year
        )
    ].sort_values("year")

    previous_auction_count = len(
        previous_auctions
    )

    if previous_auction_count > 0:

        previous_auction_price = safe_float(
            previous_auctions.iloc[-1][
                "final_price_lakh"
            ]
        )

    else:

        previous_auction_price = 0

    # --------------------------------------------------------
    # SEGMENT
    # --------------------------------------------------------

    valuation_segment = get_valuation_segment(
        prediction["predicted_price_lakh"]
    )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    return {
        "Player":
            player_name,

        "Player ID":
            player_id,

        "Auction Year":
            auction_year,

        "Role":
            prediction["role"],

        "Nationality":
            prediction["nationality"],

        "Debut Year":
            (
                debut_year
                if debut_year is not None
                else "Unknown"
            ),

        "Experience (Years)":
            (
                experience_years
                if experience_years is not None
                else "Unknown"
            ),

        "Previous Auctions":
            previous_auction_count,

        "Previous Auction Price (₹L)":
            previous_auction_price,

        "Career Runs Before Auction":
            safe_float(
                performance.get(
                    "career_runs_before",
                    0,
                )
            ),

        "Recent 3 Seasons Runs":
            safe_float(
                performance.get(
                    "recent3_runs",
                    0,
                )
            ),

        "Last Season Runs":
            safe_float(
                performance.get(
                    "last_season_runs",
                    0,
                )
            ),

        "Career Wickets Before Auction":
            safe_float(
                performance.get(
                    "career_wickets_before",
                    0,
                )
            ),

        "Recent 3 Seasons Wickets":
            safe_float(
                performance.get(
                    "recent3_wickets",
                    0,
                )
            ),

        "Career Batting SR Before Auction":
            safe_float(
                performance.get(
                    "career_batting_sr_before",
                    0,
                )
            ),

        "Last Season SR":
            safe_float(
                performance.get(
                    "last_season_sr",
                    0,
                )
            ),

        "Recent 3 Seasons SR":
            safe_float(
                performance.get(
                    "recent3_sr",
                    0,
                )
            ),

        "Last Season Wickets":
            safe_float(
                performance.get(
                    "last_season_wickets",
                    0,
                )
            ),

        "Last Season Economy":
            safe_float(
                performance.get(
                    "last_season_economy",
                    0,
                )
            ),

        "Predicted Value (₹L)":
            valuation[
                "predicted_price_lakh"
            ],

        "Predicted Value (₹Cr)":
            valuation[
                "predicted_price_crore"
            ],

        "Typical Range (₹Cr)":
            (
                f"₹{valuation['typical_low_crore']:.2f}"
                f" – "
                f"₹{valuation['typical_high_crore']:.2f}"
            ),

        "Wider Range (₹Cr)":
            (
                f"₹{valuation['wider_low_crore']:.2f}"
                f" – "
                f"₹{valuation['wider_high_crore']:.2f}"
            ),

        "Typical Low (₹Cr)":
            valuation["typical_low_crore"],

        "Typical High (₹Cr)":
            valuation["typical_high_crore"],

        "Wider Low (₹Cr)":
            valuation["wider_low_crore"],

        "Wider High (₹Cr)":
            valuation["wider_high_crore"],

        "Valuation Segment":
            valuation_segment,
    }