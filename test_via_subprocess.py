"""Test converter via subprocess wrapper"""
import subprocess
import sys
import os
from pathlib import Path

# Create inline test
test_code = """
import sys
import os
sys.path.insert(0, r'c:\\Users\\LENOVO THINKPAD\\Documents\\Aventa_AI_2026\\Aventa_HFT_Pro_2026_v736')

from csv_to_excel_converter_gui_736 import CSVToExcelConverter
import tkinter as tk

# Initialize
root = tk.Tk()
root.withdraw()

converter = CSVToExcelConverter(root)

# Set paths
csv_file = 'test_1644_proper.csv'
output_folder = 'test_subprocess'
os.makedirs(output_folder, exist_ok=True)

converter.csv_file_var.set(csv_file)
converter.output_folder_var.set(output_folder)

# Clear logs
converter.log_text.delete(1.0, tk.END)

# Run conversion
print('[CONVERTER] Running _do_conversion...')
converter._do_conversion()

# Update GUI to process any pending events
root.update()

# Check for output
from pathlib import Path
xlsx_files = list(Path(output_folder).glob('*.xlsx'))
pdf_files = list(Path(output_folder).glob('*.pdf'))

print(f'[RESULT] XLSX: {len(xlsx_files)} file(s)')
print(f'[RESULT] PDF: {len(pdf_files)} file(s)')

if xlsx_files:
    for f in xlsx_files:
        size_kb = f.stat().st_size / 1024
        print(f'[FILE] {f.name} ({size_kb:.1f} KB)')

# Get any error logs
log_text = converter.log_text.get(1.0, tk.END)
print('[FULL LOG]')
print(log_text)
error_lines = [line for line in log_text.split(chr(10)) if 'ERROR' in line or 'error' in line or 'Exception' in line]
if error_lines:
    print('[ERRORS]')
    for line in error_lines:
        print(f'  {line}')

root.destroy()

# Exit with success if files created
if xlsx_files or pdf_files:
    sys.exit(0)
else:
    sys.exit(1)
"""

# Write temp file
with open('_temp_converter_test.py', 'w') as f:
    f.write(test_code)

print('[TEST] Running converter via subprocess...')
print('=' * 60)

try:
    result = subprocess.run([sys.executable, '_temp_converter_test.py'], 
                           capture_output=True, text=True, timeout=120, cwd=os.getcwd())
    
    print(result.stdout)
    if result.stderr:
        print('[STDERR]')
        print(result.stderr)
    
    print(f'\nExit code: {result.returncode}')
    
    if result.returncode == 0:
        print('\n[SUCCESS] Converter test completed!')
    else:
        print('\n[ERROR] Converter test failed!')
        
except subprocess.TimeoutExpired:
    print('[ERROR] Subprocess timeout after 120 seconds')
except Exception as e:
    print(f'[ERROR] {e}')
finally:
    # Cleanup
    if os.path.exists('_temp_converter_test.py'):
        os.remove('_temp_converter_test.py')
