# Trader Behavior Insights Assignment

## 🎯 Project Goal
To investigate how Bitcoin market sentiment (Fear/Greed Index) correlates with actual trading performance (PnL) on the Hyperliquid exchange.

## 🛠️ Implementation Details
- **Data Normalization:** Synced Unix millisecond timestamps with ISO date formats.
- **Handling Incompatibilities:** Resolved Dtype merge conflicts between DateTime objects and strings.
- **Visualization:** Created distribution plots to compare PnL across different sentiment states.

## 📈 Key Discovery
My analysis found that while **'Greed'** phases showed the highest average profit, **'Extreme Greed'** phases saw a performance drop-off, likely due to over-leveraged late entries. 
The correlation between the sentiment value and PnL was approximately **0.011**, suggesting that sentiment is a broad indicator rather than a direct predictor of individual trade success.
