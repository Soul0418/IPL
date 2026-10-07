from pathlib import Path
import sys
import html
import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from src.model_loader import load_model_bundle
from src.valuation import generate_valuation_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IPL Auction Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
<style>

:root {
    --bg: #070b12;
    --panel: #0d1421;
    --panel-2: #111a2a;
    --panel-3: #151f31;
    --border: #24334b;
    --border-light: #30425d;

    --text: #f4f7fb;
    --muted: #94a3b8;
    --muted-2: #64748b;

    --blue: #60a5fa;
    --blue-2: #3b82f6;
    --cyan: #22d3ee;

    --green: #34d399;
    --yellow: #fbbf24;
    --orange: #fb923c;
    --red: #f87171;
}

html, body {
    background: var(--bg);
}

.main {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(37, 99, 235, 0.08),
            transparent 32%
        ),
        var(--bg);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ------------------------------------------------------------
   HERO
------------------------------------------------------------ */

.hero {
    position: relative;
    overflow: hidden;

    padding: 38px 42px;
    margin-bottom: 28px;

    border: 1px solid #24334b;
    border-radius: 20px;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(59, 130, 246, 0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0d1625 0%,
            #0b1220 55%,
            #0a101b 100%
        );

    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.30);
}

.hero::after {
    content: "";
    position: absolute;

    width: 260px;
    height: 260px;

    right: -100px;
    bottom: -150px;

    border-radius: 50%;

    background: rgba(34, 211, 238, 0.07);
    filter: blur(10px);
}

.hero-eyebrow {
    color: #60a5fa;
    font-size: 12px;
    font-weight: 800;

    letter-spacing: 0.18em;
    text-transform: uppercase;

    margin-bottom: 12px;
}

.hero-title {
    color: #f8fafc;

    font-size: 38px;
    line-height: 1.1;

    font-weight: 800;
    letter-spacing: -0.04em;

    margin-bottom: 14px;
}

.hero-subtitle {
    max-width: 760px;

    color: #94a3b8;

    font-size: 15px;
    line-height: 1.7;
}


/* ------------------------------------------------------------
   SECTION
------------------------------------------------------------ */

.section-title {
    color: #f8fafc;

    font-size: 21px;
    font-weight: 750;

    margin: 30px 0 5px 0;
}

.section-subtitle {
    color: #64748b;

    font-size: 13px;

    margin-bottom: 18px;
}


/* ------------------------------------------------------------
   STAT CARDS
------------------------------------------------------------ */

.stat-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px;
}

.stat-card {
    min-height: 126px;

    padding: 20px;

    border: 1px solid #24334b;
    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            #101a2b,
            #0d1522
        );

    box-shadow:
        0 15px 35px rgba(0, 0, 0, 0.18);
}

.stat-label {
    color: #64748b;

    font-size: 11px;
    font-weight: 700;

    letter-spacing: 0.08em;
    text-transform: uppercase;

    margin-bottom: 12px;
}

.stat-value {
    color: #f8fafc;

    font-size: 27px;
    font-weight: 800;

    letter-spacing: -0.03em;
}

.stat-description {
    color: #64748b;

    font-size: 11px;

    margin-top: 7px;
}


/* ------------------------------------------------------------
   VALUATION
------------------------------------------------------------ */

.valuation-grid {
    display: grid;

    grid-template-columns:
        1.35fr
        1fr
        1fr;

    gap: 16px;

    margin-top: 20px;
}

.valuation-main {
    padding: 28px;

    border: 1px solid #2563eb;

    border-radius: 18px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(59, 130, 246, 0.18),
            transparent 42%
        ),
        linear-gradient(
            145deg,
            #0f1d34,
            #0c1524
        );
}

.valuation-label {
    color: #93c5fd;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.valuation-price {
    color: #f8fafc;

    font-size: 48px;
    font-weight: 850;

    line-height: 1;

    margin-top: 13px;

    letter-spacing: -0.05em;
}

.valuation-lakh {
    color: #64748b;

    font-size: 12px;

    margin-top: 10px;
}

.range-card {
    padding: 24px;

    border: 1px solid #24334b;
    border-radius: 18px;

    background: #0d1522;
}

