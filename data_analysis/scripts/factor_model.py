import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime, timedelta
import pickle
import warnings
warnings.filterwarnings('ignore')

class FactorModel:
    """
    A class for implementing a Fama-French + Beta factor model for stock analysis
    and creating baskets based on risk and return characteristics.
    """
    
    def __init__(self, base_dir=None):
        """
        Initialize the FactorModel with paths to data directories.
        
        Parameters:
        -----------
        base_dir : str
            Base directory for the data analysis project
        """
        if base_dir is None:
            # Get the absolute path of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the data_analysis directory
            base_dir = os.path.dirname(current_dir)
            
        self.data_dir = os.path.join(base_dir, "data")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.results_dir = os.path.join(base_dir, "results")
        self.visualizations_dir = os.path.join(base_dir, "visualizations")
        
        # Create directories if they don't exist
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.visualizations_dir, exist_ok=True)
        
        # Load data
        self.stock_returns = None
        self.market_returns = None
        self.factors = None
        self.risk_free_rate = 0.05  # Assuming 5% annual risk-free rate
        
        # Factor loadings
        self.factor_loadings = None
        self.baskets = None
        
        print(f"Processed directory: {self.processed_dir}")
        
        self.load_data()
    
    def load_data(self):
        """
        Load processed data from files.
        """
        try:
            # Load monthly returns data for Fama-French model
            returns_file = os.path.join(self.processed_dir, "monthly_simple_returns.pkl")
            print(f"Looking for returns file at: {returns_file}")
            print(f"File exists: {os.path.exists(returns_file)}")
            
            if os.path.exists(returns_file):
                try:
                    self.stock_returns = pd.read_pickle(returns_file)
                    print(f"Loaded stock returns data with shape {self.stock_returns.shape}")
                except Exception as e:
                    print(f"Error loading returns data: {str(e)}")
            else:
                print(f"Returns file not found: {returns_file}")
                
                # Try listing all files in the processed directory
                try:
                    print("Files in processed directory:")
                    print(os.listdir(self.processed_dir))
                except Exception as e:
                    print(f"Error listing files: {str(e)}")
            
            # Instead of trying to resample market returns, we'll use the stock data
            # to create our own market proxy (equal-weighted index)
            if self.stock_returns is not None:
                # Create market return as equal-weighted average of all stocks
                self.market_returns = pd.DataFrame(index=self.stock_returns.index)
                self.market_returns['MKT'] = self.stock_returns.mean(axis=1)
                print(f"Created market returns with shape {self.market_returns.shape}")
                
                # Use a fixed risk-free rate
                self.risk_free_rate = 0.05 / 12  # Convert annual to monthly
                print(f"Using fixed monthly risk-free rate of {self.risk_free_rate:.4%}")
                
        except Exception as e:
            print(f"Error in load_data method: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def create_factors(self):
        """
        Create Fama-French factors from the data.
        - Market factor (MKT): Market return - Risk-free rate
        - Size factor (SMB): Small minus big based on market cap
        - Value factor (HML): High minus low based on book-to-market ratio
        
        Since we don't have book-to-market ratios, we'll use a momentum-based proxy.
        Since we don't have market cap data, we'll use volatility as a proxy for size.
        """
        print("Creating Fama-French factors...")
        
        if self.stock_returns is None or self.market_returns is None:
            print("Stock or market returns data not loaded.")
            return None
        
        # Create a dataframe to store the factors
        factors = pd.DataFrame(index=self.stock_returns.index)
        
        # 1. Market factor (MKT): Market return - Risk-free rate
        factors['MKT'] = self.market_returns['MKT'] - self.risk_free_rate
        
        # Calculate stock metrics for factor creation
        # We'll calculate rolling metrics using 12-month windows
        stock_metrics = pd.DataFrame(index=self.stock_returns.columns)
        
        # Calculate volatility (proxy for size)
        stock_volatility = self.stock_returns.std()
        stock_metrics['Volatility'] = stock_volatility
        
        # Calculate momentum (proxy for value)
        # Use cumulative returns over the available period
        stock_momentum = self.stock_returns.mean()
        stock_metrics['Momentum'] = stock_momentum
        
        # 2. Size factor (SMB - Small Minus Big)
        # Consider high volatility as small cap, low volatility as large cap
        size_sorted = stock_metrics.sort_values('Volatility', ascending=False)
        small_stocks = size_sorted.index[:len(size_sorted)//3]
        big_stocks = size_sorted.index[-len(size_sorted)//3:]
        
        # Calculate SMB factor
        for date in self.stock_returns.index:
            small_return = self.stock_returns.loc[date, small_stocks].mean()
            big_return = self.stock_returns.loc[date, big_stocks].mean()
            factors.loc[date, 'SMB'] = small_return - big_return
        
        # 3. Value factor (HML - High Minus Low)
        # Consider low momentum as high book-to-market, high momentum as low book-to-market
        value_sorted = stock_metrics.sort_values('Momentum', ascending=True)
        high_stocks = value_sorted.index[:len(value_sorted)//3]
        low_stocks = value_sorted.index[-len(value_sorted)//3:]
        
        # Calculate HML factor
        for date in self.stock_returns.index:
            high_return = self.stock_returns.loc[date, high_stocks].mean()
            low_return = self.stock_returns.loc[date, low_stocks].mean()
            factors.loc[date, 'HML'] = high_return - low_return
        
        self.factors = factors
        print(f"Created factors with shape {factors.shape}")
        return factors
    
    def calculate_factor_loadings(self):
        """
        Calculate factor loadings for each stock using linear regression.
        For each stock, we regress its returns against the Fama-French factors.
        """
        print("Calculating factor loadings...")
        
        if self.factors is None:
            self.create_factors()
            
        if self.factors is None:
            print("Could not create factors.")
            return None
        
        # Dictionary to store regression results
        loadings = {}
        
        # For each stock, run a regression of returns against factors
        for stock in self.stock_returns.columns:
            y = self.stock_returns[stock].values
            X = self.factors.values
            
            # Skip stocks with insufficient data
            if len(y) < 5:
                continue
                
            try:
                # Run regressions for each factor
                market_model = stats.linregress(self.factors['MKT'], self.stock_returns[stock])
                smb_model = stats.linregress(self.factors['SMB'], self.stock_returns[stock])
                hml_model = stats.linregress(self.factors['HML'], self.stock_returns[stock])
                
                # Calculate Alpha (intercept) using the market model
                beta = market_model.slope
                alpha = market_model.intercept
                r_squared = market_model.rvalue**2
                
                loadings[stock] = {
                    'Alpha': alpha * 12,  # Annualize alpha
                    'Beta': beta,
                    'SMB': smb_model.slope,
                    'HML': hml_model.slope,
                    'R2': r_squared
                }
            except Exception as e:
                print(f"Error calculating factors for {stock}: {str(e)}")
        
        # Convert to DataFrame
        self.factor_loadings = pd.DataFrame.from_dict(loadings, orient='index')
        print(f"Calculated factor loadings for {len(self.factor_loadings)} stocks")
        
        # Print summary statistics
        print("Factor loadings summary statistics:")
        print(self.factor_loadings.describe())
        
        # Save the factor loadings
        output_file = os.path.join(self.results_dir, "factor_loadings.csv")
        self.factor_loadings.to_csv(output_file)
        print(f"Factor loadings saved to {output_file}")
        
        return self.factor_loadings
    
    def create_baskets(self, n_baskets=5):
        """
        Create n baskets of stocks based on their factor loadings.
        
        We'll create a combined risk score based on:
        1. Market Beta - higher means more market risk
        2. Size exposure (SMB) - higher means more exposure to small caps
        3. Value exposure (HML) - higher means more exposure to value stocks
        4. Alpha - higher means better risk-adjusted performance
        """
        print(f"Creating {n_baskets} baskets based on factor loadings...")
        
        if self.factor_loadings is None:
            self.calculate_factor_loadings()
            
        if self.factor_loadings is None or len(self.factor_loadings) == 0:
            print("Could not calculate factor loadings.")
            return None
        
        # Create a composite risk score
        # Standardize the factors first
        factors_std = self.factor_loadings.copy()
        for col in factors_std.columns:
            if col in ['Alpha', 'Beta', 'SMB', 'HML']:
                factors_std[col] = (factors_std[col] - factors_std[col].mean()) / factors_std[col].std()
        
        # Create composite risk score
        # High beta, high SMB, high HML -> higher risk
        # Alpha is not included in risk score, but will be used for return expectations
        factors_std['RiskScore'] = factors_std['Beta'] + 0.5*factors_std['SMB'] + 0.5*factors_std['HML']
        
        # Sort by risk score
        sorted_stocks = factors_std.sort_values('RiskScore')
        
        # Create baskets
        basket_size = len(sorted_stocks) // n_baskets
        
        baskets = {}
        descriptions = {
            1: "Low Risk / Defensive",
            2: "Moderate-Low Risk / Stable Growth",
            3: "Moderate Risk / Balanced",
            4: "Moderate-High Risk / Growth",
            5: "High Risk / Aggressive Growth"
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
            return_score = sorted_stocks['Alpha'].iloc[start_idx:end_idx].mean()
            avg_beta = sorted_stocks['Beta'].iloc[start_idx:end_idx].mean()
            avg_smb = sorted_stocks['SMB'].iloc[start_idx:end_idx].mean()
            avg_hml = sorted_stocks['HML'].iloc[start_idx:end_idx].mean()
            
            # Calculate predicted returns and volatility
            # This is simplified and would be more complex in a real model
            predicted_return = avg_beta * 0.08 + avg_smb * 0.03 + avg_hml * 0.04 + return_score
            predicted_volatility = 0.15 * avg_beta  # Simple approximation
            
            # Ensure we have positive volatility
            predicted_volatility = max(0.05, predicted_volatility)
            
            # Qualitative risk and return ratings (1-5 scale)
            risk_rating = i + 1
            
            # Calculate return rating based on relative ranking within our baskets
            return_rating = min(5, max(1, risk_rating))  # Default to matching risk rating
            if predicted_return > 0.15:  # Adjust based on absolute return levels
                return_rating = 5
            elif predicted_return > 0.12:
                return_rating = 4
            elif predicted_return > 0.09:
                return_rating = 3
            elif predicted_return > 0.06:
                return_rating = 2
            else:
                return_rating = 1
            
            baskets[basket_num] = {
                'Name': descriptions[basket_num],
                'Stocks': basket_stocks[basket_num],
                'RiskScore': risk_score,
                'ReturnScore': return_score,
                'AvgBeta': avg_beta,
                'AvgSMB': avg_smb,
                'AvgHML': avg_hml,
                'PredictedAnnualReturn': predicted_return,
                'PredictedAnnualVolatility': predicted_volatility,
                'RiskRating': risk_rating,
                'ReturnRating': return_rating,
                'RiskDescription': risk_descriptions[risk_rating],
                'ReturnDescription': return_descriptions[return_rating]
            }
        
        self.baskets = baskets
        
        # Save the baskets
        output_file = os.path.join(self.results_dir, "factor_baskets.csv")
        
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
        print(f"Baskets saved to {output_file}")
        
        # Also save individual CSV files for each basket
        for basket_num, basket_data in baskets.items():
            basket_stocks = basket_data['Stocks']
            basket_file = os.path.join(self.results_dir, f"basket_{basket_num}_stocks.csv")
            basket_stock_df = pd.DataFrame({'Stock': basket_stocks})
            basket_stock_df.to_csv(basket_file, index=False)
            print(f"Basket {basket_num} stocks saved to {basket_file}")
        
        return baskets
    
    def plot_basket_characteristics(self):
        """
        Plot characteristics of each basket to visualize their differences.
        """
        if self.baskets is None:
            print("Baskets have not been created yet.")
            return
        
        # Extract data for plotting
        basket_nums = []
        risk_ratings = []
        return_ratings = []
        betas = []
        returns = []
        volatilities = []
        
        for basket_num, basket_data in self.baskets.items():
            basket_nums.append(basket_num)
            risk_ratings.append(basket_data['RiskRating'])
            return_ratings.append(basket_data['ReturnRating'])
            betas.append(basket_data['AvgBeta'])
            returns.append(basket_data['PredictedAnnualReturn'])
            volatilities.append(basket_data['PredictedAnnualVolatility'])
        
        # Create a figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Risk vs. Return Ratings
        ax = axes[0, 0]
        sns.scatterplot(x=risk_ratings, y=return_ratings, s=200, ax=ax, hue=basket_nums, palette='viridis')
        for i, basket_num in enumerate(basket_nums):
            ax.text(risk_ratings[i], return_ratings[i], f"Basket {basket_num}", ha='center', va='center')
        ax.set_xlabel('Risk Rating (1-5)')
        ax.set_ylabel('Return Rating (1-5)')
        ax.set_title('Risk vs. Return Ratings by Basket')
        ax.grid(True, alpha=0.3)
        
        # Beta distribution
        ax = axes[0, 1]
        sns.barplot(x=basket_nums, y=betas, ax=ax, palette='viridis')
        ax.set_xlabel('Basket Number')
        ax.set_ylabel('Average Beta')
        ax.set_title('Average Beta by Basket')
        ax.grid(True, alpha=0.3)
        
        # Expected return distribution
        ax = axes[1, 0]
        sns.barplot(x=basket_nums, y=returns, ax=ax, palette='viridis')
        ax.set_xlabel('Basket Number')
        ax.set_ylabel('Expected Annual Return')
        ax.set_title('Expected Annual Return by Basket')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, max(returns) * 1.2)
        
        # Expected volatility distribution
        ax = axes[1, 1]
        sns.barplot(x=basket_nums, y=volatilities, ax=ax, palette='viridis')
        ax.set_xlabel('Basket Number')
        ax.set_ylabel('Expected Annual Volatility')
        ax.set_title('Expected Annual Volatility by Basket')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, max(volatilities) * 1.2)
        
        plt.tight_layout()
        
        # Save the plot
        output_file = os.path.join(self.visualizations_dir, "factor_baskets_characteristics.png")
        plt.savefig(output_file, dpi=300)
        print(f"Basket characteristics plot saved to {output_file}")
        
        plt.close()
        
        # Create a risk vs. return scatter plot with efficient frontier
        plt.figure(figsize=(10, 8))
        
        # Plot risk vs. return for each basket
        plt.scatter(volatilities, returns, s=150, c=basket_nums, cmap='viridis')
        
        # Label each point
        for i, basket_num in enumerate(basket_nums):
            plt.annotate(f"Basket {basket_num}",
                         (volatilities[i], returns[i]),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')
        
        plt.xlabel('Expected Annual Volatility')
        plt.ylabel('Expected Annual Return')
        plt.title('Risk-Return Profile of Stock Baskets')
        plt.grid(True, alpha=0.3)
        plt.colorbar(label='Basket Number')
        
        # Save the plot
        output_file = os.path.join(self.visualizations_dir, "factor_baskets_risk_return.png")
        plt.savefig(output_file, dpi=300)
        print(f"Risk-return plot saved to {output_file}")
        
        plt.close()

if __name__ == "__main__":
    # Create an instance of the FactorModel
    print("Creating Fama-French + Beta factor model...")
    model = FactorModel()
    
    # Create factors
    model.create_factors()
    
    # Calculate factor loadings
    model.calculate_factor_loadings()
    
    # Create 5 baskets
    model.create_baskets(n_baskets=5)
    
    # Plot basket characteristics
    model.plot_basket_characteristics()
    
    print("Factor model analysis complete!") 