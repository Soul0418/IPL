# Data

The raw IPL auction and player-performance datasets used in this project are not included in the repository.

The project uses historical:

- IPL auction records
- Player information
- Season-level batting statistics
- Season-level bowling statistics

Raw datasets are excluded from GitHub to keep the repository lightweight and avoid redistributing third-party data.

## Data Processing

The notebooks perform:

1. Player-name normalization
2. Player identity resolution
3. Auction record mapping
4. Batting and bowling aggregation
5. Pre-auction feature engineering
6. Leakage prevention using auction-year cutoffs
7. Model training and evaluation

The machine-learning dataset is constructed from information available before each player's auction year.
