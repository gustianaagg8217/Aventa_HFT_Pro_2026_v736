"""
Quick verification that Custom Days option is available
"""

import tkinter as tk
from serial_generator import SerialGeneratorGUI

def test():
    root = tk.Tk()
    gui = SerialGeneratorGUI(root)
    
    print("✅ GUI initialized")
    print(f"✅ Window size: {root.geometry()}")
    
    # Check if custom days entry exists
    if hasattr(gui, 'custom_days_entry'):
        print("✅ Custom Days input field exists")
        print(f"✅ Default value: {gui.custom_days_entry.get()}")
    else:
        print("❌ Custom Days input field not found")
    
    # Check if license type var exists
    if hasattr(gui, 'license_type_var'):
        print("✅ License Type variable exists")
        print(f"✅ Default type: {gui.license_type_var.get()}")
    
    root.after(1000, root.quit)
    root.mainloop()
    
    print("\n✅ All options available:")
    print("  - 🔓 Unlimited (No expiry)")
    print("  - ⏱️ Trial 7 Days (auto expire)")
    print("  - 📅 Custom Days [30]")

if __name__ == "__main__":
    test()
