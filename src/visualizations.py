import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_pricing_strategy():
    try:
        df = pd.read_csv('data/processed/optimized_transactions.csv')
    except FileNotFoundError:
        print("error: processed data not found. run the pricing model first.")
        return

    # set up the visual style
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    # create a scatter plot: loyalty vs margin, colored by default risk
    scatter = ax.scatter(
        df['base_loyalty'], 
        df['margin_pct'], 
        c=df['default_prob'], 
        cmap='coolwarm', 
        alpha=0.7,
        edgecolors='w',
        linewidth=0.5
    )

    # add labels and title
    ax.set_title('dynamic pricing engine: elasticity vs margin', fontsize=14, pad=15)
    ax.set_xlabel('retailer base loyalty (0 to 1)', fontsize=12)
    ax.set_ylabel('optimized profit margin (%)', fontsize=12)
    
    # add a colorbar to explain the dot colors
    cbar = plt.colorbar(scatter)
    cbar.set_label('probability of default (risk)', rotation=270, labelpad=15)

    # save the graph
    os.makedirs('visualizations', exist_ok=True)
    plt.savefig('visualizations/pricing_strategy_scatter.png', dpi=300, bbox_inches='tight')
    
    print("success. graph saved to visualizations/pricing_strategy_scatter.png")

if __name__ == "__main__":
    plot_pricing_strategy()