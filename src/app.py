import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set up a clean, wide layout
st.set_page_config(page_title="pricing simulator", layout="wide", initial_sidebar_state="expanded")

# keep the ui light and minimal by reducing top padding
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("b2b dynamic pricing simulator")
st.markdown("adjust the market conditions and customer profile to see the algorithm recalculate optimal margins in real-time.")

# sidebar for the core inputs
with st.sidebar:
    st.header("market & customer inputs")
    
    order_value = st.number_input("order value (pkr)", min_value=1000, value=50000, step=1000)
    distance = st.slider("delivery distance (km)", 1, 50, 15)
    fuel_price = st.slider("fuel price (pkr/l)", 200, 350, 266)
    
    st.divider()
    
    credit_score = st.slider("retailer credit score (1-100)", 1, 100, 40)
    loyalty = st.slider("retailer base loyalty (0.1 - 1.0)", 0.1, 1.0, 0.6, 0.05)
    
    st.divider()
    
    crisis_active = st.toggle("hormuz blockage active (adds risk)", value=False)

# the core operations research math
base_cost = order_value * 0.8
logistics_cost = (distance / 5.0) * fuel_price
total_cost = base_cost + logistics_cost

default_prob = max(0.01, (100 - credit_score) / 200.0)
if crisis_active:
    default_prob += 0.05

sensitivity = 6.0 - (loyalty * 3.5)

# simulate 100 different margin points instantly
margins = np.linspace(0.01, 0.60, 100)
prices = total_cost * (1 + margins)
p_accept = loyalty * np.exp(-sensitivity * margins)
expected_profits = (prices - total_cost) * p_accept * (1 - default_prob)

# find the peak
best_idx = np.argmax(expected_profits)
best_margin = margins[best_idx]
best_price = prices[best_idx]
best_profit = expected_profits[best_idx]

# main dashboard area with clean metric cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("total cost", f"₨ {total_cost:,.0f}")
col2.metric("default risk", f"{default_prob * 100:.1f}%")
col3.metric("optimal target price", f"₨ {best_price:,.0f}")
col4.metric("optimal margin", f"{best_margin * 100:.1f}%")

st.divider()

# build a clean, light-themed visualization
fig, ax = plt.subplots(figsize=(10, 4))

# plot the curve
ax.plot(margins * 100, expected_profits, color="#2e86c1", linewidth=2.5, label="expected profit curve")

# highlight the exact peak so it feels like a simulation
ax.scatter([best_margin * 100], [best_profit], color="#e74c3c", s=100, zorder=5)
ax.axvline(x=best_margin * 100, color="#e74c3c", linestyle="--", alpha=0.5, label=f"peak margin: {best_margin*100:.1f}%")

# clean up the chart aesthetics for a precise, professional look
ax.set_title("profit optimization curve (live)", fontsize=12, pad=10, loc="left")
ax.set_xlabel("profit margin (%)")
ax.set_ylabel("expected profit (pkr)")
ax.grid(True, linestyle=":", alpha=0.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend()

# render the plot in the app
st.pyplot(fig)
