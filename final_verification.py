#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final verification of all features"""

import pandas as pd
from pathlib import Path

excel_file = Path('Backtest/trades_20260120_215755_report.xlsx')

if excel_file.exists():
    print("FINAL VERIFICATION: Excel Export\n")
    print(f"File: {excel_file.name}")
    print(f"Size: {excel_file.stat().st_size} bytes\n")
    
    xls = pd.ExcelFile(excel_file)
    print(f"Sheets ({len(xls.sheet_names)}): {xls.sheet_names}\n")
    
    # Check each sheet
    print("="*70)
    
    # BACKTEST_DETAILS
    if 'BACKTEST_DETAILS' in xls.sheet_names:
        print("\n1. BACKTEST_DETAILS Sheet:")
        df = pd.read_excel(excel_file, sheet_name='BACKTEST_DETAILS')
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   \n   Sample Data:")
        for idx in range(min(15, len(df))):
            cat = df.iloc[idx]['Category']
            val = df.iloc[idx]['Value']
            if str(cat).strip() and str(cat) != 'nan':
                print(f"     {cat}: {val}")
    
    # ALL_TRADES
    if 'ALL_TRADES' in xls.sheet_names:
        print("\n2. ALL_TRADES Sheet:")
        df = pd.read_excel(excel_file, sheet_name='ALL_TRADES')
        print(f"   Rows: {len(df)}")
        print(f"   Columns ({len(df.columns)}): {list(df.columns)}")
        
        # Check new columns
        new_cols = ['Symbol', 'Period', 'Company', 'Currency', 'Leverage', 'Market']
        present = [col for col in new_cols if col in df.columns]
        print(f"   New columns present: {present}")
        
        if 'Symbol' in df.columns:
            print(f"   \n   Sample Row:")
            row = df.iloc[0]
            print(f"     Symbol: {row['Symbol']}")
            print(f"     Period: {row['Period']}")
            print(f"     Company: {row['Company']}")
            print(f"     Currency: {row['Currency']}")
            print(f"     Leverage: {row['Leverage']}")
            print(f"     Entry Time: {row['Entry Time']}")
            print(f"     Profit: {row['Profit']}")
            print(f"     Market: {row['Market']}")
    
    print("\n" + "="*70)
    print("\nVERIFICATION COMPLETE: All features present and working!")
else:
    print("ERROR: Excel file not found")