.range-title {
    color: #94a3b8;

    font-size: 12px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.range-value {
    color: #f8fafc;

    font-size: 24px;
    font-weight: 800;

    margin-top: 14px;
}

.range-note {
    color: #64748b;

    font-size: 11px;
    line-height: 1.5;

    margin-top: 10px;
}


/* ------------------------------------------------------------
   BADGES
------------------------------------------------------------ */

.badge {
    display: inline-block;

    padding: 6px 10px;

    border-radius: 999px;

    font-size: 11px;
    font-weight: 750;

    border: 1px solid transparent;
}

.badge-blue {
    color: #bfdbfe;

    background: rgba(59, 130, 246, 0.12);

    border-color: rgba(96, 165, 250, 0.25);
}

.badge-green {
    color: #a7f3d0;

    background: rgba(16, 185, 129, 0.12);

    border-color: rgba(52, 211, 153, 0.25);
}

.badge-yellow {
    color: #fde68a;

    background: rgba(245, 158, 11, 0.12);

    border-color: rgba(251, 191, 36, 0.25);
}

.badge-orange {
    color: #fed7aa;

    background: rgba(249, 115, 22, 0.12);

    border-color: rgba(251, 146, 60, 0.25);
}


/* ------------------------------------------------------------
   PROFILE
------------------------------------------------------------ */

.profile-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 12px;

    margin-top: 16px;
}

.profile-item {
    padding: 17px;

    border: 1px solid #24334b;
    border-radius: 14px;

    background: #0d1522;
}

.profile-label {
    color: #64748b;

    font-size: 10px;
    font-weight: 750;

    letter-spacing: 0.08em;
    text-transform: uppercase;

    margin-bottom: 7px;
}

.profile-value {
    color: #e2e8f0;

    font-size: 15px;
    font-weight: 650;
}


/* ------------------------------------------------------------
   PERFORMANCE
------------------------------------------------------------ */

.performance-grid {
    display: grid;

    grid-template-columns:
        repeat(5, minmax(0, 1fr));

    gap: 12px;

    margin-top: 16px;
}

.performance-card {
    padding: 18px;

    border: 1px solid #24334b;
    border-radius: 14px;

    background: #0d1522;
}

.performance-value {
    color: #f8fafc;

    font-size: 22px;
    font-weight: 800;
}

.performance-label {
    color: #64748b;

    font-size: 10px;
    font-weight: 700;

    margin-top: 7px;

    text-transform: uppercase;
    letter-spacing: 0.06em;
}


/* ------------------------------------------------------------
   INFO PANELS
------------------------------------------------------------ */

.info-grid {
    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 16px;

    margin-top: 18px;
}

.info-card {
    padding: 23px;

    border: 1px solid #24334b;
    border-radius: 16px;

    background: #0d1522;
}

.info-card-title {
    color: #f8fafc;

    font-size: 15px;
    font-weight: 750;

    margin-bottom: 12px;
}

.info-card-text {
    color: #94a3b8;

    font-size: 13px;
    line-height: 1.75;
}


/* ------------------------------------------------------------
   TABLE
------------------------------------------------------------ */

.history-table {
    width: 100%;

    border-collapse: collapse;

    margin-top: 15px;
}

.history-table th {
    text-align: left;

    padding: 11px 13px;

    color: #64748b;

    font-size: 10px;
    font-weight: 750;

    text-transform: uppercase;
    letter-spacing: 0.07em;

    border-bottom: 1px solid #24334b;
}

.history-table td {
    padding: 13px;

    color: #cbd5e1;

    font-size: 12px;

    border-bottom: 1px solid rgba(36, 51, 75, 0.65);
}


/* ------------------------------------------------------------
   FOOTER
------------------------------------------------------------ */

.footer {
    margin-top: 45px;
    padding-top: 22px;

    border-top: 1px solid #1e293b;

    color: #475569;

    font-size: 11px;

    text-align: center;
}


/* ------------------------------------------------------------
   RESPONSIVE
------------------------------------------------------------ */

@media (max-width: 1000px) {

    .stat-grid,
    .profile-grid,
    .performance-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .valuation-grid,
    .info-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 31px;
    }
}

@media (max-width: 650px) {

    .stat-grid,
    .profile-grid,
    .performance-grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 28px;
    }

    .hero-title {
        font-size: 28px;
    }

    .valuation-price {
        font-size: 39px;
    }
}

