#!/usr/bin/env python3
"""
Test auto-detection of trading parameters from CSV filename
"""

import sys
import os
import tkinter as tk
from csv_to_excel_converter_gui_736 import CSVToExcelConverter

# Test CSV files
test_files = [
    ("Backtest/trades_20260120_215755.csv", "XAUUSD", "M15", "Unknown"),
    ("Backtest/EURUSD_H1_trades.csv", "EURUSD", "H1", "Unknown"),
    ("Backtest/GBPUSD_D1_backtest.csv", "GBPUSD", "D1", "Unknown"),
]

print("\n=== TESTING AUTO-DETECTION ===\n")

# Create dummy root for testing
root = tk.Tk()
root.withdraw()  # Hide window

try:
    converter = CSVToExcelConverter(root)
    
    # Test 1: Actual file
    test_file = "Backtest/trades_20260120_215755.csv"
    if os.path.exists(test_file):
        print(f"Test 1: Detecting from {test_file}")
        converter.detect_trading_params(test_file)
        print(f"  Symbol:   {converter.symbol_var.get()}")
        print(f"  Period:   {converter.period_var.get()}")
        print(f"  Company:  {converter.company_var.get()}")
        print(f"  Currency: {converter.currency_var.get()}")
        print(f"  Leverage: {converter.leverage_var.get()}")
        print()
    
    # Test 2: Hypothetical filenames
    test_cases = [
        ("EURUSD_H1_trades_20260120.csv", "EURUSD", "H1"),
        ("GBPUSD_M15_backtest.csv", "GBPUSD", "M15"),
        ("XAGEUR_D1_results.csv", "XAGEUR", "D1"),
    ]
    
    for filename, expected_symbol, expected_period in test_cases:
        print(f"Test: {filename}")
        # Create temporary test file
        temp_file = f"temp_{filename}"
        with open(temp_file, 'w') as f:
            f.write("Initial Balance ($),1000\n")
            f.write("#,Entry Time,Exit Time\n")
        
        converter.detect_trading_params(temp_file)
        print(f"  Expected: {expected_symbol} {expected_period}")
        print(f"  Got:      {converter.symbol_var.get()} {converter.period_var.get()}")
        print(f"  ✓ PASS" if converter.symbol_var.get() == expected_symbol and converter.period_var.get() == expected_period else f"  ✗ FAIL")
        print()
        
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("✓ AUTO-DETECTION TESTS COMPLETE")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    root.destroy()
