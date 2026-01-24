#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test the CSV converter functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
from pathlib import Path

# Test reading CSV with skiprows
csv_file = Path('Backtest/trades_20260120_215755.csv')
print(f"Testing CSV file: {csv_file}")
print(f"File exists: {csv_file.exists()}")

if csv_file.exists():
    # Read CSV with skiprows=2 to skip header lines
    df = pd.read_csv(csv_file, skiprows=2)
    print(f'✓ CSV loaded successfully with skiprows=2')
    print(f'Rows: {len(df)}, Columns: {len(df.columns)}')
    print(f'Columns: {list(df.columns)}')
    
    # Test market detection
    print('\n--- Testing Market Detection ---')
    if 'Entry Time' in df.columns:
        def get_market(time_str):
            try:
                if isinstance(time_str, str):
                    time_parts = time_str.strip().split()
                    time_part = time_parts[-1]
                    time_values = time_part.split(':')
                    
                    if len(time_values) >= 1:
                        hour = int(time_values[0])
                    else:
                        return 'Unknown'
                else:
                    hour = int(time_str.hour) if hasattr(time_str, 'hour') else 0
                
                if 5 <= hour < 15:
                    return 'Asia'
                elif 15 <= hour < 20:
                    return 'London'
                elif hour >= 20 or hour < 5:
                    return 'New York'
                else:
                    return 'Unknown'
            except:
                return 'Unknown'
        
        df['Market'] = df['Entry Time'].apply(get_market)
        print(f'✓ Market column added')
        print(f'Market distribution:\n{df["Market"].value_counts()}')
    
    print('\nFirst few rows:')
    print(df[['Entry Time', 'Type', 'Profit', 'Market']].head(10))
    
    # Test metrics
    print('\n--- Testing Metrics Calculation ---')
    initial_balance = 0.0
    try:
        with open(csv_file, 'r') as f:
            first_line = f.readline().strip()
            if 'Initial Balance' in first_line:
                parts = first_line.split(',')
                if len(parts) > 1:
                    initial_balance = float(parts[1].strip())
    except Exception as e:
        print(f"⚠️ Could not extract initial balance: {e}")
    
    print(f'✓ Initial Balance: ${initial_balance:.2f}')
    
    total_trades = len(df)
    total_profit = df['Profit'].sum()
    closing_balance = initial_balance + total_profit
    
    win_count = len(df[df['Profit'] > 0])
    loss_count = len(df[df['Profit'] < 0])
    winrate = (win_count / total_trades * 100) if total_trades > 0 else 0
    
    print(f'Total Trades: {total_trades}')
    print(f'Total Profit: ${total_profit:.2f}')
    print(f'Closing Balance: ${closing_balance:.2f}')
    print(f'Win Trades: {win_count}')
    print(f'Loss Trades: {loss_count}')
    print(f'Winrate: {winrate:.2f}%')
else:
    print('❌ CSV file not found')
