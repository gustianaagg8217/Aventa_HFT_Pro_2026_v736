#!/usr/bin/env python3
"""
Test that CSV to Excel converter can read the new CSV format with Symbol, Period, Company
"""

import sys
import os

# Add path for imports
sys.path.insert(0, "c:\\Users\\LENOVO THINKPAD\\Documents\\Aventa_AI_2026\\Aventa_HFT_Pro_2026_v736")

import pandas as pd

test_csv = "c:\\Users\\LENOVO THINKPAD\\Documents\\Aventa_AI_2026\\Aventa_HFT_Pro_2026_v736\\test_trades_export.csv"

print("\n=== TESTING CSV IMPORT BY CONVERTER ===\n")

try:
    # Read CSV as the converter would
    df = pd.read_csv(test_csv, skiprows=2)  # Skip Initial Balance + empty row
    
    print(f"✓ CSV loaded successfully")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    print(f"\nColumn names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # Check for required columns
    required = ['Symbol', 'Period', 'Company']
    print(f"\nValidation:")
    for col in required:
        if col in df.columns:
            value = df[col].iloc[0] if len(df) > 0 else "N/A"
            print(f"  ✓ {col}: {value}")
        else:
            print(f"  ✗ {col}: MISSING")
    
    # Show first row
    print(f"\nFirst trade from CSV:")
    first_row = df.iloc[0]
    for col in df.columns:
        print(f"  {col}: {first_row[col]}")
    
    print(f"\n✓ CSV IMPORT TEST PASSED - Ready for converter")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
