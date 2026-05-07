\# Resilient B2B Pricing Engine



An empirical Industrial Organization (IO) model and dynamic pricing simulator for B2B wholesale. This project analyzes firm pricing behavior under macroeconomic uncertainty by modeling price elasticity, switching costs, and counterparty default risk.



\## Overview



The engine simulates a B2B environment experiencing external supply chain shocks. It calculates optimal profit margins for individual transactions to maximize expected profit based on core IO principles:

\* \*\*Price Elasticity and Market Power:\*\* Calculates how demand decays in response to markup changes.

\* \*\*Switching Costs:\*\* Uses retailer loyalty as a metric to quantify the buffer against price shocks, allowing the firm to extract surplus.

\* \*\*Firm Behavior under Uncertainty:\*\* Adjusts pricing strategies dynamically based on fluctuating logistical costs and shifting default probabilities during a crisis.



\## Project Architecture



\* `data\_generator.py`: Synthetic pipeline generating a retailer portfolio, macro environment conditions, and daily transactions.

\* `pricing\_model.py`: The pricing engine that calculates optimal price to charge for optimal profits.

\* `app.py`: Streamlit dashboard for real-time parameter adjustment and optimization visualization.

\* `visualizations.py`: Generates graphs to help visualize the trajectory of data.



\## Installation and Usage



1\. Clone the repository and navigate to the directory:

```bash

git clone \[https://github.com/qtbeeee/resilient-pricing-engine.git](https://github.com/qtbeeee/resilient-pricing-engine.git)

cd resilient-pricing-engine

