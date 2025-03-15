# OptiVest Stock Basket Analysis

This directory contains the implementation and documentation of OptiVest's proprietary stock basket methodology, which uses the Fama-French + Beta factor model to categorize stocks into risk-based baskets.

## Overview

Our stock basket analysis divides the investment universe into five distinct baskets based on risk factors, creating a systematic approach to stock selection and portfolio construction. The methodology employs a modified Fama-French three-factor model with additional beta analysis to identify stocks with similar risk-return characteristics.

## Directory Structure

```
data_analysis/
├── data/                  # Data files
│   ├── processed/         # Processed data files
│   └── raw/               # Raw data files
├── results/               # Analysis results
│   ├── factor_loadings.csv      # Factor exposures for each stock
│   ├── factor_baskets.csv       # Summary of the 5 stock baskets
│   ├── basket_X_stocks.csv      # Stocks in each basket (X = 1-5)
│   ├── basket_X_adjusted_weights.csv  # Top 7 stocks with weights summing to 100%
│   ├── realistic_returns.csv    # Realistic return figures for each basket
│   └── basket_summary.md        # Markdown summary of the baskets
├── scripts/               # Python scripts
│   ├── data_processor.py         # Data processing script
│   ├── factor_model.py           # Fama-French + Beta model implementation
│   ├── portfolio_optimizer.py    # Portfolio optimization script
│   └── recalculate_basket_weights.py  # Script to calculate basket weights
├── visualizations/        # Visualization files
│   ├── basket_dashboard.py             # Enhanced visualization dashboard
│   ├── basket_risk_return_profile.png  # Risk-return profile visualization
│   ├── basket_factor_exposures.png     # Factor exposures dashboard
│   ├── basket_risk_return_matrix.png   # Risk-return rating matrix
│   ├── basket_characteristics_dashboard.png  # Basket metrics dashboard
│   ├── basket_stock_examples.png       # Representative stocks visualization
│   ├── executive_summary.md            # Executive summary document
│   ├── index.html                      # Interactive visualization dashboard
│   └── README.md                       # Visualization documentation
└── README.md              # This file
```

## The Five Stock Baskets

Our model creates five distinct stock baskets, each containing 7 carefully selected stocks with weights that sum to 100%:

1. **Basket 1: Conservative High Return**
   - Risk Rating: Very Low (1/5)
   - Return Rating: Moderate (3/5)
   - Beta: 0.52
   - Expected Return: 8.0%
   - Top Stocks: SMCI (31.54%), LLY (15.69%), MCK (11.77%)

2. **Basket 2: Moderate-Conservative Return**
   - Risk Rating: Low (2/5)
   - Return Rating: Moderate-High (3.5/5)
   - Beta: 0.79
   - Expected Return: 9.5%
   - Top Stocks: AVGO (18.94%), CRWD (17.70%), PANW (14.80%)

3. **Basket 3: Balanced High Return**
   - Risk Rating: Moderate (3/5)
   - Return Rating: High (4/5)
   - Beta: 1.00
   - Expected Return: 11.5%
   - Top Stocks: VST (17.17%), AXON (17.13%), PWR (15.61%)

4. **Basket 4: Growth-Oriented Return**
   - Risk Rating: High (4/5)
   - Return Rating: Very High (4.5/5)
   - Beta: 1.17
   - Expected Return: 13.5%
   - Top Stocks: HWM (17.77%), MPC (15.80%), OXY (14.70%)

5. **Basket 5: Aggressive High Return**
   - Risk Rating: Very High (5/5)
   - Return Rating: Extremely High (5/5)
   - Beta: 1.53
   - Expected Return: 16.0%
   - Top Stocks: TRGP (17.31%), PLTR (16.98%), NVDA (16.85%)

## Methodology

Our approach is based on the following key steps:

1. **Data Preparation**
   - Monthly stock returns are calculated from price data
   - Market returns are created as an equal-weighted average of all stocks
   - A fixed monthly risk-free rate is used (0.05/12 or approximately 0.417%)

2. **Factor Creation**
   - Market factor (MKT): Excess return of the market over the risk-free rate
   - Size factor (SMB): Return difference between small and large stocks
   - Value factor (HML): Return difference between value and growth stocks

3. **Factor Regression**
   - Linear regression of each stock's returns against the factors
   - Each regression provides coefficients (factor loadings) and R-squared values

