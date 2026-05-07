import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_retailers(n_retailers: int = 500) -> pd.DataFrame:
    """Generates a synthetic portfolio of B2B retailers with varying credit risks."""
    credit_scores = np.random.beta(a=2, b=5, size=n_retailers) * 100 
    
    retailers = pd.DataFrame({
        'retailer_id': [f'R_{str(i).zfill(4)}' for i in range(1, n_retailers + 1)],
        'credit_score': np.round(credit_scores, 2),
        'base_loyalty': np.round(np.random.uniform(0.3, 1.0, size=n_retailers), 2),
        'avg_basket_size_pkr': np.random.lognormal(mean=10, sigma=0.5, size=n_retailers) 
    })
    return retailers

def generate_macro_environment(days: int = 365, start_date: str = '2026-01-01') -> pd.DataFrame:
    """Simulates the 2026 Macro Environment, accounting for the Strait of Hormuz closure."""
    dates = [datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i) for i in range(days)]
    
    fuel_prices = [266.0] 
    hormuz_active = False
    
    for i in range(1, days):
        current_date = dates[i]
        
        # Simulate the late-Feb/March 2026 outbreak of the conflict
        if current_date.month == 3 and current_date.day == 1:
            hormuz_active = True
            
        # Crisis Policy: Shift from 15-day to Weekly (Friday) price reviews
        if current_date.weekday() == 4: 
            if hormuz_active:
                shock = np.random.choice(
                    [0, np.random.uniform(20, 60), np.random.uniform(-5, -10)], 
                    p=[0.20, 0.60, 0.20] 
                )
            else:
                shock = np.random.choice([0, np.random.uniform(5, 10), -5], p=[0.70, 0.20, 0.10])
                
            new_price = max(260.0, fuel_prices[-1] + shock)
            fuel_prices.append(round(new_price, 2))
        else:
            fuel_prices.append(fuel_prices[-1])

    # Inflation & Insurance Premium Spikes
    base_cost_index = []
    current_inflation = 100.0
    for i in range(days):
        if dates[i].month >= 3:
            current_inflation += np.random.uniform(0.5, 1.5) 
        else:
            current_inflation += 0.1
        base_cost_index.append(current_inflation)

    macro_df = pd.DataFrame({
        'date': dates,
        'fuel_price_pkr': fuel_prices,
        'replacement_cost_index': np.round(base_cost_index, 2),
        'hormuz_blockage_active': [1 if d.month >= 3 else 0 for d in dates]
    })
    return macro_df

def generate_transactions(retailers: pd.DataFrame, macro: pd.DataFrame) -> pd.DataFrame:
    """Combines retailers and macro data to simulate daily orders and default events."""
    transactions = []
    
    for _, day_data in macro.iterrows():
        fuel_penalty = max(0, (day_data['fuel_price_pkr'] - 270) / 1000)
        
        for _, retailer in retailers.iterrows():
            order_prob = 0.15 * retailer['base_loyalty'] - fuel_penalty
            
            if np.random.random() < order_prob:
                # Base default probability from credit score
                default_prob = max(0.01, (100 - retailer['credit_score']) / 200)
                
                # Macro Panic: Defaults spike by 5% when Hormuz is active due to cash flow crunch
                if day_data['hormuz_blockage_active'] == 1:
                    default_prob += 0.05 
                    
                is_default = np.random.random() < default_prob
                
                transactions.append({
                    'transaction_id': f"TXN_{len(transactions)+1}",
                    'date': day_data['date'],
                    'retailer_id': retailer['retailer_id'],
                    'order_value_pkr': round(retailer['avg_basket_size_pkr'] * np.random.uniform(0.8, 1.2), 2),
                    'delivery_distance_km': round(np.random.uniform(2.0, 25.0), 1),
                    'is_default': int(is_default)
                })
                
    return pd.DataFrame(transactions)

def main():
    """Executes the pipeline and saves the data."""
    print("Generating 2026 Crisis Market Data...")
    
    retailers = generate_retailers() 
    macro = generate_macro_environment()
    transactions = generate_transactions(retailers, macro)
    
    os.makedirs('data/raw', exist_ok=True)
    retailers.to_csv('data/raw/retailers.csv', index=False)
    macro.to_csv('data/raw/macro_environment.csv', index=False)
    transactions.to_csv('data/raw/transactions.csv', index=False)
    
    print(f"Success! Generated {len(transactions)} transactions.")
    print("Data saved to data/raw/")

if __name__ == "__main__":
    main()