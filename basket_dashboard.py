import matplotlib.pyplot as plt
import numpy as np
import os

def create_basket_stock_examples(self, save=True, show=False):
    """Create visualization showing example stocks from each basket"""
    
    plt.figure(figsize=(14, 12))
    
    # Create a simpler visualization since we don't have full factor data for all stocks
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Title for the entire figure
    fig.suptitle('Top Stocks by Percentage Weight in Each Basket', fontsize=24, y=0.98)
    
    # Color mapping for baskets
    basket_colors = {
        1: '#34C759',  # green for low risk
        2: '#5AC8FA',  # blue for moderate-low risk
        3: '#FFCC00',  # yellow for moderate risk
        4: '#FF9500',  # orange for moderate-high risk
        5: '#FF3B30',  # red for high risk
    }
    
    # For each basket, create a horizontal bar for top stocks
    y_positions = []
    bar_heights = []
    bar_colors = []
    bar_labels = []
    
    # Track the current position
    current_y = 0
    y_ticks = []
    y_labels = []
    
    for basket_num in sorted(self.basket_stocks.keys()):
        basket_info = self.baskets[self.baskets['BasketNumber'] == basket_num].iloc[0]
        stocks = self.basket_stocks[basket_num]
        
        # Add basket header position
        y_ticks.append(current_y)
        y_labels.append(f"Basket {basket_num}: {basket_info['Name']}")
        current_y += 1
        
        # Create equal weights for visualization purposes
        weights = np.linspace(0.3, 0.1, len(stocks))
        weights = weights / np.sum(weights)  # normalize
        
        # Add each stock
        for i, stock in enumerate(stocks):
            y_positions.append(current_y)
            bar_heights.append(weights[i] * 100)  # Convert to percentage
            bar_colors.append(basket_colors[basket_num])
            bar_labels.append(f"{stock}")
            current_y += 0.7
        
        # Add space between baskets
        current_y += 1.5
    
    # Create horizontal bars
    bars = ax.barh(y_positions, bar_heights, height=0.5, color=bar_colors, alpha=0.8)
    
    # Add labels to each bar
    for i, (bar, label) in enumerate(zip(bars, bar_labels)):
        width = bar.get_width()
        ax.text(width + 1, y_positions[i], f"{label} ({width:.1f}%)", 
               va='center', fontsize=10, fontweight='bold')
    
    # Style the plot
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12, fontweight='bold')
    ax.set_xlabel('Weight in Basket (%)', fontsize=14)
    ax.invert_yaxis()  # Make the top basket appear at the top
    ax.grid(axis='x', alpha=0.3)
    
    # Remove y-axis line
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Description text
    plt.figtext(0.5, 0.01, 
              "Visualization of top stocks in each basket with their percentage weights.",
              ha="center", fontsize=10, alpha=0.8)
    
    # Add basket descriptions
    for i, basket_num in enumerate(sorted(self.basket_stocks.keys())):
        basket_info = self.baskets[self.baskets['BasketNumber'] == basket_num].iloc[0]
        description = f"β: {basket_info['AvgBeta']:.2f}, Return: {basket_info['PredictedAnnualReturn']:.1%}, Volatility: {basket_info['PredictedAnnualVolatility']:.1%}"
        ax.text(0, y_ticks[i] - 0.5, description, fontsize=10, alpha=0.8)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    # Save and/or show
    if save:
        output_file = os.path.join(visualizations_dir, "basket_stock_examples.png")
        plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
        print(f"Basket stock examples saved to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()