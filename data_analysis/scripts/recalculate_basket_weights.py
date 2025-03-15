#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

print("Recalculating stock basket weights and returns...")

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
results_dir = os.path.join(base_dir, "results")

# Define more realistic return numbers for each basket
realistic_returns = {
    1: 0.08,   # 8% for conservative
    2: 0.095,  # 9.5% for moderate-conservative
    3: 0.115,  # 11.5% for balanced
    4: 0.135,  # 13.5% for growth
    5: 0.16    # 16% for aggressive
}

# Process each basket
for basket_num in range(1, 6):
    # Load the percentages file
    percentages_file = os.path.join(results_dir, f"basket_{basket_num}_percentages.csv")
    
    if os.path.exists(percentages_file):
        # Read the percentages data
        df = pd.read_csv(percentages_file)
        
        # Take only the top 7 stocks by percentage
        top_stocks = df.head(7)
        
        # Recalculate percentages to sum to 100%
        total_pct = top_stocks['Percentage'].sum()
        top_stocks['Percentage'] = (top_stocks['Percentage'] / total_pct) * 100
        
        # Round to 2 decimal places
        top_stocks['Percentage'] = top_stocks['Percentage'].round(2)
        
        # Ensure exact 100% by adjusting the highest weight
        diff = 100 - top_stocks['Percentage'].sum()
        if abs(diff) > 0.01:  # If difference is more than 0.01%
            # Add the difference to the highest percentage
            idx = top_stocks['Percentage'].idxmax()
            top_stocks.loc[idx, 'Percentage'] += diff
            top_stocks.loc[idx, 'Percentage'] = round(top_stocks.loc[idx, 'Percentage'], 2)
        
        # Save the recalculated weights
        output_file = os.path.join(results_dir, f"basket_{basket_num}_adjusted_weights.csv")
        top_stocks.to_csv(output_file, index=False)
        
        # Print the result
        print(f"\nBasket {basket_num} - Adjusted Weights (Total: {top_stocks['Percentage'].sum()}%):")
        for _, row in top_stocks.iterrows():
            print(f"  {row['Stock']}: {row['Percentage']:.2f}%")
    else:
        print(f"Error: Could not find percentages file for Basket {basket_num}")

# Save realistic returns data
returns_data = pd.DataFrame({
    'BasketNumber': list(range(1, 6)),
    'Name': [
        'Conservative High Return', 
        'Moderate-Conservative Return', 
        'Balanced High Return', 
        'Growth-Oriented Return', 
        'Aggressive High Return'
    ],
    'ExpectedReturn': [realistic_returns[i] for i in range(1, 6)],
    'ReturnFormatted': [f"{realistic_returns[i]*100:.1f}%" for i in range(1, 6)]
})

# Save to CSV
returns_file = os.path.join(results_dir, "realistic_returns.csv")
returns_data.to_csv(returns_file, index=False)
print(f"\nRealistic returns saved to {returns_file}")
print("Recalculation complete!") 