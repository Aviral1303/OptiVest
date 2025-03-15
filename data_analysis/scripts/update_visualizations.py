#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Updating visualizations to reflect new return ratings...")

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
vis_dir = os.path.join(base_dir, "visualizations")

# Create a DataFrame with the basket information
baskets = pd.DataFrame({
    'Basket': [1, 2, 3, 4, 5],
    'Name': [
        'Conservative High Return', 
        'Moderate-Conservative Return', 
        'Balanced High Return', 
        'Growth-Oriented Return', 
        'Aggressive High Return'
    ],
    'Risk_Rating': [1, 2, 3, 4, 5],
    'Risk_Name': ['Very Low', 'Low', 'Moderate', 'High', 'Very High'],
    'Return_Rating': [3, 3.5, 4, 4.5, 5],
    'Return_Name': ['Moderate', 'Moderate-High', 'High', 'Very High', 'Extremely High'],
    'Expected_Return': [8.0, 9.5, 11.5, 13.5, 16.0],
    'Beta': [0.52, 0.79, 1.00, 1.17, 1.53]
})

# Set style
plt.style.use('dark_background')
sns.set(style="darkgrid", palette="muted", color_codes=True)
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.family'] = 'sans-serif'

# Function to generate a risk-return matrix visualization
def create_risk_return_matrix():
    print("Generating new risk-return matrix...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9))
    
    # Create a grid for the ratings
    risk_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    return_labels = ['Very Low', 'Low', 'Moderate', 'Moderate-High', 'High', 'Very High', 'Extremely High']
    
    # Create a matrix to hold our values (all zeros initially)
    matrix = np.zeros((len(return_labels), len(risk_labels)))
    
    # Map risk and return ratings to matrix coordinates
    # Fill in our basket positions
    for _, basket in baskets.iterrows():
        risk_idx = int(basket['Risk_Rating']) - 1  # 0-indexed
        
        # Map return ratings to indices
        return_mapping = {
            1: 0,  # Very Low
            2: 1,  # Low
            3: 2,  # Moderate
            3.5: 3, # Moderate-High
            4: 4,   # High
            4.5: 5, # Very High
            5: 6    # Extremely High
        }
        return_idx = return_mapping.get(basket['Return_Rating'], 0)
        
        # Place the basket number in the matrix
        matrix[return_idx, risk_idx] = basket['Basket']
    
    # Create a heatmap
    cmap = plt.cm.get_cmap('coolwarm', 7)
    heatmap = sns.heatmap(
        matrix, 
        annot=True, 
        cmap=cmap, 
        cbar=False,
        xticklabels=risk_labels,
        yticklabels=return_labels,
        annot_kws={"size": 16, "weight": "bold"},
        fmt='.0f',
        linewidths=1,
        linecolor='gray'
    )
    
    # Hide cells with no baskets (0 values)
    for _, spine in heatmap.spines.items():
        spine.set_visible(True)
        spine.set_color('gray')
        
    # Remove annotations for cells with 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 0:
                text = heatmap.texts[i * matrix.shape[1] + j]
                text.set_text("")
    
    # Set axis labels and title
    plt.title('Risk-Return Rating Matrix', fontsize=20, pad=20)
    plt.xlabel('Risk Rating', fontsize=16, labelpad=10)
    plt.ylabel('Return Rating', fontsize=16, labelpad=10)
    
    # Add a custom legend
    legend_elements = []
    for idx, basket in baskets.iterrows():
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', 
                       label=f"Basket {basket['Basket']}: {basket['Name']}",
                       markerfacecolor=cmap(idx/5), markersize=10)
        )
    
    plt.legend(handles=legend_elements, loc='upper center', 
               bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    output_file = os.path.join(vis_dir, "updated_risk_return_matrix.png")
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    print(f"Saved new risk-return matrix to {output_file}")
    plt.close()

def create_return_chart():
    """Create a bar chart showing expected returns across baskets"""
    print("Generating expected returns chart...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create color map
    colors = ['#047857', '#0EA5E9', '#F59E0B', '#EC4899', '#DC2626']
    
    # Create bar chart
    bars = plt.bar(
        baskets['Name'], 
        baskets['Expected_Return'],
        color=colors,
        alpha=0.9
    )
    
    # Add return rating labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        rating = baskets.iloc[i]['Return_Rating']
        rating_name = baskets.iloc[i]['Return_Name']
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.5,
            f"{rating_name}\n({rating}/5)",
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )
    
    # Set chart title and labels
    plt.title('Expected Returns by Basket with Return Ratings', fontsize=18)
    plt.ylabel('Expected Annual Return (%)', fontsize=14)
    plt.ylim(0, 20)  # Set y-axis limit
    
    # Format x-axis
    plt.xticks(rotation=25, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add expected return values on bars
    for i, bar in enumerate(bars):
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height()/2,
            f"{baskets.iloc[i]['Expected_Return']}%",
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            color='black'
        )
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    output_file = os.path.join(vis_dir, "basket_return_ratings.png")
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    print(f"Saved return ratings chart to {output_file}")
    plt.close()

def create_risk_return_relationship():
    """Create a scatter plot showing the risk-return relationship"""
    print("Generating risk-return relationship chart...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create color map
    colors = ['#047857', '#0EA5E9', '#F59E0B', '#EC4899', '#DC2626']
    
    # Create scatter plot
    for i, basket in baskets.iterrows():
        plt.scatter(
            basket['Risk_Rating'],
            basket['Return_Rating'],
            s=300,
            color=colors[i],
            alpha=0.8,
            label=f"Basket {basket['Basket']}: {basket['Name']}"
        )
        
        # Add labels with expected returns
        plt.annotate(
            f"{basket['Expected_Return']}%",
            (basket['Risk_Rating'], basket['Return_Rating']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=12,
            fontweight='bold'
        )
    
    # Add a trend line
    z = np.polyfit(baskets['Risk_Rating'], baskets['Return_Rating'], 1)
    p = np.poly1d(z)
    plt.plot(baskets['Risk_Rating'], p(baskets['Risk_Rating']), 
             '--', color='gray', alpha=0.7)
    
    # Set chart title and labels
    plt.title('Risk vs. Return Rating Relationship', fontsize=18)
    plt.xlabel('Risk Rating', fontsize=14)
    plt.ylabel('Return Rating', fontsize=14)
    
    # Set axis range and ticks
    plt.xlim(0.5, 5.5)
    plt.ylim(2.5, 5.5)
    plt.xticks([1, 2, 3, 4, 5], ['Very Low', 'Low', 'Moderate', 'High', 'Very High'])
    plt.yticks([3, 3.5, 4, 4.5, 5], ['Moderate', 'Mod-High', 'High', 'Very High', 'Ext. High'])
    
    # Add grid
    plt.grid(alpha=0.3)
    
    # Add legend
    plt.legend(loc='lower right')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    output_file = os.path.join(vis_dir, "risk_return_relationship.png")
    plt.savefig(output_file, dpi=120, bbox_inches='tight')
    print(f"Saved risk-return relationship chart to {output_file}")
    plt.close()

# Generate all visualizations
create_risk_return_matrix()
create_return_chart()
create_risk_return_relationship()

print("Visualization updates complete!")
print("New files generated:")
print("1. updated_risk_return_matrix.png")
print("2. basket_return_ratings.png")
print("3. risk_return_relationship.png")
print("\nPlease update the HTML file to reference these new visualizations.") 