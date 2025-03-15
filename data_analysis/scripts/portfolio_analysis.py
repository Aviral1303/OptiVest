import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pickle

class PortfolioAnalyzer:
    """
    A class for analyzing stock data and optimizing portfolios.
    """
    
    def __init__(self, base_dir=None):
        """
        Initialize the PortfolioAnalyzer with paths to data directories.
        
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
        self.prices = None
        self.returns = None
        self.market_prices = None
        self.market_returns = None
        
        self.load_data()
    
    def load_data(self):
        """
        Load processed data from files.
        """
        try:
            # Load price data
            price_file = os.path.join(self.processed_dir, "price_matrix_close.pkl")
            if os.path.exists(price_file):
                self.prices = pd.read_pickle(price_file)
                print(f"Loaded price data with shape {self.prices.shape}")
            else:
                print(f"Price file not found: {price_file}")
            
            # Load returns data
            returns_file = os.path.join(self.processed_dir, "daily_simple_returns.pkl")
            if os.path.exists(returns_file):
                self.returns = pd.read_pickle(returns_file)
                print(f"Loaded returns data with shape {self.returns.shape}")
            else:
                print(f"Returns file not found: {returns_file}")
            
            # Load market data
            market_file = os.path.join(self.processed_dir, "market_prices.csv")
            if os.path.exists(market_file):
                self.market_prices = pd.read_csv(market_file, index_col=0, parse_dates=True)
                print(f"Loaded market price data with shape {self.market_prices.shape}")
            else:
                print(f"Market price file not found: {market_file}")
            
            market_returns_file = os.path.join(self.processed_dir, "market_returns.csv")
            if os.path.exists(market_returns_file):
                self.market_returns = pd.read_csv(market_returns_file, index_col=0, parse_dates=True)
                print(f"Loaded market returns data with shape {self.market_returns.shape}")
            else:
                print(f"Market returns file not found: {market_returns_file}")
                
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def calculate_statistics(self, period='1Y'):
        """
        Calculate basic statistics for stocks.
        
        Parameters:
        -----------
        period : str
            Time period for analysis ('1Y', '2Y', '5Y', 'All')
            
        Returns:
        --------
        DataFrame
            Statistics for each stock
        """
        if self.returns is None:
            print("Returns data not loaded")
            return None
        
        # Filter data for the specified period
        end_date = self.returns.index.max()
        
        if period == '1Y':
            start_date = end_date - timedelta(days=365)
        elif period == '2Y':
            start_date = end_date - timedelta(days=2*365)
        elif period == '5Y':
            start_date = end_date - timedelta(days=5*365)
        else:  # 'All'
            start_date = self.returns.index.min()
        
        filtered_returns = self.returns[(self.returns.index >= start_date) & (self.returns.index <= end_date)]
        
        # Calculate statistics
        stats = pd.DataFrame({
            'Mean Daily Return': filtered_returns.mean(),
            'Std Dev Daily Return': filtered_returns.std(),
            'Annualized Return': (1 + filtered_returns.mean()) ** 252 - 1,
            'Annualized Volatility': filtered_returns.std() * np.sqrt(252),
            'Sharpe Ratio': (filtered_returns.mean() / filtered_returns.std()) * np.sqrt(252),
            'Max Drawdown': self.calculate_max_drawdown(filtered_returns),
            'Positive Days %': (filtered_returns > 0).mean() * 100
        })
        
        # Sort by Sharpe Ratio
        stats = stats.sort_values('Sharpe Ratio', ascending=False)
        
        # Save to CSV
        output_file = os.path.join(self.results_dir, f"stock_statistics_{period}.csv")
        stats.to_csv(output_file)
        print(f"Statistics saved to {output_file}")
        
        return stats
    
    def calculate_max_drawdown(self, returns):
        """
        Calculate maximum drawdown for each stock.
        
        Parameters:
        -----------
        returns : DataFrame
            Returns data
            
        Returns:
        --------
        Series
            Maximum drawdown for each stock
        """
        # Convert returns to cumulative returns
        cum_returns = (1 + returns).cumprod()
        
        # Calculate running maximum
        running_max = cum_returns.cummax()
        
        # Calculate drawdown
        drawdown = (cum_returns / running_max) - 1
        
        # Get maximum drawdown
        max_drawdown = drawdown.min()
        
        return max_drawdown
    
    def plot_correlation_matrix(self, n_stocks=30, period='1Y'):
        """
        Plot correlation matrix for top n stocks.
        
        Parameters:
        -----------
        n_stocks : int
            Number of stocks to include
        period : str
            Time period for analysis ('1Y', '2Y', '5Y', 'All')
        """
        if self.returns is None:
            print("Returns data not loaded")
            return
        
        # Get statistics to find top stocks
        stats = self.calculate_statistics(period)
        
        # Select top n stocks by Sharpe ratio
        top_stocks = stats.head(n_stocks).index.tolist()
        
        # Filter returns for top stocks
        top_returns = self.returns[top_stocks]
        
        # Calculate correlation matrix
        corr_matrix = top_returns.corr()
        
        # Create plot
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
        plt.title(f'Correlation Matrix for Top {n_stocks} Stocks ({period})')
        plt.tight_layout()
        
        # Save plot
        output_file = os.path.join(self.visualizations_dir, f"correlation_matrix_{period}_{n_stocks}_stocks.png")
        plt.savefig(output_file, dpi=300)
        print(f"Correlation matrix plot saved to {output_file}")
        
        plt.close()
    
    def plot_cumulative_returns(self, tickers=None, period='1Y', market_comparison=True):
        """
        Plot cumulative returns for selected stocks.
        
        Parameters:
        -----------
        tickers : list
            List of stock tickers to plot
        period : str
            Time period for analysis ('1Y', '2Y', '5Y', 'All')
        market_comparison : bool
            Whether to include market (S&P 500) for comparison
        """
        if self.returns is None:
            print("Returns data not loaded")
            return
        
        # Filter data for the specified period
        end_date = self.returns.index.max()
        
        if period == '1Y':
            start_date = end_date - timedelta(days=365)
        elif period == '2Y':
            start_date = end_date - timedelta(days=2*365)
        elif period == '5Y':
            start_date = end_date - timedelta(days=5*365)
        else:  # 'All'
            start_date = self.returns.index.min()
        
        # If no tickers provided, use top 5 by Sharpe ratio
        if tickers is None:
            stats = self.calculate_statistics(period)
            tickers = stats.head(5).index.tolist()
        
        # Filter returns for selected stocks
        selected_returns = self.returns[tickers]
        selected_returns = selected_returns[(selected_returns.index >= start_date) & (selected_returns.index <= end_date)]
        
        # Calculate cumulative returns
        cum_returns = (1 + selected_returns).cumprod()
        
        # Create plot
        plt.figure(figsize=(12, 8))
        
        # Plot stock returns
        for ticker in tickers:
            plt.plot(cum_returns.index, cum_returns[ticker], label=ticker)
        
        # Add market comparison if requested
        if market_comparison and self.market_returns is not None:
            market_returns = self.market_returns['SPY']
            market_returns = market_returns[(market_returns.index >= start_date) & (market_returns.index <= end_date)]
            market_cum_returns = (1 + market_returns).cumprod()
            plt.plot(market_cum_returns.index, market_cum_returns, 'k--', label='S&P 500 (SPY)')
        
        plt.title(f'Cumulative Returns ({period})')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save plot
        tickers_str = '_'.join(tickers) if len(tickers) <= 3 else f"{len(tickers)}_stocks"
        output_file = os.path.join(self.visualizations_dir, f"cumulative_returns_{period}_{tickers_str}.png")
        plt.savefig(output_file, dpi=300)
        print(f"Cumulative returns plot saved to {output_file}")
        
        plt.close()
    
    def run_basic_analysis(self):
        """
        Run a basic analysis of the stock data.
        """
        print("\n=== Running Basic Analysis ===")
        
        # Calculate statistics for different time periods
        for period in ['1Y', '2Y', 'All']:
            print(f"\nStatistics for {period}:")
            stats = self.calculate_statistics(period)
            print(stats.head(10)[['Annualized Return', 'Annualized Volatility', 'Sharpe Ratio']])
        
        # Plot correlation matrices
        for period in ['1Y', 'All']:
            self.plot_correlation_matrix(n_stocks=30, period=period)
        
        # Plot cumulative returns for top performers
        for period in ['1Y', 'All']:
            stats = self.calculate_statistics(period)
            top_tickers = stats.head(5).index.tolist()
            self.plot_cumulative_returns(tickers=top_tickers, period=period)
        
        print("\nBasic analysis complete!")

if __name__ == "__main__":
    analyzer = PortfolioAnalyzer()
    analyzer.run_basic_analysis() 