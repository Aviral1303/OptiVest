#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
results_dir = os.path.join(base_dir, "results")

print("Calculating stock percentages for each basket...")

# Load factor loadings
loadings_file = os.path.join(results_dir, "factor_loadings.csv")
factor_loadings = pd.read_csv(loadings_file, index_col=0)

# Load basket information
basket_files = [f"high_return_basket_{i}_stocks.csv" for i in range(1, 6)]
baskets = {}

for i, basket_file in enumerate(basket_files, 1):
    file_path = os.path.join(results_dir, basket_file)
    basket_stocks = pd.read_csv(file_path)
    
    # Filter factor loadings to only include stocks in this basket
    basket_data = factor_loadings.loc[basket_stocks['Stock'].tolist()]
    
    # Calculate weights based on Alpha (higher Alpha = higher weight)
    if 'Alpha' in basket_data.columns:
        # Shift Alpha to ensure all values are positive (for weighting)
        min_alpha = basket_data['Alpha'].min()
        shifted_alpha = basket_data['Alpha'] - min_alpha + 0.01  # Add small constant to avoid zero weights
        
        # Calculate percentage based on Alpha
        total_alpha = shifted_alpha.sum()
        weights = shifted_alpha / total_alpha
        
        # Create DataFrame with stock symbols and percentages
        basket_percentages = pd.DataFrame({
            'Stock': basket_data.index,
            'Percentage': weights * 100  # Convert to percentage
        })
        
        # Sort by percentage (highest first)
        basket_percentages = basket_percentages.sort_values('Percentage', ascending=False)
        
        # Save to CSV
        output_file = os.path.join(results_dir, f"basket_{i}_percentages.csv")
        basket_percentages.to_csv(output_file, index=False)
        print(f"Basket {i} percentages saved to {output_file}")
        
        # Also store in dictionary for later use
        baskets[i] = basket_percentages
    else:
        print(f"Could not calculate percentages for Basket {i}: Alpha column not found")

# Print top 5 stocks in each basket
for basket_num, basket_data in baskets.items():
    print(f"\nBasket {basket_num} Top Stocks by Percentage:")
    top_stocks = basket_data.head(5)
    for _, row in top_stocks.iterrows():
        print(f"  {row['Stock']}: {row['Percentage']:.2f}%")

print("\nPercentage calculations complete!") 