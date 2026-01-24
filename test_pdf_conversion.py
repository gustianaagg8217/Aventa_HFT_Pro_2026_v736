#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test PDF conversion"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Configure matplotlib non-GUI backend BEFORE importing
import matplotlib
matplotlib.use('Agg')

# Import modules
from csv_to_excel_converter_gui_736 import CSVToExcelConverter
import tkinter as tk
from unittest.mock import MagicMock
from pathlib import Path

# Create minimal GUI for converter without showing GUI
root = tk.Tk()
root.withdraw()  # Hide window

# Create converter instance
converter = CSVToExcelConverter(root)

# Mock the GUI display methods so we don't show the window
converter.root.update = MagicMock()

# Set file paths
excel_file = 'Backtest/trades_20260120_215755_report.xlsx'
output_folder = 'Backtest'

# Test PDF conversion
print("Testing PDF conversion...")
print(f"Input Excel: {excel_file}")
print(f"Output folder: {output_folder}")

converter._do_pdf_conversion(excel_file, output_folder)

# Check if PDF was created
pdf_file = Path('Backtest/trades_20260120_215755.pdf')
if pdf_file.exists():
    print(f"\n✓ PDF file created successfully!")
    print(f"File size: {pdf_file.stat().st_size} bytes")
else:
    print(f"\n❌ PDF file not found")

print("PDF conversion test completed!")
root.destroy()