</style>
"""
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def get_bundle():
    return load_model_bundle()


try:
    bundle = get_bundle()
except Exception as e:
    st.error("Unable to load the IPL auction model.")
    st.exception(e)
    st.stop()


# ============================================================
# HELPERS
# ============================================================

def safe_text(value, default="Unknown"):
    if value is None:
        return default

    try:
        if value != value:
            return default
    except Exception:
        pass

    text = str(value).strip()

    if not text:
        return default

    return html.escape(text)


def safe_number(value, default=0):
    try:
        if value is None:
            return default

        result = float(value)

        if result != result:
            return default

        return result

    except Exception:
        return default


def crore(value):
    return f"₹{safe_number(value):,.2f} Cr"


def lakh(value):
    return f"₹{safe_number(value):,.2f} L"


def integer(value):
    return f"{safe_number(value):,.0f}"


def get_player_names():
    lookup = bundle.get("player_lookup")

    if lookup is None:
        return []

    if "player_name" not in lookup.columns:
        return []

    names = (
        lookup["player_name"]
        .dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return names


def valuation_badge_class(segment):
    segment = str(segment).lower()

    if "premium" in segment or "elite" in segment:
        return "badge-yellow"

    if "high" in segment:
        return "badge-orange"

    if "upper" in segment:
        return "badge-blue"

    return "badge-green"

def get_model_feature_importance():
    """
    Global feature importance from the champion
    Experience-Enhanced Random Forest model.

    These values come from the trained model evaluation
    performed in the notebook.
    """

    return [
        ("Recent 3-season runs", 20.15),
        ("Last-season wickets", 9.26),
        ("Career batting strike rate", 5.99),
        ("Last-season runs", 5.77),
        ("Previous auction price", 5.21),
        ("Last-season balls bowled", 4.00),
        ("Last-season balls faced", 3.98),
        ("Last-season strike rate", 3.73),
        ("Experience", 3.20),
        ("Career sixes", 2.86),
    ]

def get_auction_history(player_id):
    """
    Return historical auction records for a player.
    Uses only the auction data already stored in the model bundle.
    """

    auction_features = bundle.get("auction_features")

    if auction_features is None:
        return None

    if "player_id" not in auction_features.columns:
        return None

    history = auction_features[
        auction_features["player_id"].astype(str) == str(player_id)
    ].copy()

    if history.empty:
        return None

    columns = [
        col
        for col in [
            "year",
            "team",
            "base_price_lakh",
            "final_price_lakh",
            "role",
            "nationality",
        ]
        if col in history.columns
    ]

    history = history[columns].copy()

    if "year" in history.columns:
        history["year"] = history["year"].astype(int)

    if "final_price_lakh" in history.columns:
        history["final_price_lakh"] = pd.to_numeric(
            history["final_price_lakh"],
            errors="coerce"
        )

    if "base_price_lakh" in history.columns:
        history["base_price_lakh"] = pd.to_numeric(
            history["base_price_lakh"],
            errors="coerce"
        )

    history = history.sort_values("year")

    return history



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
<div style="
    padding: 8px 0 22px 0;
    border-bottom: 1px solid #24334b;
    margin-bottom: 22px;
">

    <div style="
        color:#60a5fa;
        font-size:10px;
        font-weight:800;
        letter-spacing:.16em;
        text-transform:uppercase;
        margin-bottom:8px;
    ">
        IPL ANALYTICS
    </div>

    <div style="
        color:#f8fafc;
        font-size:23px;
        line-height:1.15;
        font-weight:850;
        letter-spacing:-.04em;
    ">
        Auction<br>
        Intelligence
    </div>

</div>
"""
    )

    st.html(
        """
<div style="
    color:#f8fafc;
    font-size:14px;
    font-weight:750;
    margin-bottom:13px;
">
    Player Inputs
</div>
"""
    )

    player_names = get_player_names()

    if not player_names:
        st.error("No player names found in the model bundle.")
        st.stop()

    selected_player = st.selectbox(
        "Player Name",
        player_names,
        index=player_names.index("AB de Villiers")
        if "AB de Villiers" in player_names
        else 0,
    )

    selected_year = st.number_input(
        "Auction Year",
        min_value=2008,
        max_value=2026,
        value=2012,
        step=1,
    )

    selected_role = st.selectbox(
        "Role",
        [
            "Batsman",
            "Bowler",
            "All-Rounder",
            "Wicket-Keeper",
            "Unknown",
        ],
        index=0,
    )

    selected_nationality = st.selectbox(
        "Nationality",
        [
            "Indian",
            "Overseas",
            "Unknown",
        ],
        index=1,
    )

    st.write("")

    generate = st.button(
        "Generate Valuation",
        use_container_width=True,
        type="primary",
    )

    st.write("")

    st.html(
        """
<div style="
    padding:14px;
    border:1px solid #24334b;
    border-radius:12px;
    background:#0d1522;
">

    <div style="
        color:#64748b;
        font-size:10px;
        font-weight:750;
        letter-spacing:.08em;
        text-transform:uppercase;
        margin-bottom:7px;
    ">
        Model
    </div>

    <div style="
        color:#e2e8f0;
        font-size:13px;
        font-weight:650;
    ">
        Experience-Enhanced<br>
        Random Forest
    </div>

    <div style="
        color:#64748b;
        font-size:10px;
        margin-top:7px;
    ">
        Temporal validation
    </div>

</div>
"""
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
<div class="hero">

    <div class="hero-eyebrow">
        IPL PLAYER VALUATION SYSTEM
    </div>

    <div class="hero-title">
        Auction Intelligence Dashboard
    </div>

    <div class="hero-subtitle">
        Estimate a player's potential IPL auction value using
        historical performance, recent form, auction history,
        player context and experience available before the
        selected auction year.
    </div>

</div>
"""
)


# ============================================================
# MODEL AT A GLANCE
# ============================================================

st.html(
    """
<div class="section-title">
    Model at a glance
</div>

<div class="section-subtitle">
    The final model was evaluated using a temporal holdout,
    training on earlier auctions and testing on later auctions.
</div>

<div class="stat-grid">

    <div class="stat-card">
        <div class="stat-label">
            MAE
        </div>

        <div class="stat-value">
            ₹210.26L
        </div>

        <div class="stat-description">
            Mean absolute error
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">
            RMSE
        </div>

        <div class="stat-value">
            ₹373.87L
        </div>

        <div class="stat-description">
            Penalizes larger errors
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">
            R²
        </div>

        <div class="stat-value">
            0.249
        </div>

        <div class="stat-description">
            Variance explained
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">
            Training
        </div>

        <div class="stat-value">
            2008–2022
        </div>

        <div class="stat-description">
            Temporal training period
        </div>
    </div>

</div>
"""
)


# ============================================================
# DEFAULT / GENERATED STATE
# ============================================================

if "valuation_report" not in st.session_state:
    st.session_state["valuation_report"] = None


if generate:

    try:

        with st.spinner("Analyzing player history and generating valuation..."):

            report = generate_valuation_report(
                player_name=selected_player,
                auction_year=int(selected_year),
                role=selected_role,
                nationality=selected_nationality,
            )

        st.session_state["valuation_report"] = report

    except Exception as e:

        st.session_state["valuation_report"] = None

        st.error("Valuation generation failed.")
        st.exception(e)


# ============================================================
# GET CURRENT REPORT
# ============================================================

report = st.session_state.get("valuation_report")


# ============================================================
# LANDING STATE
# ============================================================

if report is None:

    st.html(
        """
<div style="
    margin-top:25px;
    padding:30px;

    border:1px dashed #30425d;
    border-radius:17px;

    background:#0b121e;

    text-align:center;
">

    <div style="
        font-size:30px;
        margin-bottom:12px;
    ">
        🏏
    </div>

    <div style="
        color:#f8fafc;
        font-size:17px;
        font-weight:750;
        margin-bottom:8px;
    ">
        Ready to value a player
    </div>

    <div style="
        color:#64748b;
        font-size:13px;
    ">
        Select a player profile from the sidebar and generate
        a pre-auction valuation.
    </div>

</div>
"""
    )


# ============================================================
# REPORT
# ============================================================

if report is not None:

    player = safe_text(report.get("Player"))
    player_id = safe_text(report.get("Player ID"))

    auction_year = safe_text(report.get("Auction Year"))
    role = safe_text(report.get("Role"))
    nationality = safe_text(report.get("Nationality"))

    debut_year = safe_text(report.get("Debut Year"))
    experience = safe_text(report.get("Experience (Years)"))

    previous_auctions = integer(
        report.get("Previous Auctions", 0)
    )

    previous_price = lakh(
        report.get("Previous Auction Price (₹L)", 0)
    )

    predicted_lakh = safe_number(
        report.get("Predicted Value (₹L)", 0)
    )

    predicted_crore = safe_number(
        report.get("Predicted Value (₹Cr)", 0)
    )

    typical_range = safe_text(
        report.get("Typical Range (₹Cr)", "Not available")
    )

    wider_range = safe_text(
        report.get("Wider Range (₹Cr)", "Not available")
    )

    typical_low = safe_number(
        report.get("Typical Low (₹Cr)", 0)
    )

    typical_high = safe_number(
        report.get("Typical High (₹Cr)", 0)
    )

    wider_low = safe_number(
        report.get("Wider Low (₹Cr)", 0)
    )

    wider_high = safe_number(
        report.get("Wider High (₹Cr)", 0)
    )

    segment = safe_text(
        report.get("Valuation Segment", "Unknown")
    )

    segment_class = valuation_badge_class(
        report.get("Valuation Segment", "")
    )


    # ========================================================
    # PLAYER HEADER
    # ========================================================

    st.html(
        f"""
<div style="
    margin-top:32px;
    margin-bottom:18px;
">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:flex-end;
        gap:20px;
        flex-wrap:wrap;
    ">

        <div>

            <div style="
                color:#60a5fa;
                font-size:10px;
                font-weight:800;
                letter-spacing:.13em;
                text-transform:uppercase;
                margin-bottom:7px;
            ">
                PLAYER VALUATION
            </div>

            <div style="
                color:#f8fafc;
                font-size:31px;
                font-weight:850;
                letter-spacing:-.04em;
            ">
                {player}
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                margin-top:6px;
            ">
                Player ID: {player_id}
                &nbsp; • &nbsp;
                Auction Year: {auction_year}
            </div>

        </div>

        <div>
            <span class="badge {segment_class}">
                {segment}
            </span>
        </div>

    </div>

</div>
"""
    )


    # ========================================================
    # VALUATION
    # ========================================================

    st.html(
        f"""
<div class="valuation-grid">

    <div class="valuation-main">

        <div class="valuation-label">
            Predicted Auction Value
        </div>

        <div class="valuation-price">
            ₹{predicted_crore:,.2f} Cr
        </div>

        <div class="valuation-lakh">
            Equivalent to ₹{predicted_lakh:,.2f} lakh
        </div>

        <div style="
            margin-top:20px;
        ">
            <span class="badge {segment_class}">
                {segment}
            </span>
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Typical valuation range
        </div>

        <div class="range-value">
            ₹{typical_low:,.2f} – ₹{typical_high:,.2f} Cr
        </div>

        <div class="range-note">
            Based on the model's empirical historical
            prediction error distribution.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Wider valuation range
        </div>

        <div class="range-value">
            ₹{wider_low:,.2f} – ₹{wider_high:,.2f} Cr
        </div>

        <div class="range-note">
            A wider benchmark using the 75th percentile
            historical absolute error.
        </div>

    </div>

</div>
"""
    )


    # ========================================================
    # PLAYER PROFILE
    # ========================================================

    st.html(
        f"""
<div class="section-title">
    Player Profile
</div>

<div class="section-subtitle">
    Context available before the selected auction.
</div>

<div class="profile-grid">

    <div class="profile-item">
        <div class="profile-label">
            Role
        </div>

        <div class="profile-value">
            {role}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Nationality
        </div>

        <div class="profile-value">
            {nationality}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Debut Year
        </div>

        <div class="profile-value">
            {debut_year}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Experience
        </div>

        <div class="profile-value">
            {experience} years
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Previous Auctions
        </div>

        <div class="profile-value">
            {previous_auctions}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Previous Auction Price
        </div>

        <div class="profile-value">
            {previous_price}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Auction Year
        </div>

        <div class="profile-value">
            {auction_year}
        </div>
    </div>

    <div class="profile-item">
        <div class="profile-label">
            Model Segment
        </div>

        <div class="profile-value">
            {segment}
        </div>
    </div>

</div>
"""
    )

    # ========================================================
    # HISTORICAL AUCTION INTELLIGENCE
    # ========================================================

    auction_history = get_auction_history(
        report.get("Player ID")
    )

    st.html(
        """
<div class="section-title">
    Historical Auction Intelligence
</div>

<div class="section-subtitle">
    Previous auction outcomes provide additional context for the
    player's valuation.
</div>
"""
    )

    if auction_history is not None and not auction_history.empty:

        history_rows = ""

        for _, auction_row in auction_history.iterrows():

            year_value = auction_row.get("year", "")

            team_value = auction_row.get(
                "team",
                "Unknown"
            )

            actual_price = safe_number(
                auction_row.get(
                    "final_price_lakh",
                    0
                )
            )

            base_price = safe_number(
                auction_row.get(
                    "base_price_lakh",
                    0
                )
            )

            if actual_price > 0:

                actual_display = (
                    f"₹{actual_price / 100:,.2f} Cr"
                )

            else:

                actual_display = "Not available"

            if base_price > 0:

                base_display = (
                    f"₹{base_price:,.0f} L"
                )

            else:

                base_display = "—"

            history_rows += f"""
<tr>

    <td>
        {safe_text(year_value)}
    </td>

    <td>
        {safe_text(team_value)}
    </td>

    <td>
        {base_display}
    </td>

    <td>
        <strong style="color:#f8fafc;">
            {actual_display}
        </strong>
    </td>

</tr>
"""

        st.html(
            f"""
<div class="info-card">

    <div class="info-card-title">
        Auction History
    </div>

    <table class="history-table">

        <thead>

            <tr>

                <th>
                    Year
                </th>

                <th>
                    Team
                </th>

                <th>
                    Base Price
                </th>

                <th>
                    Actual Auction Price
                </th>

            </tr>

        </thead>

        <tbody>

            {history_rows}

        </tbody>

    </table>

</div>
"""
        )

    else:

        st.html(
            """
<div class="info-card">

    <div class="info-card-title">
        Auction History
    </div>

    <div class="info-card-text">
        No historical auction records were found for this
        player in the available auction dataset.
    </div>

</div>
"""
        )

    # ========================================================
    # MODEL VS ACTUAL
    # ========================================================

    actual_price_lakh = None

    if auction_history is not None and not auction_history.empty:

        matching_auction = auction_history[
            auction_history["year"] == int(
                report.get("Auction Year")
            )
        ].copy()

        if not matching_auction.empty:

            value = matching_auction.iloc[0].get(
                "final_price_lakh"
            )

            if pd.notna(value):

                actual_price_lakh = float(value)


    if actual_price_lakh is not None:

        actual_price_crore = (
            actual_price_lakh / 100
        )

        model_price_lakh = safe_number(
            report.get(
                "Predicted Value (₹L)",
                0
            )
        )

        model_price_crore = (
            model_price_lakh / 100
        )

        difference_lakh = (
            model_price_lakh
            - actual_price_lakh
        )

        difference_crore = (
            difference_lakh / 100
        )

        absolute_error_lakh = abs(
            difference_lakh
        )

        if actual_price_lakh > 0:

            percentage_error = (
                absolute_error_lakh
                / actual_price_lakh
            ) * 100

        else:

            percentage_error = 0


        if difference_lakh > 0:

            comparison_text = "Model overestimated the auction price"

            comparison_color = "#fbbf24"

        elif difference_lakh < 0:

            comparison_text = "Model underestimated the auction price"

            comparison_color = "#60a5fa"

        else:

            comparison_text = "Model matched the auction price"

            comparison_color = "#34d399"


        st.html(
            f"""
<div class="section-title">
    Model vs Actual Auction Price
</div>

<div class="section-subtitle">
    Comparison between the model's valuation and the recorded
    auction outcome for the selected player and year.
</div>

<div class="valuation-grid">

    <div class="range-card">

        <div class="range-title">
            Model Valuation
        </div>

        <div class="range-value">
            ₹{model_price_crore:,.2f} Cr
        </div>

        <div class="range-note">
            Estimated before the selected auction year.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Actual Auction Price
        </div>

        <div class="range-value">
            ₹{actual_price_crore:,.2f} Cr
        </div>

        <div class="range-note">
            Recorded historical auction outcome.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Prediction Difference
        </div>

        <div class="range-value"
             style="color:{comparison_color};">

            {"+" if difference_crore > 0 else ""}
            ₹{difference_crore:,.2f} Cr

        </div>

        <div class="range-note">

            Absolute error:
            ₹{absolute_error_lakh:,.2f} L

            <br>

            Percentage error:
            {percentage_error:.1f}%

        </div>

    </div>

</div>

<div style="
    margin-top:14px;
    padding:15px 18px;

    border:1px solid #24334b;
    border-radius:13px;

    background:#0d1522;

    color:#94a3b8;

    font-size:12px;
">

    <strong style="color:{comparison_color};">
        {comparison_text}.
    </strong>

    The difference between predicted and actual auction
    price reflects the uncertainty inherent in auction
    outcomes.

</div>
"""
        )

    else:

        st.html(
            """
<div class="section-title">
    Model vs Actual Auction Price
</div>

<div class="info-card">

    <div class="info-card-title">
        Historical comparison unavailable
    </div>

    <div class="info-card-text">
        There is no recorded auction outcome for this player
        in the selected auction year. The dashboard therefore
        shows the model valuation without inventing an actual
        price.
    </div>

</div>
"""
        )
    # ========================================================
    # PERFORMANCE
    # ========================================================

    career_runs = integer(
        report.get("Career Runs Before Auction", 0)
    )

    recent_runs = integer(
        report.get("Recent 3 Seasons Runs", 0)
    )

    last_runs = integer(
        report.get("Last Season Runs", 0)
    )

    career_wickets = integer(
        report.get("Career Wickets Before Auction", 0)
    )

    recent_wickets = integer(
        report.get("Recent 3 Seasons Wickets", 0)
    )

    career_sr = safe_number(
        report.get("Career Batting SR Before Auction", 0)
    )

    last_sr = safe_number(
        report.get("Last Season SR", 0)
    )

    recent_sr = safe_number(
        report.get("Recent 3 Seasons SR", 0)
    )

    last_wickets = integer(
        report.get("Last Season Wickets", 0)
    )

    last_economy = safe_number(
        report.get("Last Season Economy", 0)
    )


    st.html(
        f"""
<div class="section-title">
    Pre-Auction Performance
</div>

<div class="section-subtitle">
    Historical performance available before {auction_year}.
</div>

<div class="performance-grid">

    <div class="performance-card">
        <div class="performance-value">
            {career_runs}
        </div>

        <div class="performance-label">
            Career Runs
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {recent_runs}
        </div>

        <div class="performance-label">
            Recent 3 Seasons Runs
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {last_runs}
        </div>

        <div class="performance-label">
            Last Season Runs
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {career_wickets}
        </div>

        <div class="performance-label">
            Career Wickets
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {recent_wickets}
        </div>

        <div class="performance-label">
            Recent 3 Seasons Wickets
        </div>
    </div>

</div>
"""
    )


    # ========================================================
    # SECOND PERFORMANCE ROW
    # ========================================================

    st.html(
        f"""
<div class="performance-grid" style="margin-top:12px;">

    <div class="performance-card">
        <div class="performance-value">
            {career_sr:.1f}
        </div>

        <div class="performance-label">
            Career Batting SR
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {last_sr:.1f}
        </div>

        <div class="performance-label">
            Last Season SR
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {recent_sr:.1f}
        </div>

        <div class="performance-label">
            Recent 3 Seasons SR
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {last_wickets}
        </div>

        <div class="performance-label">
            Last Season Wickets
        </div>
    </div>

    <div class="performance-card">
        <div class="performance-value">
            {last_economy:.2f}
        </div>

        <div class="performance-label">
            Last Season Economy
        </div>
    </div>

</div>
"""
    )

    # ========================================================
    # MODEL EXPLAINABILITY
    # ========================================================

    importance_data = get_model_feature_importance()

    st.html(
        """
<div class="section-title">
    What Drives the Valuation?
</div>

<div class="section-subtitle">
    The champion Random Forest model relies on several historical
    performance, auction and player-context signals when estimating
    auction value.
</div>
"""
    )

    importance_rows = ""

    for feature_name, importance in importance_data:

        bar_width = min(
            float(importance) / 20.15 * 100,
            100
        )

        importance_rows += f"""
<div style="
    margin-bottom:18px;
">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:7px;
    ">

        <span style="
            color:#dbeafe;
            font-size:13px;
            font-weight:600;
        ">
            {feature_name}
        </span>

        <span style="
            color:#60a5fa;
            font-size:13px;
            font-weight:700;
        ">
            {importance:.2f}%
        </span>

    </div>

    <div style="
        width:100%;
        height:8px;
        background:#172235;
        border-radius:999px;
        overflow:hidden;
    ">

        <div style="
            width:{bar_width:.1f}%;
            height:100%;
            background:linear-gradient(
                90deg,
                #2563eb,
                #60a5fa
            );
            border-radius:999px;
        ">
        </div>

    </div>

</div>
"""

    st.html(
        f"""
<div class="info-card">

    <div class="info-card-title">
        Global Model Feature Importance
    </div>

    <div style="
        margin-top:10px;
        margin-bottom:22px;
        color:#64748b;
        font-size:12px;
        line-height:1.6;
    ">
        Percentage contribution of the model's input features
        to its overall prediction process. Higher importance
        indicates that the Random Forest relied more heavily on
        that feature across the evaluation data.
    </div>

    {importance_rows}

</div>
"""
    )

    # ========================================================
    # PLAYER-SPECIFIC INTERPRETATION
    # ========================================================

    recent_runs = safe_number(
        report.get(
            "Recent 3 Seasons Runs",
            0
        )
    )

    last_runs = safe_number(
        report.get(
            "Last Season Runs",
            0
        )
    )

    career_sr = safe_number(
        report.get(
            "Career Batting SR Before Auction",
            0
        )
    )

    previous_price = safe_number(
        report.get(
            "Previous Auction Price (₹L)",
            0
        )
    )

    experience = safe_number(
        report.get(
            "Experience (Years)",
            0
        )
    )

    st.html(
        f"""
<div class="section-title">
    Player-Specific Context
</div>

<div class="section-subtitle">
    How the selected player's pre-auction profile compares
    with the signals that matter most to the model.
</div>

<div class="valuation-grid">

    <div class="range-card">

        <div class="range-title">
            Recent Form
        </div>

        <div class="range-value">
            {recent_runs:,.0f}
        </div>

        <div class="range-note">
            Runs across the previous three seasons.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Last Season
        </div>

        <div class="range-value">
            {last_runs:,.0f}
        </div>

        <div class="range-note">
            Runs in the most recent season available
            before the auction.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Batting Strike Rate
        </div>

        <div class="range-value">
            {career_sr:,.1f}
        </div>

        <div class="range-note">
            Career strike rate available before the auction.
        </div>

    </div>


    <div class="range-card">

        <div class="range-title">
            Previous Auction Price
        </div>

        <div class="range-value">
            ₹{previous_price:,.0f}L
        </div>

        <div class="range-note">
            Historical auction value used as model context.
        </div>

    </div>

</div>
"""
    )

    # ========================================================
    # INTERPRETATION
    # ========================================================

    st.html(
        f"""
<div class="info-card"
     style="
        margin-top:20px;
        border-color:#23436d;
     ">

    <div class="info-card-title">
        How to Read This
    </div>

    <div style="
        color:#94a3b8;
        font-size:13px;
        line-height:1.8;
    ">

        <p>
            <strong style="color:#f8fafc;">
                Recent performance
            </strong>
            is the strongest individual signal in the model.
            The selected player recorded
            <strong style="color:#60a5fa;">
                {recent_runs:,.0f} runs
            </strong>
            across the previous three seasons.
        </p>

        <p>
            The model also places substantial importance on
            recent bowling performance, batting efficiency,
            previous auction value and other historical
            player-performance indicators.
        </p>

        <p>
            For this player, the model combines these
            pre-auction signals with player context and
            experience to produce the estimated valuation of
            <strong style="color:#60a5fa;">
                ₹{safe_number(report.get("Predicted Value (₹Cr)", 0)):,.2f} Cr
            </strong>.
        </p>

        <p style="
            margin-bottom:0;
            color:#64748b;
        ">
            Note: feature importance describes how the model
            behaves overall. It should not be interpreted as
            proof that any single feature directly caused the
            player's auction price.
        </p>

    </div>

</div>
"""
    )

    # ========================================================
    # INTERPRETATION
    # ========================================================

    st.html(
        f"""
<div class="section-title">
    Valuation Interpretation
</div>

<div class="section-subtitle">
    How the model output should be interpreted.
</div>

<div class="info-grid">

    <div class="info-card">

        <div class="info-card-title">
            What the valuation means
        </div>

        <div class="info-card-text">
            The model estimates a benchmark auction value of
            <strong style="color:#f8fafc;">
                ₹{predicted_crore:,.2f} Cr
            </strong>
            based on information that would have been available
            before the selected auction year.
            <br><br>
            The estimate is intended for valuation and
            decision-support rather than as an exact prediction
            of the final winning bid.
        </div>

    </div>


    <div class="info-card">

        <div class="info-card-title">
            Uncertainty
        </div>

        <div class="info-card-text">
            The typical historical range is
            <strong style="color:#f8fafc;">
                ₹{typical_low:,.2f} – ₹{typical_high:,.2f} Cr
            </strong>.
            <br><br>
            A wider empirical range is
            <strong style="color:#f8fafc;">
                ₹{wider_low:,.2f} – ₹{wider_high:,.2f} Cr
            </strong>.
            These are empirical valuation ranges, not statistical
            confidence intervals.
        </div>

    </div>

</div>
"""
    )


    # ========================================================
    # METHODOLOGY
    # ========================================================

    st.html(
        """
<div class="section-title">
    Model Methodology
</div>

<div class="section-subtitle">
    The valuation system is designed to prevent future-information leakage.
</div>

<div class="info-grid">

    <div class="info-card">

        <div class="info-card-title">
            Champion Model
        </div>

        <div class="info-card-text">

            <strong style="color:#f8fafc;">
                Experience-Enhanced Random Forest
            </strong>

            <br><br>

            The model combines historical player performance,
            recent form, auction history, player context and
            experience.

            <br><br>

            <strong style="color:#60a5fa;">
                MAE:
            </strong>
            ₹210.26L

            <br>

            <strong style="color:#60a5fa;">
                RMSE:
            </strong>
            ₹373.87L

            <br>

            <strong style="color:#60a5fa;">
                R²:
            </strong>
            0.249

        </div>

    </div>


    <div class="info-card">

        <div class="info-card-title">
            Temporal Validation
        </div>

        <div class="info-card-text">

            Training data covers auction years
            <strong style="color:#f8fafc;">
                2008–2022
            </strong>.

            <br><br>

            Later auction years are kept as a temporal
            holdout to evaluate how the model performs
            on future auction periods.

            <br><br>

            Only player performance from seasons before
            the selected auction year is used for valuation.

        </div>

    </div>


    <div class="info-card">

        <div class="info-card-title">
            Important Features
        </div>

        <div class="info-card-text">

            The strongest individual features include:

            <br><br>

            • Recent 3-season runs

            <br>
            • Last-season wickets

            <br>
            • Career batting strike rate

            <br>
            • Last-season runs

            <br>
            • Previous auction price

            <br>
            • Recent batting strike rate

        </div>

    </div>


    <div class="info-card">

        <div class="info-card-title">
            Model Limitation
        </div>

        <div class="info-card-text">

            The model performs substantially better on normal
            auction valuations than on extreme high-value
            purchases.

            <br><br>

            Very large auction outcomes can be influenced by
            factors such as bidding competition, franchise
            requirements, scarcity, reputation and auction
            strategy that historical player statistics cannot
            fully capture.

        </div>

    </div>

</div>
"""
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.html(
        """
<div style="
    margin-top:25px;
    padding:17px 20px;

    border:1px solid #3b2f13;
    border-radius:13px;

    background:rgba(245,158,11,0.05);

    color:#a8a29e;

    font-size:11px;
    line-height:1.7;
">

    <strong style="color:#fbbf24;">
        Model note:
    </strong>

    Auction valuation is inherently uncertain.
    This dashboard should be used as a historical
    benchmarking and decision-support tool, not as a
    guarantee of the final auction price.

</div>
"""
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
<div class="footer">

    IPL Auction Intelligence
    &nbsp;•&nbsp;
    Experience-Enhanced Random Forest
    &nbsp;•&nbsp;
    Temporal ML Valuation System

</div>
"""
)
