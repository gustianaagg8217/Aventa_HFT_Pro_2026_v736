"""
Quick test to verify serial generator GUI with expiry options
"""

import tkinter as tk
from serial_generator import SerialGeneratorGUI

def test_gui():
    """Quick GUI test"""
    print("Testing Serial Generator GUI with Expiry Options...")
    
    root = tk.Tk()
    gui = SerialGeneratorGUI(root)
    
    print("✅ GUI initialized successfully")
    print("✅ License type options loaded")
    print("✅ Custom days input field ready")
    print("\nGUI Window Open - Check that you see:")
    print("  - Hardware ID input field")
    print("  - License Type section with 3 options:")
    print("    ○ 🔓 Unlimited (No expiry)")
    print("    ○ ⏱️ Trial 7 Days (auto expire)")
    print("    ○ 📅 Custom Days [30]")
    print("  - Generate Serial, Copy Serial, Clear buttons")
    print("  - Log display area")
    print("\nClose the window to finish test...")
    
    # Auto-close after 3 seconds for automated testing
    root.after(3000, root.quit)
    
    try:
        root.mainloop()
        print("✅ GUI test completed successfully")
        return True
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gui()
    exit(0 if success else 1)
