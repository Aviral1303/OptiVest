import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors

# Set style
plt.style.use('dark_background')
sns.set_style("darkgrid")

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
results_dir = os.path.join(base_dir, "results")
visualizations_dir = os.path.join(base_dir, "visualizations")

# Create directories if they don't exist
os.makedirs(visualizations_dir, exist_ok=True)

# Load basket data
basket_file = os.path.join(results_dir, "factor_baskets.csv")
baskets = pd.read_csv(basket_file)

# Print basket summary
print("Fama-French + Beta Model Stock Baskets Summary:")
for _, row in baskets.iterrows():
    print(f"Basket {row['BasketNumber']} - {row['Name']}:")
    print(f"  Risk Rating: {row['RiskDescription']} ({row['RiskRating']}/5)")
    print(f"  Return Rating: {row['ReturnDescription']} ({row['ReturnRating']}/5)")
    print(f"  Average Beta: {row['AvgBeta']:.3f}")
    print(f"  Expected Annual Return: {row['PredictedAnnualReturn']*100:.2f}%")
    print(f"  Expected Annual Volatility: {row['PredictedAnnualVolatility']*100:.2f}%")
    print(f"  Number of Stocks: {row['NumStocks']}")
    print()

# Create improved visualizations
print("Creating visualizations...")

# 1. Risk-Return Profile with Efficient Frontier Simulation
plt.figure(figsize=(14, 10))

# Setup colors
colors = plt.cm.viridis(np.linspace(0, 1, len(baskets)))

# Extract data
volatilities = baskets['PredictedAnnualVolatility'].values
returns = baskets['PredictedAnnualReturn'].values
basket_nums = baskets['BasketNumber'].values
names = baskets['Name'].values
risk_ratings = baskets['RiskRating'].values
return_ratings = baskets['ReturnRating'].values

# Create risk-return scatter plot
for i, (vol, ret, basket, name, color) in enumerate(
    zip(volatilities, returns, basket_nums, names, colors)):
    marker_size = 500 + risk_ratings[i] * 100  # Size based on risk
    plt.scatter(vol, ret, s=marker_size, color=color, alpha=0.7, 
                edgecolor='white', linewidth=2, zorder=5)
    
    # Add basket number and name as annotation
    plt.annotate(f"Basket {basket}\n{name}", 
                 xy=(vol, ret), xytext=(10, 10),
                 textcoords='offset points', 
                 fontsize=12, fontweight='bold',
                 color='white', 
                 bbox=dict(boxstyle="round,pad=0.3", fc=color, alpha=0.7))

# Generate a simulated efficient frontier for visualization
vol_range = np.linspace(0.05, 0.25, 100)
# Simplified model of expected returns based on volatility
frontier_returns = 0.05 + 0.3 * vol_range - 0.5 * vol_range**2

# Plot the frontier
plt.plot(vol_range, frontier_returns, 'w--', alpha=0.5, linewidth=2, label='Simulated Efficient Frontier')

# Add risk-free rate point
risk_free_rate = 0.05
plt.scatter(0, risk_free_rate, s=150, color='gold', marker='*', 
            edgecolor='white', linewidth=1, label='Risk-Free Rate (5%)')

# Add benchmark market return point (estimated)
market_return = 0.08
market_vol = 0.15
plt.scatter(market_vol, market_return, s=200, color='red', marker='d', 
            edgecolor='white', linewidth=1, label='Market (Est.)')

# Style the plot
plt.title('Risk-Return Profile of Fama-French + Beta Stock Baskets', fontsize=18, pad=20)
plt.xlabel('Expected Annual Volatility (Risk)', fontsize=14)
plt.ylabel('Expected Annual Return', fontsize=14)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='white', linestyle=':', alpha=0.3)
plt.legend(loc='upper left', fontsize=12)

# Format axes as percentages
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))

# Set reasonable axis limits
plt.xlim(0, max(volatilities) * 1.1)
plt.ylim(min(min(returns), 0) * 1.1, max(max(returns), market_return) * 1.2)

# Save the plot
output_file = os.path.join(visualizations_dir, "factor_baskets_risk_return_enhanced.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Risk-return plot saved to {output_file}")
plt.close()

# 2. Factor Exposures by Basket
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Factor exposures
factor_names = ['Beta', 'SMB', 'HML']
factor_cols = ['AvgBeta', 'AvgSMB', 'AvgHML']

for i, (factor, col) in enumerate(zip(factor_names, factor_cols)):
    ax = axes[i]
    sns.barplot(x='BasketNumber', y=col, data=baskets, palette='viridis', ax=ax)
    ax.set_title(f'Average {factor} Exposure by Basket', fontsize=14)
    ax.set_xlabel('Basket Number', fontsize=12)
    ax.set_ylabel(f'Average {factor}', fontsize=12)
    
    # Add value labels on bars
    for j, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., height + (0.1 if height >= 0 else -0.1),
                f'{height:.2f}', ha='center', fontsize=10, fontweight='bold')
    
    ax.grid(True, alpha=0.3)

plt.suptitle('Factor Exposures Across Stock Baskets', fontsize=18, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the factor exposures plot
output_file = os.path.join(visualizations_dir, "factor_baskets_exposures.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Factor exposures plot saved to {output_file}")
plt.close()

# 3. Risk-Return Rating Matrix
plt.figure(figsize=(12, 10))

# Create a risk-return grid
risk_levels = range(1, 6)
return_levels = range(1, 6)
grid = np.zeros((5, 5))

# Count baskets in each risk-return cell
for _, row in baskets.iterrows():
    risk_idx = int(row['RiskRating']) - 1
    return_idx = int(row['ReturnRating']) - 1
    grid[return_idx, risk_idx] = row['BasketNumber']

# Plot heatmap with text
ax = plt.gca()
im = ax.imshow(grid, cmap='viridis')

# Add text annotations
for i in range(5):
    for j in range(5):
        basket_num = int(grid[i, j])
        if basket_num > 0:
            ax.text(j, i, f"Basket {basket_num}", ha="center", va="center", 
                   color="white", fontsize=14, fontweight='bold')
        else:
            ax.text(j, i, "—", ha="center", va="center", 
                   color="gray", fontsize=14)

# Set tick labels
risk_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
return_labels = ['Low', 'Moderate-Low', 'Moderate', 'Moderate-High', 'High']

ax.set_xticks(np.arange(len(risk_labels)))
ax.set_yticks(np.arange(len(return_labels)))
ax.set_xticklabels(risk_labels)
ax.set_yticklabels(return_labels)

# Rotate x tick labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add labels and title
plt.title('Risk-Return Rating Matrix of Stock Baskets', fontsize=18, pad=20)
plt.xlabel('Risk Rating', fontsize=14)
plt.ylabel('Return Rating', fontsize=14)

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Basket Number', rotation=270, labelpad=20, fontsize=12)

# Save the rating matrix plot
output_file = os.path.join(visualizations_dir, "factor_baskets_rating_matrix.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Rating matrix plot saved to {output_file}")
plt.close()

print("All visualizations completed.") 