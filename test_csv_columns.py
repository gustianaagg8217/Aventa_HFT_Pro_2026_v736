#!/usr/bin/env python3
"""
Test CSV export to verify Symbol, Period, Company columns are present
"""

import csv
import os

csv_file = "c:/Users/LENOVO THINKPAD/Documents/Aventa_AI_2026/Aventa_HFT_Pro_2026_v736/Backtest/trades_20260124_113010.csv"

if os.path.exists(csv_file):
    print(f"\n=== CSV EXPORT VERIFICATION ===\n")
    print(f"File: {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Skip first 2 rows (Initial Balance + empty)
        initial_balance = next(reader)
        empty_row = next(reader)
        
        # Get header
        header = next(reader)
        
        print(f"\nHeader columns ({len(header)} total):")
        for i, col in enumerate(header, 1):
            print(f"  {i}. {col}")
        
        # Check for required columns
        required_cols = ['Symbol', 'Period', 'Company']
        present_cols = [col for col in required_cols if col in header]
        missing_cols = [col for col in required_cols if col not in header]
        
        print(f"\n✓ Required columns present: {', '.join(present_cols)}")
        if missing_cols:
            print(f"✗ Missing columns: {', '.join(missing_cols)}")
        
        # Read first few trades
        print(f"\nFirst 3 trades:")
        for i, row in enumerate(reader):
            if i >= 3:
                break
            
            print(f"\nTrade {i+1}:")
            for j, col_name in enumerate(header):
                if j < len(row):
                    print(f"  {col_name}: {row[j]}")
    
    print(f"\n✓ CSV VERIFICATION COMPLETE")
else:
    print(f"✗ File not found: {csv_file}")
    print("\nSearching for recent CSV files...")
    backtest_dir = "c:/Users/LENOVO THINKPAD/Documents/Aventa_AI_2026/Aventa_HFT_Pro_2026_v736/Backtest"
    if os.path.exists(backtest_dir):
        csv_files = [f for f in os.listdir(backtest_dir) if f.endswith('.csv') and f.startswith('trades')]
        if csv_files:
            print(f"\nFound {len(csv_files)} trade CSV files:")
            for f in sorted(csv_files)[-3:]:
                print(f"  - {f}")
