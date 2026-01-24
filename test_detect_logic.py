#!/usr/bin/env python3
"""
Test auto-detection logic without GUI
"""

import os

def detect_trading_params_test(csv_file):
    """
    Auto-detect trading parameters from CSV file filename
    """
    # Get filename without extension
    filename = os.path.basename(csv_file)
    filename_base = os.path.splitext(filename)[0]
    
    # Default values
    symbol = "Unknown"
    period = "Unknown"
    company = "Unknown"
    currency = "Unknown"
    leverage = "Unknown"
    
    # Try to parse filename (e.g., "XAUUSD_M15_trades_..." or "trades_20260120_215755")
    parts = filename_base.split('_')
    
    # Known symbol patterns (common forex/commodity pairs)
    common_symbols = ['XAUUSD', 'XAGUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 
                    'NZDUSD', 'USDCAD', 'USDCHF', 'EURGBP', 'EURJPY', 'GBPJPY',
                    'XAGEUR', 'EURAUD', 'CADCHF', 'AUDNZD']
    
    # Words to skip (common filename components)
    skip_words = ['trades', 'backtest', 'results', 'data', 'report', 'csv', 'export']
    
    # Check if filename contains known symbol (usually first part)
    for part in parts:
        part_upper = part.upper()
        if part_upper in common_symbols:
            symbol = part_upper
            break
    
    # If not found in common list, check if first part looks like a symbol
    # (3-6 letter code, mostly letters) and not a skip word
    if symbol == "Unknown" and parts and len(parts[0]) >= 3 and len(parts[0]) <= 8:
        first_part = parts[0]
        first_part_lower = first_part.lower()
        
        # Skip if it's a common word
        if first_part_lower not in skip_words:
            # Check if it looks like a symbol (mostly letters, at least 3 chars)
            letter_count = sum(1 for c in first_part if c.isalpha())
            if letter_count >= 3 and first_part[0].isalpha() and (first_part.isupper() or 
                (first_part[0].isupper() and first_part[1:].isupper())):
                symbol = first_part.upper()
    
    # Check if filename contains period (M1, M5, M15, H1, D1, etc.)
    period_patterns = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']
    for part in parts:
        if part.upper() in period_patterns:
            period = part.upper()
            break
    
    # Set defaults
    if currency == "Unknown":
        currency = "USD"
    
    if leverage == "Unknown":
        leverage = "1:500"
    
    return symbol, period, company, currency, leverage


print("\n=== TESTING AUTO-DETECTION ===\n")

test_cases = [
    ("trades_20260120_215755.csv", "Unknown", "Unknown"),  # No symbol/period in name
    ("EURUSD_H1_trades_20260120.csv", "EURUSD", "H1"),
    ("GBPUSD_M15_backtest.csv", "GBPUSD", "M15"),
    ("XAGEUR_D1_results.csv", "XAGEUR", "D1"),
    ("XAUUSD_M15_something.csv", "XAUUSD", "M15"),
]

all_pass = True
for filename, expected_symbol, expected_period in test_cases:
    symbol, period, company, currency, leverage = detect_trading_params_test(filename)
    passed = (symbol == expected_symbol and period == expected_period)
    status = "✓ PASS" if passed else "✗ FAIL"
    all_pass = all_pass and passed
    
    print(f"{status} {filename}")
    print(f"      Expected: {expected_symbol} {expected_period}")
    print(f"      Got:      {symbol} {period}")
    print()

if all_pass:
    print("✓ ALL TESTS PASSED")
else:
    print("✗ SOME TESTS FAILED")
