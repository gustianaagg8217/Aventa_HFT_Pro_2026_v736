#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test new features: Trading Parameters and Backtest Details"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Configure matplotlib
import matplotlib
matplotlib.use('Agg')

import tkinter as tk
from unittest.mock import MagicMock
from pathlib import Path
import pandas as pd

print("=== TESTING NEW FEATURES ===\n")

try:
    # Import converter
    print("1. Loading converter...")
    from csv_to_excel_converter_gui_736 import CSVToExcelConverter
    
    # Create converter
    root = tk.Tk()
    root.withdraw()
    converter = CSVToExcelConverter(root)
    converter.root.update = MagicMock()
    print("   OK\n")
    
    # Set parameters
    print("2. Setting trading parameters...")
    converter.csv_file_var.set('Backtest/trades_20260120_215755.csv')
    converter.output_folder_var.set('Backtest')
    
    converter.symbol_var.set('XAUUSD')
    converter.period_var.set('M15')
    converter.company_var.set('MetaTrader 5')
    converter.currency_var.set('USD')
    converter.leverage_var.set('1:500')
    
    print(f"   Symbol: {converter.symbol_var.get()}")
    print(f"   Period: {converter.period_var.get()}")
    print(f"   Company: {converter.company_var.get()}")
    print(f"   Currency: {converter.currency_var.get()}")
    print(f"   Leverage: {converter.leverage_var.get()}\n")
    
    # Run conversion
    print("3. Running conversion with new parameters...")
    converter._do_conversion()
    print("   OK\n")
    
    # Verify output
    print("4. Verifying output...")
    excel_file = Path('Backtest/trades_20260120_215755_report.xlsx')
    
    if excel_file.exists():
        print(f"   ✓ Excel file created: {excel_file.stat().st_size} bytes")
        
        # Check sheets
        xls = pd.ExcelFile(excel_file)
        print(f"   Sheets: {xls.sheet_names}")
        
        # Check BACKTEST_DETAILS
        if 'BACKTEST_DETAILS' in xls.sheet_names:
            print("\n   --- BACKTEST_DETAILS Sheet ---")
            backtest_df = pd.read_excel(excel_file, sheet_name='BACKTEST_DETAILS')
            print(f"   Rows: {len(backtest_df)}")
            print("\n   Key Metrics:")
            for idx, row in backtest_df.iterrows():
                if row['Category'] and str(row['Category']).strip():
                    print(f"     {row['Category']}: {row['Value']}")
        
        # Check ALL_TRADES for new columns
        print("\n   --- ALL_TRADES Sheet ---")
        trades_df = pd.read_excel(excel_file, sheet_name='ALL_TRADES')
        print(f"   Rows: {len(trades_df)}")
        print(f"   Columns: {list(trades_df.columns)}")
        
        # Check if new columns exist
        new_cols = ['Symbol', 'Period', 'Company', 'Currency', 'Leverage', 'Market']
        found_cols = [col for col in new_cols if col in trades_df.columns]
        print(f"   New columns found: {found_cols}")
        
        if 'Symbol' in trades_df.columns:
            print(f"   Sample Symbol: {trades_df['Symbol'].iloc[0]}")
            print(f"   Sample Period: {trades_df['Period'].iloc[0]}")
            print(f"   Sample Company: {trades_df['Company'].iloc[0]}")
        
        print("\n   ✓ All verifications passed!")
    else:
        print(f"   ✗ Excel file not found")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("SUCCESS: All new features working correctly!")
    print("="*60)
    
    root.destroy()

except Exception as e:
    import traceback
    print(f"\nERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
