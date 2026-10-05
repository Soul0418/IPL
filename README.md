# 🏏 IPL Player Auction Intelligence & Valuation System

An end-to-end machine learning project that estimates the potential auction value of IPL players using only information that would have been available before the auction.

The project combines historical IPL auction data with season-level batting and bowling performance to build a time-aware player valuation system.

---

## 📌 Project Overview

IPL auction prices are influenced by player performance, experience, previous auction history, role, nationality, and market demand.

The goal of this project was to answer:

> **"Based on everything known about a player before an auction, what could their potential auction valuation be?"**

The system performs:

- Player identity resolution across multiple datasets
- Data cleaning and preprocessing
- Historical performance aggregation
- Pre-auction feature engineering
- Temporal data splitting
- Machine learning model comparison
- Feature importance analysis
- Prediction error analysis
- Player valuation generation

The final system can take a player's:

- Name
- Auction year
- Role
- Nationality

and generate an estimated auction value along with an empirical valuation range.

---

## 🎯 Objectives

The project was designed to:

1. Combine IPL auction and player performance datasets.
2. Resolve inconsistent player names across datasets.
3. Create historical player performance features.
4. Ensure that only information available before an auction is used.
5. Train machine learning regression models.
6. Compare model performance using a future-year test set.
7. Identify the features most associated with auction valuation.
8. Analyze where the model performs well and where it struggles.
9. Build an interpretable player valuation system.

---

## 📊 Dataset

The project uses three major data sources:

### Player Data

Contains player-level information such as:

- Player name
- Country
- Debut year
- Last year
- Seasons played
- Career statistics

### Batting Data

Season-level batting statistics including:

- Innings
- Runs
- Balls faced
- Batting strike rate
- Hundreds
- Fifties
- Fours
- Sixes

### Bowling Data

Season-level bowling statistics including:

- Innings
- Balls bowled
- Runs conceded
- Wickets
- Economy rate
- Bowling strike rate
- Wicket hauls

### Auction Data

Auction-level information including:

- Auction year
- Player
- Role
- Nationality
- Base price
- Final auction price
- Team
- Auction status

---

## 🧹 Data Cleaning & Entity Resolution

One of the major challenges was inconsistent player naming across datasets.

The same player could appear with:

- Initials
- Abbreviated names
- Different spacing
- Different punctuation
- Alternative naming conventions

For example:

```text
K L Rahul
KL Rahul