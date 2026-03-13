"""
Project: Trader Behavior & Market Sentiment Analysis
Author: [Your Name]
Objective: Analyze the relationship between Hyperliquid trader performance 
           and the Bitcoin Fear & Greed Index.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress minor aesthetic warnings for a cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

def run_analysis():
    # 1. DATA ACQUISITION
    try:
        trader_data = pd.read_csv('data/historical_data.csv')
        sentiment_data = pd.read_csv('data/fear_greed_index.csv')
        print("✅ Datasets loaded successfully.")
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find the data files. {e}")
        return

    # 2. DATA NORMALIZATION (Pre-processing)
    # We convert Hyperliquid Unix ms timestamps to readable dates
    trader_data['dt'] = pd.to_datetime(trader_data['Timestamp'], unit='ms')
    sentiment_data['dt'] = pd.to_datetime(sentiment_data['date'])

    # Standardizing the merge key to 'YYYY-MM-DD' strings to avoid Dtype mismatches
    trader_data['merge_date'] = trader_data['dt'].dt.strftime('%Y-%m-%d')
    sentiment_data['merge_date'] = sentiment_data['dt'].dt.strftime('%Y-%m-%d')

    # 3. DATA INTEGRATION (The Merge)
    # Using an inner join to focus only on days where we have both sentiment and trade data
    merged_df = pd.merge(trader_data, sentiment_data, on='merge_date', how='inner')

    # 4. FEATURE ENGINEERING & CLEANING
    # Ensure financial metrics are numeric for calculation
    cols_to_fix = ['Closed PnL', 'Size USD']
    for col in cols_to_fix:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

    # Aggregating metrics by market sentiment classification
    performance_metrics = merged_df.groupby('classification').agg({
        'Closed PnL': ['mean', 'sum', 'count'],
        'Size USD': 'mean'
    }).reset_index()

    # Flattening multi-index columns for cleaner referencing
    performance_metrics.columns = ['Sentiment', 'Avg_PnL', 'Total_PnL', 'Trade_Count', 'Avg_Size_USD']

    # 5. INSIGHT GENERATION
    print("\n--- Summary of Findings ---")
    print(performance_metrics.to_string(index=False))

    # Calculating correlation between the raw Index Value and PnL
    pnl_corr = merged_df['value'].corr(merged_df['Closed PnL'])
    print(f"\n💡 Hidden Pattern Insight: Correlation between Index Value and PnL is {pnl_corr:.4f}")

    # 6. DATA VISUALIZATION
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Using 'hue' and 'legend=False' to adhere to modern Seaborn standards
    plot = sns.barplot(
        data=performance_metrics, 
        x='Sentiment', 
        y='Avg_PnL', 
        hue='Sentiment', 
        palette='magma', 
        legend=False
    )

    plt.title('Trader Profitability vs. Market Sentiment', fontsize=14, pad=15)
    plt.axhline(0, color='black', linestyle='--', alpha=0.6) # Baseline for profit/loss
    plt.ylabel('Average Closed PnL (USD)', fontsize=12)
    plt.xlabel('Market Sentiment State', fontsize=12)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_analysis()
