@'
# IPL Player Auction Intelligence & Valuation System

An end-to-end machine learning project that estimates IPL player auction valuations using only information that would have been available before the auction.

The system combines historical IPL auction records with season-level batting and bowling performance to create a time-aware player valuation framework.

---

## Project Overview

IPL auction prices are influenced by many factors including recent performance, career statistics, experience, previous auction history, player role, nationality, and market conditions.

This project asks:

> **Based on everything known about a player before an auction, what could their potential auction valuation be?**

The system performs:

- Player identity resolution across multiple datasets
- Data cleaning and preprocessing
- Historical batting and bowling aggregation
- Pre-auction feature engineering
- Data leakage prevention
- Temporal model evaluation
- Machine learning model comparison
- Feature importance analysis
- Prediction error analysis
- Interactive player valuation

The final system can take a player's name, auction year, role, and nationality and generate an estimated auction value with an empirical valuation range.

---

## Objectives

1. Combine historical IPL auction and player-performance datasets.
2. Resolve inconsistent player names across different datasets.
3. Build season-level batting and bowling performance histories.
4. Generate features using only information available before each auction.
5. Train machine learning regression models for auction valuation.
6. Evaluate models using a future-year temporal holdout.
7. Identify the most influential feature groups.
8. Analyze prediction errors and model limitations.
9. Build an interpretable player valuation system.

---

## Dataset

The project combines four main categories of information.

### Player Data

Player-level information including:

- Player name
- Country
- Debut year
- Last active year
- Seasons played
- Career statistics

### Batting Data

Season-level batting statistics including:

- Innings
- Runs scored
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

Raw datasets are not committed to the repository. See [`data/README.md`](data/README.md) for details.

---

## Data Cleaning & Player Identity Resolution

A major challenge was that the same player could appear under different names across datasets.

Examples include:

```text
K L Rahul
KL Rahul

M Shahrukh Khan
Shahrukh Khan

D L Chahar
Deepak Chahar