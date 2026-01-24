#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug PDF conversion step by step"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(__file__))

# Configure matplotlib BEFORE importing
import matplotlib
matplotlib.use('Agg')

import pandas as pd
from fpdf import FPDF
from pathlib import Path

try:
    print("1. Loading Excel file...")
    excel_file = 'Backtest/trades_20260120_215755_report.xlsx'
    xls = pd.ExcelFile(excel_file)
    print(f"   Sheets: {xls.sheet_names}")
    
    # Create PDF
    print("2. Creating PDF...")
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    
    # Add sheets
    for sheet_name in xls.sheet_names:
        print(f"3. Processing sheet: {sheet_name}")
        
        # Read sheet data
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Replace NaN values with empty string
        df = df.fillna('')
        
        if len(df) == 0:
            print(f"   Skipping empty sheet")
            continue
        
        print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
        
        # Add new page
        pdf.add_page()
        
        # Add title
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Sheet: {sheet_name}", ln=True)
        pdf.ln(3)
        
        # Calculate column widths
        num_cols = len(df.columns)
        available_width = pdf.w - 20
        
        col_widths = []
        min_col_width = 15
        wide_columns = ['Entry Time', 'Exit Time', 'Reason', 'Entry Date', 'Exit Date', 'Metric']
        
        print(f"   Calculating column widths...")
        for col in df.columns:
            max_len = len(str(col))
            for val in df[col]:
                max_len = max(max_len, len(str(val)))
            
            estimated_width = max(min_col_width, max_len * 0.4 + 2)
            
            if col == 'Metric':
                estimated_width *= 2.0
            elif col in wide_columns:
                estimated_width *= 1.5
            
            col_widths.append(estimated_width)
        
        # Scale columns
        total_width = sum(col_widths)
        if total_width > available_width:
            scale_factor = available_width / total_width
            col_widths = [w * scale_factor for w in col_widths]
        
        # Set font for header
        print(f"   Creating table header...")
        pdf.set_font("Helvetica", 'B', 7)
        
        # Add header
        for col_idx, col in enumerate(df.columns):
            col_width = col_widths[col_idx]
            col_text = str(col)[:20]
            pdf.cell(col_width, 7, col_text, border=1, align='C')
        pdf.ln()
        
        # Set font for data
        pdf.set_font("Helvetica", '', 6)
        
        # Add rows
        print(f"   Adding {len(df)} data rows...")
        for idx, row in df.iterrows():
            for col_idx, col in enumerate(df.columns):
                col_width = col_widths[col_idx]
                value = str(row[col])
                
                if len(value) > 25:
                    value = value[:22] + "..."
                
                align = 'R' if isinstance(row[col], (int, float)) else 'L'
                pdf.cell(col_width, 5, value, border=1, align=align)
            pdf.ln()
        
        print(f"   OK Sheet completed")
    
    # Save PDF
    print("4. Saving PDF...")
    pdf_file = 'Backtest/trades_20260120_215755_debug.pdf'
    pdf.output(pdf_file)
    print(f"   OK PDF saved: {pdf_file}")
    
    # Check file
    if Path(pdf_file).exists():
        print(f"5. OK PDF file exists, size: {Path(pdf_file).stat().st_size} bytes")
    else:
        print(f"5. ERROR PDF file not found")

except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nDebug test completed!")
