#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final comprehensive test - Full end-to-end conversion"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Configure matplotlib non-GUI backend BEFORE importing
import matplotlib
matplotlib.use('Agg')

# Test imports
try:
    print("=== TESTING CSV TO EXCEL/PDF CONVERTER ===\n")
    
    print("1. Testing imports...")
    import tkinter as tk
    from unittest.mock import MagicMock
    from pathlib import Path
    import pandas as pd
    print("   OK All modules imported successfully\n")
    
    # Import converter
    print("2. Loading converter class...")
    from csv_to_excel_converter_gui_736 import CSVToExcelConverter
    print("   OK Converter loaded\n")
    
    # Create converter
    print("3. Creating converter instance...")
    root = tk.Tk()
    root.withdraw()
    converter = CSVToExcelConverter(root)
    converter.root.update = MagicMock()
    print("   OK Converter instance created\n")
    
    # Set paths
    print("4. Setting file paths...")
    csv_file = 'Backtest/trades_20260120_215755.csv'
    output_folder = 'Backtest'
    converter.csv_file_var.set(csv_file)
    converter.output_folder_var.set(output_folder)
    print(f"   CSV File: {csv_file}")
    print(f"   Output Folder: {output_folder}\n")
    
    # Test conversion
    print("5. Running Excel conversion...")
    converter._do_conversion()
    print("   OK Excel conversion completed\n")
    
    # Verify Excel output
    print("6. Verifying Excel output...")
    excel_file = Path('Backtest/trades_20260120_215755_report.xlsx')
    if excel_file.exists():
        print(f"   OK Excel file created: {excel_file.stat().st_size} bytes")
        
        # Check sheets
        xls = pd.ExcelFile(excel_file)
        print(f"   Sheets: {xls.sheet_names}")
        
        # Check summary
        summary_df = pd.read_excel(excel_file, sheet_name='SUMMARY')
        print(f"   Summary rows: {len(summary_df)}")
        print(f"   Initial Balance: ${summary_df[summary_df['Metric']=='Initial Balance ($)']['Value'].values[0]:.2f}")
        print(f"   Total Profit: ${summary_df[summary_df['Metric']=='Total Profit']['Value'].values[0]:.2f}")
        print(f"   Winrate: {summary_df[summary_df['Metric']=='Winrate (%)']['Value'].values[0]:.2f}%\n")
    else:
        print(f"   ERROR Excel file not found\n")
        sys.exit(1)
    
    # Test PDF conversion
    print("7. Running PDF conversion...")
    converter._do_pdf_conversion(str(excel_file), output_folder)
    print("   OK PDF conversion completed\n")
    
    # Verify PDF output
    print("8. Verifying PDF output...")
    pdf_file = Path('Backtest/trades_20260120_215755.pdf')
    if pdf_file.exists():
        print(f"   OK PDF file created: {pdf_file.stat().st_size} bytes\n")
    else:
        print(f"   ERROR PDF file not found\n")
        sys.exit(1)
    
    # Success
    print("=" * 50)
    print("SUCCESS: All tests passed!")
    print("=" * 50)
    print("\nGenerated files:")
    print(f"  - Excel: {excel_file}")
    print(f"  - PDF: {pdf_file}")
    
    root.destroy()
    
except Exception as e:
    import traceback
    print(f"\nERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
