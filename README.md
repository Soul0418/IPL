# 🏏 IPL Player Auction Intelligence & Valuation System

## 🚀 Live Demo

🔗 **[Try the IPL Auction Analysis Dashboard](https://iplauctionanalysis.streamlit.app/)**

> Explore IPL player auction valuations, historical auction intelligence, performance insights, and ML-powered price predictions.

An end-to-end **Machine Learning project** that analyzes IPL player performance and historical auction data to estimate a player's potential auction value.

The project transforms historical IPL auction records, batting performance, bowling performance, player experience, and previous auction prices into a structured player valuation framework.

It also provides analytical insights into **overvalued, undervalued, and fairly valued players** and includes an interactive Streamlit dashboard for exploring predictions and player-level insights.

---

## 🎯 Project Objective

The main objective is to build a data-driven system that can answer:

* What auction price could a player reasonably command?
* How much does recent form influence auction value?
* How important is previous auction price?
* Which players appear undervalued or overvalued compared with their predicted value?
* How does player role affect valuation?
* How well does the model generalize to future IPL auctions?

The model is designed as a **decision-support and valuation tool**, rather than a system that attempts to perfectly predict auction outcomes.

---

## 📊 Data Used

The project combines multiple IPL datasets containing:

* Historical IPL auction prices
* Player information
* Season-level batting statistics
* Season-level bowling statistics
* Previous auction history
* Player roles and nationality
* Career performance
* Recent performance
* Experience-related features

Player names were normalized and mapped across datasets to create a consistent player-level representation.

---

## 🧹 Data Preparation

The raw IPL datasets contained inconsistent player names, duplicate records, missing values, and different naming conventions across sources.

The data preparation process included:

1. Cleaning raw datasets
2. Standardizing player names
3. Creating player aliases
4. Mapping players across auction, batting, and bowling datasets
5. Removing duplicate player-season records
6. Creating chronological performance features
7. Handling missing performance history
8. Building auction-level modeling datasets

The final auction dataset contains approximately **1,400+ auction records**.

---

## ⚙️ Feature Engineering

The model uses historical information that could reasonably be available before an auction.

### Batting Features

* Career runs
* Career batting strike rate
* Career innings
* Career hundreds
* Career fifties
* Career fours
* Career sixes
* Last-season runs
* Last-season strike rate
* Recent 3-season runs
* Recent 3-season strike rate
* Recent hundreds and fifties

### Bowling Features

* Career wickets
* Career economy
* Career bowling innings
* Career balls bowled
* Career runs conceded
* Career 3-wicket, 4-wicket and 5-wicket hauls
* Last-season wickets
* Last-season economy
* Recent 3-season wickets
* Recent 3-season economy

### Auction & Player Features

* Previous auction price
* Number of previous auctions
* Player role
* Nationality
* Career seasons
* Batting seasons
* Bowling seasons
* Experience years
* Availability of batting/bowling history

---

## 🤖 Machine Learning Model

The project evaluates player characteristics and historical performance to estimate auction value.

The final model uses a machine-learning pipeline containing preprocessing and the trained valuation model.

The prediction target is:

**Player Final Auction Price**

The model follows a chronological evaluation approach so that future auction periods can be evaluated separately from earlier historical data.

---

## 📈 Model Performance

### Future Auction Evaluation — 2023–2026

| Metric |   Result |
| ------ | -------: |
| MAE    | ₹1.74 Cr |
| RMSE   | ₹3.10 Cr |
| R²     |    0.485 |

The model achieves an R² of approximately **0.49** on the future evaluation period.

This indicates that the model captures meaningful relationships between player performance, experience, previous auction history, and auction value, while still leaving substantial variation unexplained.

### Why are some predictions difficult?

IPL auctions are influenced by factors that are difficult to capture using historical player statistics alone, including:

* Team requirements
* Bidding competition
* Player scarcity
* Overseas-player slots
* Reputation and popularity
* Injuries and availability
* Recent performances
* Strategic team decisions
* Auction-day dynamics

Therefore, the model should be interpreted as a **data-driven valuation estimate**, not a guaranteed auction-price predictor.

---

## 💰 Auction Value Analysis

The project compares predicted auction value with actual auction price.

### Value Gap

**Value Gap = Predicted Price − Actual Price**

Players are categorized as:

* **Undervalued** — model predicts substantially higher value than the actual price
* **Overvalued** — actual price is substantially higher than the model prediction
* **Fair Value** — prediction and actual price are relatively close

The project generates analysis for:

* Top undervalued players
* Top overvalued players
* Best-value players
* Team-wise value gaps
* Role-wise value gaps
* Price-band model errors
* Year-wise model performance
* Largest prediction errors

---

## 📊 Interactive Dashboard

The project includes an interactive **Streamlit dashboard** for exploring:

* Player auction predictions
* Historical auction values
* Player performance
* Model insights
* Overvalued players
* Undervalued players
* Team-level analysis
* Role-level analysis

### Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```text
IPL/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── *.csv
│   └── raw/                 # ignored by Git
│
├── notebooks/
│   ├── data_inspection.ipynb
│   └── Model_Interpretation.ipynb
│
├── outputs/
│   └── figures/
│
├── src/
│   ├── auction_value_analysis.py
│   ├── chronological_evaluation.py
│   ├── evaluate_model.py
│   ├── model_diagnostics.py
│   ├── model_loader.py
│   ├── predict.py
│   └── valuation.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── README_BUILD.md
```

---

## 🚀 Installation & Usage

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd IPL
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🔍 Example Prediction

The model can be used to estimate an auction value for a player based on their historical performance and available pre-auction information.

Example:

```text
Player: Virat Kohli
Auction Year: 2026

Estimated Auction Value:
₹6.39 Crore
```

This value represents the model's estimate and should not be interpreted as the player's guaranteed auction price.

---

## 📌 Key Insights

The analysis demonstrates that:

* Recent player performance is an important factor in valuation.
* Previous auction price provides useful information for predicting future auction value.
* Batting and bowling performance contribute differently depending on player role.
* High-value auction purchases are significantly harder to predict accurately.
* Extreme auction prices are often influenced by factors outside player statistics.
* The model is more useful for identifying valuation patterns and potential market inefficiencies than for predicting exact auction outcomes.

---

## ⚠️ Limitations

The model does not fully capture:

* Team-specific requirements
* Auction bidding wars
* Player popularity
* Media hype
* Injuries and availability
* Strategic team decisions
* Real-time auction dynamics
* Changes in team composition

Additionally, some recent auction records contain incomplete role or experience information, which can affect individual predictions.

---

## 🔮 Future Improvements

Potential improvements include:

* Incorporating team purse and squad composition
* Adding player availability and injury information
* Adding venue and performance-context features
* Including player popularity or social-media signals
* Incorporating team-specific historical buying patterns
* Testing advanced boosting models
* Adding prediction intervals instead of a single price estimate
* Building a real-time auction simulation
* Improving player-role classification for newer auction records

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Matplotlib**
* **Jupyter Notebook**
* **Streamlit**
* **Git & GitHub**

---

## 👨‍💻 Project Focus

This project demonstrates practical skills in:

**Data Cleaning → Data Integration → Feature Engineering → Machine Learning → Model Evaluation → Business Analysis → Data Visualization**

It is designed to showcase an end-to-end **Data Analytics + Machine Learning workflow** using a real-world sports analytics problem.
