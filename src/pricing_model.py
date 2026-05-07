import pandas as pd
import numpy as np
import os

def load_data():
    try:
        r = pd.read_csv('data/raw/retailers.csv')
        m = pd.read_csv('data/raw/macro_environment.csv')
        t = pd.read_csv('data/raw/transactions.csv')
        return r, m, t
    except FileNotFoundError:
        print("error: files missing. run the data generator first.")
        return None, None, None

def optimize_single_order(cost, default_prob, loyalty):
    # test profit margins from 1% to 60%
    margins = np.linspace(0.01, 0.60, 50)
    test_prices = cost * (1 + margins)
    
    # dynamic elasticity: loyal shops tolerate higher markups
    sensitivity = 6.0 - (loyalty * 3.5)
    p_accept = loyalty * np.exp(-sensitivity * margins)
    
    # expected profit formula
    expected_profits = (test_prices - cost) * p_accept * (1 - default_prob)
    
    # find the absolute peak
    best_idx = np.argmax(expected_profits)
    
    return pd.Series({
        'optimized_price': test_prices[best_idx],
        'expected_profit': expected_profits[best_idx],
        'prob_accept': p_accept[best_idx],
        'margin_pct': margins[best_idx] * 100
    })

def calculate_prices(t, r, m):
    print("running stochastic price optimization...")
    
    df = t.merge(r, on='retailer_id', how='left')
    df = df.merge(m, on='date', how='left')
    
    # base costs and inflation
    df['base_cost'] = (df['order_value_pkr'] * 0.8) * (df['replacement_cost_index'] / 100)
    df['logistics_cost'] = (df['delivery_distance_km'] / 5.0) * df['fuel_price_pkr']
    df['total_cost'] = df['base_cost'] + df['logistics_cost']
    
    # default risk with crisis penalty
    df['default_prob'] = np.where(
        df['hormuz_blockage_active'] == 1,
        np.maximum(0.01, (100 - df['credit_score']) / 200) + 0.05,
        np.maximum(0.01, (100 - df['credit_score']) / 200)
    )
    
    # run the optimizer row by row
    optimized_results = df.apply(
        lambda row: optimize_single_order(row['total_cost'], row['default_prob'], row['base_loyalty']), 
        axis=1
    )
    
    df = pd.concat([df, optimized_results], axis=1)
    return df

def main():
    r, m, t = load_data()
    
    if r is not None:
        priced_data = calculate_prices(t, r, m)
        
        os.makedirs('data/processed', exist_ok=True)
        priced_data.to_csv('data/processed/optimized_transactions.csv', index=False)
        
        print("\nsuccess. complex optimization complete.")
        
        cols_to_show = ['credit_score', 'base_loyalty', 'total_cost', 'optimized_price', 'margin_pct', 'prob_accept']
        print(priced_data[cols_to_show].head())

if __name__ == "__main__":
    main()