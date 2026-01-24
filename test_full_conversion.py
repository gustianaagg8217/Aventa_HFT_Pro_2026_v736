#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test full Excel conversion without GUI"""

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

# Create minimal GUI for converter without showing GUI
root = tk.Tk()
root.withdraw()  # Hide window

# Create converter instance
converter = CSVToExcelConverter(root)

# Mock the GUI display methods so we don't show the window
converter.root.update = MagicMock()

# Set file paths
converter.csv_file_var.set('Backtest/trades_20260120_215755.csv')
converter.output_folder_var.set('Backtest')

# Test conversion
print("Testing Excel conversion...")
converter._do_conversion()

print("Test completed!")
root.destroy()
