#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify Excel file structure"""

import pandas as pd
from pathlib import Path

excel_file = Path('Backtest/trades_20260120_215755_report.xlsx')
print(f"Checking Excel file: {excel_file}")
print(f"File exists: {excel_file.exists()}")
print(f"File size: {excel_file.stat().st_size} bytes")

if excel_file.exists():
    xls = pd.ExcelFile(excel_file)
    print(f"\n✓ Excel file loaded successfully")
    print(f"Sheet names: {xls.sheet_names}")
    
    # Check each sheet
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"\n--- Sheet: {sheet_name} ---")
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        if sheet_name == 'SUMMARY':
            print(df.to_string())
        elif len(df) > 0:
            print(f"Columns: {list(df.columns)}")
            print(f"First row:\n{df.iloc[0].to_dict()}")
        else:
            print(f"(Empty sheet with {len(df.columns)} columns)")
else:
    print('❌ Excel file not found')
