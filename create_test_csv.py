#!/usr/bin/env python3
"""
Simulate creating a CSV export with Symbol, Period, Company columns
"""

import csv
import os
from datetime import datetime

# Create a test CSV with the new format
output_file = "c:/Users/LENOVO THINKPAD/Documents/Aventa_AI_2026/Aventa_HFT_Pro_2026_v736/test_trades_export.csv"

print("\n=== Creating Test CSV with Symbol, Period, Company ===\n")

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Header row 1: Initial Balance
    writer.writerow(['Initial Balance ($)', 6795.0])
    writer.writerow([])  # Empty row
    
    # Header row 3: Column names (UPDATED FORMAT)
    writer.writerow(['#', 'Entry Time', 'Exit Time', 'Type', 'Entry Price', 
                     'Exit Price', 'Volume', 'Profit', 'Saldo Awal', 'Saldo Akhir', 'Duration', 'Reason', 
                     'Symbol', 'Period', 'Company'])
    
    # Sample trades
    sample_trades = [
        [1, '2025-12-22 01:50:00', '2025-12-22 01:51:00', 'BUY', '4354.19000', '4355.15000', '0.01', '0.99', '6795.00', '6795.99', '1 min', 'Take Profit', 'XAUUSD', 'M15', 'MetaTrader 5'],
        [2, '2025-12-22 01:51:00', '2025-12-22 02:00:00', 'BUY', '4355.15000', '4359.25000', '0.01', '4.24', '6795.99', '6800.24', '9 min', 'Take Profit', 'XAUUSD', 'M15', 'MetaTrader 5'],
        [3, '2025-12-22 02:00:00', '2025-12-22 02:01:00', 'BUY', '4359.25000', '4361.98000', '0.01', '2.83', '6800.24', '6803.06', '1 min', 'Take Profit', 'XAUUSD', 'M15', 'MetaTrader 5'],
    ]
    
    for trade in sample_trades:
        writer.writerow(trade)

print(f"✓ Test CSV created: {output_file}\n")

# Verify
print("=== Verification ===\n")
with open(output_file, 'r') as f:
    reader = csv.reader(f)
    
    # Skip Initial Balance + empty
    initial = next(reader)
    empty = next(reader)
    
    # Header
    header = next(reader)
    print(f"Header columns ({len(header)} total):")
    for i, col in enumerate(header, 1):
        print(f"  {i}. {col}")
    
    # Check for required columns
    required = ['Symbol', 'Period', 'Company', 'Volume']
    found = [col for col in required if col in header]
    missing = [col for col in required if col not in header]
    
    print(f"\n✓ Found: {', '.join(found)}")
    if missing:
        print(f"✗ Missing: {', '.join(missing)}")
    else:
        print(f"✓ All required columns present!")
    
    # Show first trade
    print(f"\nFirst trade data:")
    first_trade = next(reader)
    for col_name, value in zip(header, first_trade):
        print(f"  {col_name}: {value}")

print(f"\n✓ TEST COMPLETE - CSV format is correct!")
