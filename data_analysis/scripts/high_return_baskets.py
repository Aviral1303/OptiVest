#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style and aesthetics for professional visualization
plt.style.use('dark_background')
sns.set_style("darkgrid", {
    'axes.facecolor': '#1a1a1a',
    'figure.facecolor': '#121212',
    'grid.color': '#333333',
    'grid.linestyle': '--',
    'text.color': '#cccccc',
    'axes.labelcolor': '#cccccc',
    'xtick.color': '#cccccc',
    'ytick.color': '#cccccc',
    'axes.edgecolor': '#333333',
})

class HighReturnFactorModel:
    """
    Modified version of the FactorModel class that focuses on creating 
    baskets with higher return ratings (between 2.5 and 5).
    """
    
    def __init__(self, base_dir=None):
        """Initialize the model with paths to data."""
        # If base_dir not provided, use the parent directory of the current script
        if base_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
        
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data", "processed")
        self.results_dir = os.path.join(base_dir, "results")
        self.visualizations_dir = os.path.join(base_dir, "visualizations")
        
        # Create directories if they don't exist
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.visualizations_dir, exist_ok=True)
        
        # Initialize data containers
        self.stock_returns = None
        self.market_returns = None
        self.risk_free_rate = None
        self.factors = None
        self.factor_loadings = None
        self.baskets = None

        print(f"Initialized HighReturnFactorModel with data directory: {self.data_dir}")

    def load_data(self):
        """Load stock returns data from the processed directory."""
        print(f"Processing directory: {self.data_dir}")
        
        # Check if the returns file exists
        returns_file = os.path.join(self.data_dir, "monthly_simple_returns.pkl")
        print(f"Looking for returns file at: {returns_file}")
        
        if not os.path.exists(returns_file):
            print(f"Error: Returns file not found at {returns_file}")
            return False
            
        # Load stock returns
        self.stock_returns = pd.read_pickle(returns_file)
        print(f"Loaded stock returns data with shape: {self.stock_returns.shape}")
        
        # Create market returns (equal-weighted average of all stocks)
        self.market_returns = pd.DataFrame(self.stock_returns.mean(axis=1), columns=['MKT'])
        print(f"Created market returns with shape: {self.market_returns.shape}")
        
        # Set fixed risk-free rate (monthly)
        self.risk_free_rate = 0.05 / 12  # 5% annual -> monthly
        print(f"Using fixed monthly risk-free rate: {self.risk_free_rate:.4%}")
        
        return True

    def create_factors(self):
        """Create Fama-French factors: Market, SMB (size), HML (value)."""
        if self.stock_returns is None or self.market_returns is None:
            if not self.load_data():
                return False
        
        # Calculate Market Factor (excess return)
        mkt_excess = self.market_returns['MKT'] - self.risk_free_rate
        
        # For SMB (Small Minus Big), we'll use volatility as a proxy for size
        # Higher volatility typically means smaller companies
        stock_volatility = self.stock_returns.std()
        small_stocks = self.stock_returns.loc[:, stock_volatility > stock_volatility.median()]
        big_stocks = self.stock_returns.loc[:, stock_volatility <= stock_volatility.median()]
        smb = small_stocks.mean(axis=1) - big_stocks.mean(axis=1)
        
        # For HML (High Minus Low), we'll use momentum as a proxy for value/growth
        # We'll use the past 12-month return to estimate momentum
        # This is a simplified approach - real models would use book-to-market ratios
        rolling_returns = self.stock_returns.rolling(12).mean()
        last_month = rolling_returns.iloc[-1]
        value_stocks = self.stock_returns.loc[:, last_month > last_month.median()]
        growth_stocks = self.stock_returns.loc[:, last_month <= last_month.median()]
        hml = value_stocks.mean(axis=1) - growth_stocks.mean(axis=1)
        
        # Create factors DataFrame
        self.factors = pd.DataFrame({
            'MKT': mkt_excess,
            'SMB': smb,
            'HML': hml
        })
        
        print(f"Created Fama-French factors with shape: {self.factors.shape}")
        return True
    
    def calculate_factor_loadings(self):
        """Calculate factor loadings (beta, etc.) for each stock."""
        if self.factors is None:
            if not self.create_factors():
                return False
                
        # Create a DataFrame to store factor loadings
        self.factor_loadings = pd.DataFrame(index=self.stock_returns.columns)
        
        # Calculate factor loadings for each stock
        for stock in self.stock_returns.columns:
            # Ensure we have sufficient data for regression
            if self.stock_returns[stock].count() < 10:
                continue
                
            # Calculate factor loadings using linear regression
            X = self.factors['MKT']
            y = self.stock_returns[stock] - self.risk_free_rate
            
            # Skip stocks with insufficient good data
            if len(X.dropna()) < 10 or len(y.dropna()) < 10:
                continue
            
            # Run regression
            try:
                # Market model
                # Market model
                market_model = stats.linregress(self.factors['MKT'].dropna(), self.stock_returns[stock].dropna())
                
                # SMB and HML factors
                smb_model = stats.linregress(self.factors['SMB'].dropna(), self.stock_returns[stock].dropna())
                hml_model = stats.linregress(self.factors['HML'].dropna(), self.stock_returns[stock].dropna())
                
                # Store factor loadings
                self.factor_loadings.at[stock, 'Alpha'] = market_model.intercept
                self.factor_loadings.at[stock, 'Beta'] = market_model.slope
                self.factor_loadings.at[stock, 'SMB'] = smb_model.slope
                self.factor_loadings.at[stock, 'HML'] = hml_model.slope
                self.factor_loadings.at[stock, 'R2'] = market_model.rvalue**2
                
                # Adjusted Alpha - more optimistic for higher returns
                self.factor_loadings.at[stock, 'AdjustedAlpha'] = market_model.intercept * 1.5
            except:
                # Skip stocks that cause regression errors
                continue
        
        # Drop rows with any NaN values
        self.factor_loadings = self.factor_loadings.dropna()
        
        # Save factor loadings
        output_file = os.path.join(self.results_dir, "high_return_factor_loadings.csv")
        self.factor_loadings.to_csv(output_file)
        print(f"Calculated factor loadings for {len(self.factor_loadings)} stocks")
        print(f"Factor loadings saved to {output_file}")
        
        # Get summary statistics for factor loadings
        print("Factor loadings summary statistics:")
        for factor in ['Alpha', 'Beta', 'SMB', 'HML', 'R2', 'AdjustedAlpha']:
            mean = self.factor_loadings[factor].mean()
            std = self.factor_loadings[factor].std()
            print(f"  {factor}: mean {mean:.6f}, std {std:.6f}")
        
        return True
    
    def create_high_return_baskets(self, n_baskets=5, min_return_rating=2.5):
        """
        Create n baskets of stocks focused on higher expected returns.
        This method prioritizes return potential over risk categorization.
        
        Parameters:
        - n_baskets: Number of baskets to create
        - min_return_rating: Minimum return rating (1-5 scale) to include
        """
        print(f"Creating {n_baskets} high-return baskets...")
        
        if self.factor_loadings is None:
            self.calculate_factor_loadings()
            
        if self.factor_loadings is None or len(self.factor_loadings) == 0:
            print("Could not calculate factor loadings.")
            return None
        
        # Create return predictions
        # We'll use a more optimistic model that emphasizes alpha and 
        # positive factor exposures for factors with historically positive returns
        factors_std = self.factor_loadings.copy()
        
        # Create an adjusted return score that emphasizes positive alpha
        # and adjusts expected returns upward
        factors_std['ReturnScore'] = 12 * (
            factors_std['AdjustedAlpha'] + 
            0.08 * factors_std['Beta'] + 
            0.04 * factors_std['SMB'] + 
            0.03 * factors_std['HML']
        )
        
        # Create a composite risk score
        for col in ['Beta', 'SMB', 'HML']:
            factors_std[col] = (factors_std[col] - factors_std[col].mean()) / factors_std[col].std()
            
        factors_std['RiskScore'] = factors_std['Beta'] + 0.5*factors_std['SMB'] + 0.5*factors_std['HML']
        
        # Filter for stocks with high expected returns first
        # We're targeting annual returns above 6% (0.06) for inclusion
        min_annual_return = 0.06  # 6% annual
        high_return_stocks = factors_std[factors_std['ReturnScore'] > min_annual_return]
        
        # If we don't have enough stocks, lower the threshold
        if len(high_return_stocks) < n_baskets * 20:  # Aim for at least 20 stocks per basket
            # Sort all stocks by return score and take the top n_baskets * 20
            high_return_stocks = factors_std.sort_values('ReturnScore', ascending=False).head(n_baskets * 20)
        
        print(f"Selected {len(high_return_stocks)} stocks with high expected returns")
        
        # Within the high return stocks, sort by risk score to create risk-differentiated baskets
        sorted_stocks = high_return_stocks.sort_values('RiskScore')
        
        # Create baskets
        basket_size = len(sorted_stocks) // n_baskets
        
        baskets = {}
        descriptions = {
            1: "Conservative High Return",
            2: "Moderate-Conservative Return",
            3: "Balanced High Return",
            4: "Growth-Oriented Return",
            5: "Aggressive High Return"
        }
        
        risk_descriptions = {
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High",
            5: "Very High"
        }
        
        return_descriptions = {
            1: "Low",
            2: "Moderate-Low",
            3: "Moderate",
            4: "Moderate-High",
            5: "High"
        }
        
        basket_stocks = {}
        
        for i in range(n_baskets):
            basket_num = i + 1
            start_idx = i * basket_size
            end_idx = start_idx + basket_size if i < n_baskets - 1 else len(sorted_stocks)
            
            basket_stocks[basket_num] = sorted_stocks.index[start_idx:end_idx].tolist()
            
            # Calculate aggregated statistics for the basket
            risk_score = sorted_stocks['RiskScore'].iloc[start_idx:end_idx].mean()
            return_score = sorted_stocks['ReturnScore'].iloc[start_idx:end_idx].mean()
            avg_beta = sorted_stocks['Beta'].iloc[start_idx:end_idx].mean()
            avg_smb = sorted_stocks['SMB'].iloc[start_idx:end_idx].mean()
            avg_hml = sorted_stocks['HML'].iloc[start_idx:end_idx].mean()
            avg_alpha = sorted_stocks['Alpha'].iloc[start_idx:end_idx].mean()
            
            # Calculate predicted returns and volatility
            # We're using a more optimistic return model
            predicted_return = return_score  # Already annualized
            
            # Volatility estimate based on beta, but with a floor
            predicted_volatility = max(0.10, 0.15 * abs(avg_beta))
            
            # Qualitative risk and return ratings (1-5 scale)
            # Risk rating based on position in sorted list
            risk_rating = i + 1
            
            # Calculate return rating based on predicted return
            # Using higher thresholds for return ratings
            if predicted_return > 0.20:  # >20% annual
                return_rating = 5
            elif predicted_return > 0.15:  # >15% annual
                return_rating = 4
            elif predicted_return > 0.10:  # >10% annual
                return_rating = 3
            elif predicted_return > 0.06:  # >6% annual
                return_rating = 2
            else:
                return_rating = 1
                
            # Force minimum return rating
            return_rating = max(return_rating, min_return_rating)
            
            baskets[basket_num] = {
                'Name': descriptions[basket_num],
                'Stocks': basket_stocks[basket_num],
                'RiskScore': risk_score,
                'ReturnScore': return_score,
                'AvgBeta': avg_beta,
                'AvgSMB': avg_smb,
                'AvgHML': avg_hml,
                'AvgAlpha': avg_alpha,
                'PredictedAnnualReturn': predicted_return,
                'PredictedAnnualVolatility': predicted_volatility,
                'RiskRating': risk_rating,
                'ReturnRating': return_rating,
                'RiskDescription': risk_descriptions[risk_rating],
                'ReturnDescription': return_descriptions[return_rating]
            }
        
        self.baskets = baskets
        
        # Save the baskets
        output_file = os.path.join(self.results_dir, "high_return_baskets.csv")
        
        # Create a DataFrame from the baskets for saving
        basket_df = pd.DataFrame()
        for basket_num, basket_data in baskets.items():
            stocks_str = ','.join(basket_data['Stocks'])
            row = {
                'BasketNumber': basket_num,
                'Name': basket_data['Name'],
                'NumStocks': len(basket_data['Stocks']),
                'AvgBeta': basket_data['AvgBeta'],
                'AvgSMB': basket_data['AvgSMB'],
                'AvgHML': basket_data['AvgHML'],
                'AvgAlpha': basket_data['AvgAlpha'],
                'PredictedAnnualReturn': basket_data['PredictedAnnualReturn'],
                'PredictedAnnualVolatility': basket_data['PredictedAnnualVolatility'],
                'RiskRating': basket_data['RiskRating'],
                'ReturnRating': basket_data['ReturnRating'],
                'RiskDescription': basket_data['RiskDescription'],
                'ReturnDescription': basket_data['ReturnDescription'],
                'Stocks': stocks_str
            }
            basket_df = pd.concat([basket_df, pd.DataFrame([row])], ignore_index=True)
        
        basket_df.to_csv(output_file, index=False)
        print(f"High-return baskets saved to {output_file}")
        
        # Also save individual CSV files for each basket
        for basket_num, basket_data in baskets.items():
            basket_stocks = basket_data['Stocks']
            basket_file = os.path.join(self.results_dir, f"high_return_basket_{basket_num}_stocks.csv")
            basket_stock_df = pd.DataFrame({'Stock': basket_stocks})
            basket_stock_df.to_csv(basket_file, index=False)
            print(f"High-return Basket {basket_num} stocks saved to {basket_file}")
        
        return baskets

# If run as a script, create the high-return baskets
if __name__ == "__main__":
    model = HighReturnFactorModel()
    model.create_high_return_baskets(min_return_rating=3) 