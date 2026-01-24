"""Test converter dengan actual CSV dari screenshot"""
import sys
import os
sys.path.insert(0, r'c:\Users\LENOVO THINKPAD\Documents\Aventa_AI_2026\Aventa_HFT_Pro_2026_v736')

from csv_to_excel_converter_gui_736 import CSVToExcelConverter
import tkinter as tk
from pathlib import Path

print('[TEST] Testing converter dengan trades_20260124_121916.csv')
print('=' * 60)

# Create GUI
root = tk.Tk()
root.withdraw()

# Initialize
converter = CSVToExcelConverter(root)

# Set files
csv_file = r'C:\Users\LENOVO THINKPAD\Documents\trades_20260124_121916.csv'
output_folder = 'test_real_csv'
os.makedirs(output_folder, exist_ok=True)

if not os.path.exists(csv_file):
    print(f'[ERROR] CSV not found: {csv_file}')
    root.destroy()
    sys.exit(1)

converter.csv_file_var.set(csv_file)
converter.output_folder_var.set(output_folder)

# Clear logs
converter.log_text.delete(1.0, tk.END)

print('[RUN] Starting conversion...')
try:
    # Run directly
    converter._do_conversion()
    
    # Update GUI
    root.update()
    
    # Get logs
    log_text = converter.log_text.get(1.0, tk.END)
    for line in log_text.split('\n')[-20:]:
        if line.strip():
            try:
                print(line)
            except:
                pass
    
    # Check output
    xlsx_files = list(Path(output_folder).glob('*.xlsx'))
    if xlsx_files:
        for f in xlsx_files:
            size_kb = f.stat().st_size / 1024
            print(f'\n[SUCCESS] {f.name} ({size_kb:.1f} KB)')
    else:
        print('\n[ERROR] No Excel files created')
        
except Exception as e:
    print(f'[ERROR] Exception: {e}')
    import traceback
    traceback.print_exc()
    root.destroy()
    sys.exit(1)

root.destroy()
