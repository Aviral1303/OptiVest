# OptiVest Stock Basket Analysis Documentation

## Overview

This document provides comprehensive documentation for the OptiVest stock picking methodology, which uses a multi-factor approach based on the Fama-French framework with additional beta factors to categorize stocks into distinct risk-based baskets.

## Stock Selection Methodology

Our approach uses a systematic, factor-based stock selection process:

### 1. Factor Model Implementation

We implemented a **Modified Fama-French + Beta Model** that analyzes stocks based on key risk factors:

- **Market Beta (β)**: Measures sensitivity to market movements
  - β > 1: Higher market sensitivity (amplifies market movements)
  - β = 1: Moves with the market
  - β < 0: Moves counter to the market (defensive stocks)
  
- **Size Factor (SMB - Small Minus Big)**:
  - Positive values: Greater exposure to small-cap characteristics 
  - Negative values: Greater exposure to large-cap characteristics
  
- **Value Factor (HML - High Minus Low)**:
  - Positive values: Greater exposure to value characteristics
  - Negative values: Greater exposure to growth characteristics
  
- **Alpha (α)**: Risk-adjusted excess returns
  - Measures stock performance beyond what would be predicted by its risk factors

### 2. Factor Loading Calculation

For each stock, we performed regression analysis against these factors:

```python
# For each stock, calculate factor loadings
market_model = stats.linregress(factors['MKT'], stock_returns[stock])
smb_model = stats.linregress(factors['SMB'], stock_returns[stock])
hml_model = stats.linregress(factors['HML'], stock_returns[stock])

# Extract key parameters
beta = market_model.slope
alpha = market_model.intercept
r_squared = market_model.rvalue**2
```

### 3. Risk Score Calculation

We created a composite risk score using a weighted combination of factor exposures:

```python
# Standardize the factors first
factors_std[col] = (factors_std[col] - factors_std[col].mean()) / factors_std[col].std()

# Create composite risk score with appropriate weights
factors_std['RiskScore'] = factors_std['Beta'] + 0.5*factors_std['SMB'] + 0.5*factors_std['HML']
```

### 4. Basket Creation

Based on the risk scores, we divided stocks into 5 distinct risk-based baskets:

| Basket | Profile | Risk Rating | Beta Range | Key Characteristics |
|--------|---------|-------------|------------|---------------------|
| 1 | Defensive | Very Low | ~ -1.30 | Negative beta, counter-cyclical, often outperforms in down markets |
| 2 | Stable Growth | Low | ~ -0.55 | Slightly negative beta, stable, low volatility |
| 3 | Balanced | Moderate | ~ 0.00 | Neutral beta, balanced risk-return |
| 4 | Growth | High | ~ 0.44 | Positive beta, follows market trends |
| 5 | Aggressive Growth | Very High | ~ 1.36 | High beta, amplifies market movements |

## Model Implementation Details

The model is implemented in the `factor_model.py` script in the following steps:

### 1. Data Preparation
- Monthly stock returns data is loaded from the processed data directory
- Market returns are created as an equal-weighted average of all stocks
- A fixed monthly risk-free rate of 0.05/12 (approximately 0.417%) is used

### 2. Factor Creation
- Market factor (MKT): Excess return of the market over the risk-free rate
- Size factor (SMB): Return difference between small and large stocks (based on volatility as a proxy)
- Value factor (HML): Return difference between value and growth stocks (based on momentum as a proxy)

### 3. Factor Regression
- Linear regression of each stock's returns against the factors
- Each regression provides coefficients (factor loadings) and R-squared values

### 4. Risk Scoring and Basket Assignment
- Stocks are scored based on standardized factor loadings
- Stocks are ranked by composite risk score
- The stock universe is divided into 5 equally-sized baskets

### 5. Return and Volatility Predictions
- Expected returns are calculated using factor loadings and expected factor premiums
- Volatility estimations are based on beta exposure and historical volatility measures

## Visualization Guide

Our visualization suite includes multiple perspectives on the basket characteristics:

### 1. Risk-Return Profile
`factor_baskets_risk_return_enhanced.png`

This visualization shows:
- Each basket's position on the risk-return spectrum
- Basket size indicates risk rating (larger = higher risk)
- A simulated efficient frontier for context
- The risk-free rate and market return benchmark

### 2. Factor Exposures
`factor_baskets_exposures.png`

This visualization shows:
- Average factor exposures (Beta, SMB, HML) for each basket
- Clear progression of factor values across baskets
- Actual factor values labeled on each bar

### 3. Risk-Return Rating Matrix
`factor_baskets_rating_matrix.png`

This visualization shows:
- A matrix view of risk ratings (x-axis) vs. return ratings (y-axis)
- Shows the distribution of baskets across the risk-return space
- Helps identify clusters and gaps in the risk-return coverage

## Basket Characteristics and Stock Examples

### Basket 1: Low Risk / Defensive
- **Risk Rating**: Very Low (1/5)
- **Return Rating**: Moderate-High (4/5)
- **Average Beta**: -1.30
- **Expected Annual Return**: 12.94%
- **Expected Annual Volatility**: 5.00%
- **Example Stocks**: BIIB, GIS, NOC, LLY, CPB

### Basket 2: Moderate-Low Risk / Stable Growth
- **Risk Rating**: Low (2/5)
- **Return Rating**: Low (1/5)
- **Average Beta**: -0.55
- **Expected Annual Return**: -0.61%
- **Expected Annual Volatility**: 5.00%
- **Example Stocks**: LDOS, CI, RTX, D, ORLY

### Basket 3: Moderate Risk / Balanced
- **Risk Rating**: Moderate (3/5)
- **Return Rating**: Low (1/5)
- **Average Beta**: 0.00
- **Expected Annual Return**: 3.68%
- **Expected Annual Volatility**: 5.00%
- **Example Stocks**: FI, ANET, SBAC, CDNS, HOLX

### Basket 4: Moderate-High Risk / Growth
- **Risk Rating**: High (4/5)
- **Return Rating**: Low (1/5)
- **Average Beta**: 0.44
- **Expected Annual Return**: -15.45%
- **Expected Annual Volatility**: 6.57%
- **Example Stocks**: COO, DVA, WST, MMM, GPN

### Basket 5: High Risk / Aggressive Growth
- **Risk Rating**: Very High (5/5)
- **Return Rating**: Low (1/5)
- **Average Beta**: 1.36
- **Expected Annual Return**: -0.53%
- **Expected Annual Volatility**: 20.39%
- **Example Stocks**: VLO, IFF, TFX, EQT, NSC

## Investment Applications

These stock baskets can be used for:

1. **Portfolio Construction**: Build diversified portfolios using stocks from different baskets
2. **Risk Management**: Adjust portfolio risk by allocating more or less to specific baskets
3. **Market Timing**: Tilt allocations based on market outlook (more defensive in downturns, more aggressive in bull markets)
4. **Goal-Based Investing**: Match specific baskets to investor goals and risk tolerance

## Conclusion

The OptiVest stock basket methodology provides a systematic, factor-based approach to organizing the stock universe into cohesive risk-based categories. This approach combines rigorous quantitative analysis with practical portfolio applications, enabling more informed investment decisions. 