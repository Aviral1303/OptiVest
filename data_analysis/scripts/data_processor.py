import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob
from typing import Dict, List, Optional, Union, Tuple
import warnings
import pickle

class DataProcessor:
    """
    A class to process and organize financial data into structured DataFrames.
    """
    
    def __init__(self, base_dir: str = None):
        """
        Initialize the DataProcessor.
        
        Args:
            base_dir (str): Base directory for the project
        """
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.data_dir = os.path.join(base_dir, "data")
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        
        # Create necessary directories
        os.makedirs(self.processed_dir, exist_ok=True)
        
        print(f"Processed data will be saved to: {self.processed_dir}")
    
    def create_price_matrix(
        self, 
        field: str = 'Close', 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fill_method: str = 'ffill',
        min_pct_data: float = 0.80,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Create a price matrix with stocks as columns and dates as index.
        
        Args:
            field (str): Price field to use ('Open', 'High', 'Low', 'Close')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            fill_method (str): Method to fill missing values ('ffill', 'bfill', 'linear', None)
            min_pct_data (float): Minimum percentage of data required for a stock to be included
            save (bool): Whether to save the DataFrame to a CSV file
            
        Returns:
            pd.DataFrame: Price matrix with dates as index and stocks as columns
        """
        # Find all CSV files in the raw directory
        csv_files = glob.glob(os.path.join(self.raw_dir, "*_1d.csv"))
        
        if not csv_files:
            print("No CSV files found in the raw directory.")
            return pd.DataFrame()
        
        print(f"Found {len(csv_files)} CSV files to process")
        
        # Dictionary to store data for each symbol
        data_dict = {}
        skipped_files = 0
        
        # Process each CSV file
        for file_path in csv_files:
            try:
                # Extract symbol from filename
                symbol = os.path.basename(file_path).split('_')[0]
                
                # Skip market indices and other non-stock symbols
                if symbol.startswith('^') or symbol in ['SPY', 'VOO', 'QQQ']:
                    continue
                
                # Read the CSV file
                df = pd.read_csv(file_path)
                
                # Convert the Date column to datetime and set as index
                df['Date'] = pd.to_datetime(df['Date'], utc=True)
                df.set_index('Date', inplace=True)
                
                # Check if the required field exists
                if field not in df.columns:
                    skipped_files += 1
                    continue
                
                # Extract the specified price field
                data_dict[symbol] = df[field]
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                skipped_files += 1
                continue
        
        print(f"Skipped {skipped_files} files due to missing data or errors")
        
        if not data_dict:
            print("No valid data found in any of the CSV files.")
            return pd.DataFrame()
        
        # Create a DataFrame from the dictionary
        price_df = pd.DataFrame(data_dict)
        
        # Filter by date range if specified
        if start_date:
            price_df = price_df[price_df.index >= start_date]
        if end_date:
            price_df = price_df[price_df.index <= end_date]
            
        # Calculate percentage of non-NaN data for each column
        data_pct = price_df.count() / len(price_df)
        
        # Filter out columns with insufficient data
        columns_to_keep = data_pct[data_pct >= min_pct_data].index.tolist()
        price_df = price_df[columns_to_keep]
        
        print(f"Retained {len(columns_to_keep)} stocks after filtering for data completeness")
        
        # Handle missing values
        if fill_method:
            if fill_method in ['ffill', 'bfill']:
                if fill_method == 'ffill':
                    price_df = price_df.ffill()
                else:
                    price_df = price_df.bfill()
            elif fill_method == 'linear':
                price_df = price_df.interpolate(method='linear')
                
            # Forward fill any remaining NaNs at the beginning
            price_df = price_df.ffill()
            # Backward fill any remaining NaNs at the end
            price_df = price_df.bfill()
        
        # Check for any remaining NaNs
        if price_df.isna().any().any():
            warnings.warn(f"Warning: DataFrame still contains {price_df.isna().sum().sum()} NaN values")
        
        # Save to CSV if requested
        if save:
            output_path = os.path.join(self.processed_dir, f"price_matrix_{field.lower().replace(' ', '_')}.csv")
            price_df.to_csv(output_path)
            
            # Also save as a pickled DataFrame for faster loading
            pickle_path = os.path.join(self.processed_dir, f"price_matrix_{field.lower().replace(' ', '_')}.pkl")
            price_df.to_pickle(pickle_path)
            
            print(f"Saved price matrix to {output_path} and {pickle_path}")
        
        return price_df
    
    def create_returns_matrix(
        self,
        price_matrix: Optional[pd.DataFrame] = None,
        field: str = 'Close',
        period: str = 'daily',
        log_returns: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Create a returns matrix from price data.
        
        Args:
            price_matrix (pd.DataFrame): Optional pre-loaded price matrix
            field (str): Price field to use if price_matrix not provided
            period (str): Return calculation period ('daily', 'weekly', 'monthly')
            log_returns (bool): Whether to calculate log returns instead of simple returns
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            save (bool): Whether to save the DataFrame to a CSV file
            
        Returns:
            pd.DataFrame: Returns matrix with dates as index and stocks as columns
        """
        # Load price matrix if not provided
        if price_matrix is None:
            price_matrix = self.create_price_matrix(
                field=field,
                start_date=start_date,
                end_date=end_date,
                save=False
            )
        
        if price_matrix.empty:
            print("No price data available to calculate returns.")
            return pd.DataFrame()
        
        # Resample based on period if needed
        if period == 'weekly':
            price_matrix = price_matrix.resample('W').last()
        elif period == 'monthly':
            price_matrix = price_matrix.resample('M').last()
        
        # Calculate returns
        if log_returns:
            returns_df = np.log(price_matrix) - np.log(price_matrix.shift(1))
        else:
            returns_df = price_matrix.pct_change()
        
        # Drop the first row with NaN values
        returns_df = returns_df.dropna(how='all')
        
        # Save to CSV if requested
        if save:
            return_type = 'log' if log_returns else 'simple'
            output_path = os.path.join(
                self.processed_dir, 
                f"{period}_{return_type}_returns.csv"
            )
            returns_df.to_csv(output_path)
            
            # Also save as a pickled DataFrame for faster loading
            pickle_path = os.path.join(
                self.processed_dir, 
                f"{period}_{return_type}_returns.pkl"
            )
            returns_df.to_pickle(pickle_path)
            
            print(f"Saved returns matrix to {output_path} and {pickle_path}")
        
        return returns_df
    
    def create_market_data(
        self,
        market_symbols: List[str] = ['SPY', '^GSPC'],
        risk_free_rate_symbol: str = '^IRX',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        save: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Create market data DataFrame with market indices and risk-free rate.
        
        Args:
            market_symbols (List[str]): List of market index symbols
            risk_free_rate_symbol (str): Symbol for risk-free rate
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            save (bool): Whether to save the DataFrame to a CSV file
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with market price and returns DataFrames
        """
        # Check if market data files exist in raw directory
        market_files = []
        for symbol in market_symbols + [risk_free_rate_symbol]:
            file_path = os.path.join(self.raw_dir, f"{symbol}_1d.csv")
            if os.path.exists(file_path):
                market_files.append((symbol, file_path))
        
        if not market_files:
            print("No market data files found. Please download market data first.")
            return {}
        
        # Dictionary to store market data
        market_prices = {}
        
        # Process each market file
        for symbol, file_path in market_files:
            try:
                df = pd.read_csv(file_path)
                
                # Convert the Date column to datetime and set as index
                df['Date'] = pd.to_datetime(df['Date'], utc=True)
                df.set_index('Date', inplace=True)
                
                if 'Close' in df.columns:
                    market_prices[symbol] = df['Close']
                else:
                    print(f"Warning: 'Close' column not found in {symbol} data. Skipping.")
            except Exception as e:
                print(f"Error processing market data for {symbol}: {str(e)}")
        
        # Create market price DataFrame
        market_price_df = pd.DataFrame(market_prices)
        
        # Filter by date range if specified
        if start_date:
            market_price_df = market_price_df[market_price_df.index >= start_date]
        if end_date:
            market_price_df = market_price_df[market_price_df.index <= end_date]
        
        # Handle missing values
        market_price_df = market_price_df.ffill().bfill()
        
        # Calculate returns
        market_returns_df = market_price_df.pct_change().dropna(how='all')
        
        # Annualize risk-free rate if available
        if risk_free_rate_symbol in market_price_df.columns:
            # Treasury yields are in percentage, so divide by 100
            market_returns_df[f"{risk_free_rate_symbol}_daily"] = market_price_df[risk_free_rate_symbol] / 100 / 252
        
        # Save to CSV if requested
        if save and not market_price_df.empty:
            price_path = os.path.join(self.processed_dir, "market_prices.csv")
            market_price_df.to_csv(price_path)
            
            returns_path = os.path.join(self.processed_dir, "market_returns.csv")
            market_returns_df.to_csv(returns_path)
            
            print(f"Saved market data to {price_path} and {returns_path}")
        
        return {
            'prices': market_price_df,
            'returns': market_returns_df
        }

if __name__ == "__main__":
    # Example usage
    processor = DataProcessor()
    
    # Create price matrix with close prices
    price_matrix = processor.create_price_matrix(
        field='Close',
        fill_method='ffill',
        min_pct_data=0.80  # Require at least 80% of data points
    )
    
    # Create daily returns matrix
    daily_returns = processor.create_returns_matrix(
        price_matrix=price_matrix,
        period='daily',
        log_returns=False
    )
    
    # Create weekly returns matrix
    weekly_returns = processor.create_returns_matrix(
        price_matrix=price_matrix,
        period='weekly',
        log_returns=False
    )
    
    # Create monthly returns matrix
    monthly_returns = processor.create_returns_matrix(
        price_matrix=price_matrix,
        period='monthly',
        log_returns=False
    )
    
    # Create market data
    market_data = processor.create_market_data()
    
    print("Data processing complete!") 