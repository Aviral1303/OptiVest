import os
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from bs4 import BeautifulSoup

class DataCollector:
    """
    A class to collect financial data from various sources.
    """
    
    def __init__(self, base_dir: str = None):
        """
        Initialize the DataCollector.
        
        Args:
            base_dir (str): Base directory for the project
        """
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.data_dir = os.path.join(base_dir, "data")
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        
        # Create necessary directories
        for directory in [self.raw_dir, self.processed_dir]:
            os.makedirs(directory, exist_ok=True)
            
        print(f"Data will be saved to: {self.raw_dir}")
    
    def get_sp500_symbols(self) -> List[str]:
        """
        Fetch current S&P 500 symbols from Wikipedia.
        
        Returns:
            List[str]: List of S&P 500 stock symbols
        """
        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'wikitable'})
            
            symbols = []
            for row in table.find_all('tr')[1:]:
                symbol = row.find_all('td')[0].text.strip()
                symbols.append(symbol)
            
            # Save the symbols list
            symbols_file = os.path.join(self.raw_dir, "sp500_symbols.txt")
            with open(symbols_file, 'w') as f:
                f.write('\n'.join(symbols))
            
            print(f"Found {len(symbols)} S&P 500 symbols")
            return symbols
            
        except Exception as e:
            print(f"Error fetching S&P 500 symbols: {str(e)}")
            return []
    
    def fetch_stock_data(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d",
        batch_size: int = 50,
        delay: float = 1.0
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical stock data for given symbols.
        
        Args:
            symbols (List[str]): List of stock symbols
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            interval (str): Data interval ('1d', '1wk', '1mo')
            batch_size (int): Number of symbols to process before delay
            delay (float): Delay in seconds between batches
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames with stock data
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
        data = {}
        for i, symbol in enumerate(symbols):
            try:
                # Add delay between batches to avoid rate limiting
                if i > 0 and i % batch_size == 0:
                    print(f"Sleeping for {delay} seconds after processing {i} symbols...")
                    time.sleep(delay)
                
                ticker = yf.Ticker(symbol)
                df = ticker.history(start=start_date, end=end_date, interval=interval)
                
                if not df.empty:
                    data[symbol] = df
                    # Save to CSV
                    output_path = os.path.join(self.raw_dir, f"{symbol}_{interval}.csv")
                    df.to_csv(output_path)
                    print(f"Saved data for {symbol} to {output_path}")
                
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue
                
        return data
    
    def fetch_sp500_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical data for all S&P 500 stocks.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            interval (str): Data interval ('1d', '1wk', '1mo')
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames with stock data
        """
        # Get S&P 500 symbols
        symbols = self.get_sp500_symbols()
        
        if not symbols:
            print("Failed to fetch S&P 500 symbols. Aborting data collection.")
            return {}
        
        # Create a metadata file with download information
        metadata = {
            'download_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'start_date': start_date,
            'end_date': end_date,
            'interval': interval,
            'total_symbols': len(symbols)
        }
        
        metadata_path = os.path.join(self.raw_dir, "sp500_download_metadata.json")
        pd.DataFrame([metadata]).to_json(metadata_path, orient='records')
        
        # Fetch data for all symbols
        return self.fetch_stock_data(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )
        
    def fetch_market_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch market data including index and risk-free rate.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            interval (str): Data interval ('1d', '1wk', '1mo')
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames with market data
        """
        market_symbols = [
            '^GSPC',  # S&P 500 Index
            'SPY',    # S&P 500 ETF
            '^IRX',   # 13-week Treasury Bill (risk-free rate)
            '^TNX',   # 10-Year Treasury Yield
            'VOO',    # Vanguard S&P 500 ETF
            'QQQ',    # Nasdaq 100 ETF
            '^DJI',   # Dow Jones Industrial Average
            '^IXIC',  # Nasdaq Composite
            '^VIX',   # Volatility Index
        ]
        
        print(f"Fetching market data for {len(market_symbols)} symbols...")
        return self.fetch_stock_data(
            symbols=market_symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            batch_size=len(market_symbols)
        )

if __name__ == "__main__":
    # Example usage for S&P 500 data collection
    collector = DataCollector()
    
    # Fetch last 5 years of daily data
    start_date = (datetime.now() - timedelta(days=5*365)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Fetching S&P 500 data from {start_date} to {end_date}...")
    data = collector.fetch_sp500_data(
        start_date=start_date,
        end_date=end_date,
        interval="1d"
    ) 