4. **Risk Scoring and Basket Assignment**
   - Stocks are scored based on standardized factor loadings
   - Composite risk score = Beta + 0.5*SMB + 0.5*HML
   - Stocks are ranked by composite risk score and divided into 5 equally-sized baskets

5. **Return and Volatility Predictions**
   - Expected returns are calculated using factor loadings and expected factor premiums
   - Volatility estimations are based on beta exposure and historical volatility measures

6. **Basket Weight Calculation**
   - Top 7 stocks in each basket are selected based on alpha and factor characteristics
   - Weights are normalized to sum to 100% within each basket
   - Realistic return figures are assigned based on risk profile (8.0% to 16.0%)

## Key Files

- **Implementation**
  - [factor_model.py](scripts/factor_model.py): Implementation of the Fama-French + Beta model
  - [basket_dashboard.py](visualizations/basket_dashboard.py): Enhanced visualization dashboard
  - [recalculate_basket_weights.py](scripts/recalculate_basket_weights.py): Script to calculate basket weights

- **Results**
  - [factor_baskets.csv](results/factor_baskets.csv): Summary of the 5 stock baskets
  - [factor_loadings.csv](results/factor_loadings.csv): Factor exposures for each stock
  - [basket_X_adjusted_weights.csv](results/basket_1_adjusted_weights.csv): Weighted stocks for each basket
  - [realistic_returns.csv](results/realistic_returns.csv): Realistic return figures for each basket

- **Documentation**
  - [executive_summary.md](visualizations/executive_summary.md): Executive summary document
  - [basket_summary.md](results/basket_summary.md): Detailed markdown summary of the baskets
  - [visualization/README.md](visualizations/README.md): Documentation of visualization methods

- **Interactive Dashboard**
  - [index.html](visualizations/index.html): Interactive visualization dashboard

## Visualizations

Our analysis includes the following visualizations:

1. **Risk-Return Profile** ([basket_risk_return_profile.png](visualizations/basket_risk_return_profile.png))
   - Plots each basket on the risk-return spectrum (returns from 8.0% to 16.0%)

2. **Factor Exposures Dashboard** ([basket_factor_exposures.png](visualizations/basket_factor_exposures.png))
   - Visualization of factor loadings across baskets (Beta from 0.52 to 1.53)

3. **Risk-Return Matrix** ([basket_risk_return_matrix.png](visualizations/basket_risk_return_matrix.png))
   - Visual grid showing the distribution of baskets across risk ratings (1-5) and return ratings (3-5)
   - Demonstrates the positive correlation between risk and return across baskets

4. **Basket Characteristics Dashboard** ([basket_characteristics_dashboard.png](visualizations/basket_characteristics_dashboard.png))
   - Comprehensive dashboard of basket performance metrics and volatility
   - Shows the progression of return ratings from Moderate (3/5) to Extremely High (5/5)

5. **Stock Examples** ([basket_stock_examples.png](visualizations/basket_stock_examples.png))
   - Top stocks in each basket with their percentage weights (summing to 100%)

## Portfolio Applications

These stock baskets can be applied in portfolio management in various ways:

1. **Strategic Asset Allocation**
   - Conservative Mix: 50% Basket 1 (Moderate Return), 30% Basket 2 (Moderate-High Return), 20% Basket 3 (High Return) (Expected Return: ~9.2%)
   - Balanced Mix: 20% Basket 1, 30% Basket 2, 30% Basket 3, 20% Basket 4 (Very High Return) (Expected Return: ~10.6%)
   - Aggressive Mix: 10% Basket 1, 15% Basket 3, 30% Basket 4, 45% Basket 5 (Extremely High Return) (Expected Return: ~13.8%)

2. **Tactical Market Positioning**
   - Overweight Basket 1 in uncertain markets for stability with moderate returns (3/5 rating, 8.0%)
   - Overweight Basket 5 in strong bull markets to maximize return potential (5/5 rating, 16.0%)
   - Use Basket 3 as a core holding for balanced exposure (4/5 rating, 11.5%)

## Usage

To view the interactive dashboard, open the `visualizations/index.html` file in a web browser.

To re-run the analysis:

```bash
# Navigate to the data_analysis directory
cd data_analysis

# Run the Fama-French + Beta model
python scripts/factor_model.py

# Create enhanced visualizations
python visualizations/basket_dashboard.py

# Recalculate basket weights
python scripts/recalculate_basket_weights.py
```

## Requirements

- Python 3.6+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn

## License

© 2023 OptiVest. All rights reserved.
