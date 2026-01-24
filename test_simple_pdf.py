#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple PDF test to debug"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Configure matplotlib BEFORE importing
import matplotlib
matplotlib.use('Agg')

import traceback

try:
    print("1. Starting PDF test...")
    
    import pandas as pd
    print("2. pandas imported")
    
    from fpdf import FPDF
    print("3. fpdf2 imported")
    
    # Try simple PDF creation
    print("4. Creating simple PDF...")
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Test PDF", ln=True)
    
    test_file = 'Backtest/test_simple.pdf'
    pdf.output(test_file)
    print(f"5. PDF created: {test_file}")
    
    # Check if file exists
    from pathlib import Path
    if Path(test_file).exists():
        print(f"6. ✓ PDF file exists, size: {Path(test_file).stat().st_size} bytes")
    else:
        print(f"6. ❌ PDF file not found")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
