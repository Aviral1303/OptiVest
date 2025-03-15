import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pickle
import scipy.optimize as sco

class PortfolioOptimizer:
    """
    A class for optimizing portfolios using modern portfolio theory.
    """
    
    def __init__(self, base_dir=None):
        """
        Initialize the PortfolioOptimizer with paths to data directories.
        
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
        self.returns = None
        self.market_returns = None
        self.risk_free_rate = 0.05  # Assuming 5% annual risk-free rate
        
        # Print paths for debugging
        print(f"Processed directory: {self.processed_dir}")
        
        self.load_data()
    
    def load_data(self):
        """
        Load processed data from files.
        """
        try:
            # Load returns data - check for file existence first
            returns_file = os.path.join(self.processed_dir, "daily_simple_returns.pkl")
            print(f"Looking for returns file at: {returns_file}")
            print(f"File exists: {os.path.exists(returns_file)}")
            
            if os.path.exists(returns_file):
                try:
                    self.returns = pd.read_pickle(returns_file)
                    print(f"Loaded returns data with shape {self.returns.shape}")
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
            
            # Load market returns data
            market_returns_file = os.path.join(self.processed_dir, "market_returns.csv")
            if os.path.exists(market_returns_file):
                self.market_returns = pd.read_csv(market_returns_file, index_col=0, parse_dates=True)
                print(f"Loaded market returns data with shape {self.market_returns.shape}")
                
                # Extract risk-free rate from T-bill data if available
                if 'IRX' in self.market_returns.columns:
                    # Convert from daily to annual rate
                    self.risk_free_rate = self.market_returns['IRX'].mean() * 252
                    print(f"Using risk-free rate of {self.risk_free_rate:.2%} from T-bill data")
            else:
                print(f"Market returns file not found: {market_returns_file}")
                
        except Exception as e:
            print(f"Error in load_data method: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def select_stocks(self, n_stocks=20, period='1Y', method='sharpe'):
        """
        Select stocks for portfolio optimization.
        
        Parameters:
        -----------
        n_stocks : int
            Number of stocks to select
        period : str
            Time period for analysis ('1Y', '2Y', '5Y', 'All')
        method : str
            Method for selecting stocks ('sharpe', 'return', 'volatility')
            
        Returns:
        --------
        list
            List of selected stock tickers
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
        mean_returns = filtered_returns.mean()
        std_returns = filtered_returns.std()
        sharpe_ratios = (mean_returns / std_returns) * np.sqrt(252)
        
        # Select stocks based on the specified method
        if method == 'sharpe':
            selected_stocks = sharpe_ratios.sort_values(ascending=False).head(n_stocks).index.tolist()
        elif method == 'return':
            selected_stocks = mean_returns.sort_values(ascending=False).head(n_stocks).index.tolist()
        elif method == 'volatility':
            selected_stocks = std_returns.sort_values(ascending=True).head(n_stocks).index.tolist()
        else:
            print(f"Invalid selection method: {method}")
            return None
        
        return selected_stocks
    
    def portfolio_annualized_performance(self, weights, mean_returns, cov_matrix):
        """
        Calculate annualized return and volatility for a portfolio.
        
        Parameters:
        -----------
        weights : array
            Portfolio weights
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
            
        Returns:
        --------
        tuple
            (annualized_return, annualized_volatility)
        """
        returns = np.sum(mean_returns * weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return returns, std
    
    def negative_sharpe_ratio(self, weights, mean_returns, cov_matrix, risk_free_rate):
        """
        Calculate negative Sharpe ratio (for minimization).
        
        Parameters:
        -----------
        weights : array
            Portfolio weights
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
        risk_free_rate : float
            Risk-free rate
            
        Returns:
        --------
        float
            Negative Sharpe ratio
        """
        p_ret, p_vol = self.portfolio_annualized_performance(weights, mean_returns, cov_matrix)
        return -(p_ret - risk_free_rate) / p_vol
    
    def max_sharpe_ratio(self, mean_returns, cov_matrix, risk_free_rate):
        """
        Find the portfolio weights that maximize the Sharpe ratio.
        
        Parameters:
        -----------
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
        risk_free_rate : float
            Risk-free rate
            
        Returns:
        --------
        tuple
            (optimal_weights, performance_metrics)
        """
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix, risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        
        initial_guess = np.array([1/num_assets] * num_assets)
        
        result = sco.minimize(self.negative_sharpe_ratio, initial_guess,
                             args=args, method='SLSQP', bounds=bounds,
                             constraints=constraints)
        
        optimal_weights = result['x']
        performance = self.portfolio_annualized_performance(optimal_weights, mean_returns, cov_matrix)
        sharpe_ratio = (performance[0] - risk_free_rate) / performance[1]
        
        return optimal_weights, {
            'Return': performance[0],
            'Volatility': performance[1],
            'Sharpe Ratio': sharpe_ratio
        }
    
    def portfolio_volatility(self, weights, mean_returns, cov_matrix):
        """
        Calculate portfolio volatility.
        
        Parameters:
        -----------
        weights : array
            Portfolio weights
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
            
        Returns:
        --------
        float
            Portfolio volatility
        """
        return self.portfolio_annualized_performance(weights, mean_returns, cov_matrix)[1]
    
    def min_volatility(self, mean_returns, cov_matrix):
        """
        Find the portfolio weights that minimize volatility.
        
        Parameters:
        -----------
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
            
        Returns:
        --------
        tuple
            (optimal_weights, performance_metrics)
        """
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        
        initial_guess = np.array([1/num_assets] * num_assets)
        
        result = sco.minimize(self.portfolio_volatility, initial_guess,
                             args=args, method='SLSQP', bounds=bounds,
                             constraints=constraints)
        
        optimal_weights = result['x']
        performance = self.portfolio_annualized_performance(optimal_weights, mean_returns, cov_matrix)
        sharpe_ratio = (performance[0] - self.risk_free_rate) / performance[1]
        
        return optimal_weights, {
            'Return': performance[0],
            'Volatility': performance[1],
            'Sharpe Ratio': sharpe_ratio
        }
    
    def efficient_frontier(self, mean_returns, cov_matrix, returns_range):
        """
        Calculate the efficient frontier.
        
        Parameters:
        -----------
        mean_returns : Series
            Mean returns for each asset
        cov_matrix : DataFrame
            Covariance matrix of returns
        returns_range : array
            Range of target returns
            
        Returns:
        --------
        tuple
            (efficient_volatilities, target_returns)
        """
        efficient_volatilities = []
        
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        
        for target_return in returns_range:
            constraints = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: self.portfolio_annualized_performance(x, mean_returns, cov_matrix)[0] - target_return}
            )
            bounds = tuple((0, 1) for asset in range(num_assets))
            
            initial_guess = np.array([1/num_assets] * num_assets)
            
            result = sco.minimize(self.portfolio_volatility, initial_guess,
                                 args=args, method='SLSQP', bounds=bounds,
                                 constraints=constraints)
            
            efficient_volatilities.append(result['fun'])
        
        return efficient_volatilities, returns_range
    
    def optimize_portfolio(self, tickers=None, n_stocks=20, period='1Y'):
        """
        Optimize a portfolio using the selected stocks.
        
        Parameters:
        -----------
        tickers : list
            List of stock tickers to include in the portfolio
        n_stocks : int
            Number of stocks to select if tickers is None
        period : str
            Time period for analysis ('1Y', '2Y', '5Y', 'All')
            
        Returns:
        --------
        dict
            Dictionary of optimization results
        """
        if self.returns is None:
            print("Returns data not loaded")
            return None
        
        # Select stocks if not provided
        if tickers is None:
            tickers = self.select_stocks(n_stocks=n_stocks, period=period)
        
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
        
        filtered_returns = self.returns[tickers]
        filtered_returns = filtered_returns[(filtered_returns.index >= start_date) & (filtered_returns.index <= end_date)]
        
        # Calculate mean returns and covariance matrix
        mean_returns = filtered_returns.mean()
        cov_matrix = filtered_returns.cov()
        
        # Find the maximum Sharpe ratio portfolio
        max_sharpe_weights, max_sharpe_performance = self.max_sharpe_ratio(mean_returns, cov_matrix, self.risk_free_rate)
        
        # Find the minimum volatility portfolio
        min_vol_weights, min_vol_performance = self.min_volatility(mean_returns, cov_matrix)
        
        # Calculate the efficient frontier
        target_returns = np.linspace(min_vol_performance['Return'], max_sharpe_performance['Return'] * 1.2, 50)
        efficient_volatilities, target_returns = self.efficient_frontier(mean_returns, cov_matrix, target_returns)
        
        # Create a DataFrame with the portfolio weights
        max_sharpe_portfolio = pd.DataFrame({
            'Stock': tickers,
            'Weight': max_sharpe_weights
        })
        max_sharpe_portfolio = max_sharpe_portfolio.sort_values('Weight', ascending=False)
        
        min_vol_portfolio = pd.DataFrame({
            'Stock': tickers,
            'Weight': min_vol_weights
        })
        min_vol_portfolio = min_vol_portfolio.sort_values('Weight', ascending=False)
        
        # Save results
        results = {
            'tickers': tickers,
            'period': period,
            'max_sharpe_portfolio': max_sharpe_portfolio,
            'max_sharpe_performance': max_sharpe_performance,
            'min_vol_portfolio': min_vol_portfolio,
            'min_vol_performance': min_vol_performance,
            'efficient_frontier': {
                'volatilities': efficient_volatilities,
                'returns': target_returns
            }
        }
        
        # Save to CSV
        max_sharpe_portfolio.to_csv(os.path.join(self.results_dir, f"max_sharpe_portfolio_{period}.csv"), index=False)
        min_vol_portfolio.to_csv(os.path.join(self.results_dir, f"min_vol_portfolio_{period}.csv"), index=False)
        
        # Plot the efficient frontier
        self.plot_efficient_frontier(results)
        
        # Plot the portfolio weights
        self.plot_portfolio_weights(results)
        
        return results
    
    def plot_efficient_frontier(self, results):
        """
        Plot the efficient frontier.
        
        Parameters:
        -----------
        results : dict
            Dictionary of optimization results
        """
        period = results['period']
        efficient_volatilities = results['efficient_frontier']['volatilities']
        target_returns = results['efficient_frontier']['returns']
        
        max_sharpe_performance = results['max_sharpe_performance']
        min_vol_performance = results['min_vol_performance']
        
        plt.figure(figsize=(12, 8))
        
        # Plot the efficient frontier
        plt.plot(efficient_volatilities, target_returns, 'b-', linewidth=2, label='Efficient Frontier')
        
        # Plot the maximum Sharpe ratio portfolio
        plt.scatter(max_sharpe_performance['Volatility'], max_sharpe_performance['Return'],
                   marker='*', color='r', s=300, label='Maximum Sharpe Ratio')
        
        # Plot the minimum volatility portfolio
        plt.scatter(min_vol_performance['Volatility'], min_vol_performance['Return'],
                   marker='o', color='g', s=200, label='Minimum Volatility')
        
        # Add labels and title
        plt.title(f'Efficient Frontier ({period})')
        plt.xlabel('Annualized Volatility')
        plt.ylabel('Annualized Return')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save plot
        output_file = os.path.join(self.visualizations_dir, f"efficient_frontier_{period}.png")
        plt.savefig(output_file, dpi=300)
        print(f"Efficient frontier plot saved to {output_file}")
        
        plt.close()
    
    def plot_portfolio_weights(self, results):
        """
        Plot the portfolio weights.
        
        Parameters:
        -----------
        results : dict
            Dictionary of optimization results
        """
        period = results['period']
        max_sharpe_portfolio = results['max_sharpe_portfolio']
        min_vol_portfolio = results['min_vol_portfolio']
        
        # Filter to include only stocks with weights > 1%
        max_sharpe_filtered = max_sharpe_portfolio[max_sharpe_portfolio['Weight'] > 0.01]
        min_vol_filtered = min_vol_portfolio[min_vol_portfolio['Weight'] > 0.01]
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Plot maximum Sharpe ratio portfolio weights
        max_sharpe_filtered.plot.pie(y='Weight', labels=max_sharpe_filtered['Stock'], autopct='%1.1f%%',
                                   ax=ax1, startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        ax1.set_title(f'Maximum Sharpe Ratio Portfolio Weights ({period})')
        ax1.set_ylabel('')
        
        # Plot minimum volatility portfolio weights
        min_vol_filtered.plot.pie(y='Weight', labels=min_vol_filtered['Stock'], autopct='%1.1f%%',
                                ax=ax2, startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        ax2.set_title(f'Minimum Volatility Portfolio Weights ({period})')
        ax2.set_ylabel('')
        
        plt.tight_layout()
        
        # Save plot
        output_file = os.path.join(self.visualizations_dir, f"portfolio_weights_{period}.png")
        plt.savefig(output_file, dpi=300)
        print(f"Portfolio weights plot saved to {output_file}")
        
        plt.close()
    
    def run_optimization(self):
        """
        Run portfolio optimization for different time periods.
        """
        print("\n=== Running Portfolio Optimization ===")
        
        # Optimize portfolios for different time periods
        for period in ['1Y', '2Y', 'All']:
            print(f"\nOptimizing portfolio for {period}:")
            results = self.optimize_portfolio(period=period, n_stocks=20)
            
            if results:
                print(f"\nMaximum Sharpe Ratio Portfolio ({period}):")
                print(f"Expected Return: {results['max_sharpe_performance']['Return']:.2%}")
                print(f"Expected Volatility: {results['max_sharpe_performance']['Volatility']:.2%}")
                print(f"Sharpe Ratio: {results['max_sharpe_performance']['Sharpe Ratio']:.4f}")
                
                print(f"\nMinimum Volatility Portfolio ({period}):")
                print(f"Expected Return: {results['min_vol_performance']['Return']:.2%}")
                print(f"Expected Volatility: {results['min_vol_performance']['Volatility']:.2%}")
                print(f"Sharpe Ratio: {results['min_vol_performance']['Sharpe Ratio']:.4f}")
        
        print("\nPortfolio optimization complete!")

if __name__ == "__main__":
    optimizer = PortfolioOptimizer()
    optimizer.run_optimization() 