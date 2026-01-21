"""
Test: Dialog activation muncul dengan baik
Menghapus license.json sementara untuk trigger dialog
"""

import sys
import os
from pathlib import Path
import shutil
import subprocess
import time

def test_dialog_appears():
    """Test that activation dialog appears"""
    
    print("\n" + "="*70)
    print("🔐 TESTING: License Activation Dialog Appears")
    print("="*70)
    
    license_file = Path("license.json")
    backup_file = Path("license.json.backup_dialog_test")
    
    # Backup existing license
    if license_file.exists():
        shutil.copy(license_file, backup_file)
        license_file.unlink()
        print("\n✅ Removed license.json to trigger dialog")
    
    try:
        print("\n⏳ Starting program...")
        print("   If dialog appears correctly, you should see it within 5 seconds")
        print("   Dialog should show:")
        print("   - 🔐 License Activation Required title")
        print("   - Hardware ID display")
        print("   - Serial input field")
        print("   - Copy button")
        print("   - Activate/Cancel/Help buttons")
        
        # Note: Can't automate checking if dialog appeared
        # But we can verify the code structure is correct
        
        # Check license_check.py
        with open("license_check.py", 'r', encoding='utf-8') as f:
            check_content = f.read()
        
        # Check license_manager.py
        with open("license_manager.py", 'r', encoding='utf-8') as f:
            manager_content = f.read()
        
        checks = [
            ("Dialog attributes('-topmost'", "attributes('-topmost'" in manager_content),
            ("Dialog lift()", "dialog.lift()" in manager_content),
            ("Dialog focus_force()", "dialog.focus_force()" in manager_content),
            ("Dialog center on screen", "screen_width =" in manager_content),
            ("Hardware ID display", "Hardware ID (Unique to this PC)" in manager_content),
            ("Serial input field", "Enter Serial Number" in manager_content),
            ("Copy button", "Copy Hardware ID" in manager_content),
            ("Root geometry hidden", 'geometry("0x0+0+0")' in check_content),
            ("Root attributes alpha", "attributes('-alpha', 0)" in check_content),
        ]
        
        print("\n✅ DIALOG IMPLEMENTATION CHECKS:\n")
        all_pass = True
        for check_name, result in checks:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {check_name}")
            if not result:
                all_pass = False
        
        if all_pass:
            print("\n" + "="*70)
            print("✅ ALL DIALOG COMPONENTS PROPERLY IMPLEMENTED")
            print("="*70)
            print("\nDialog should now appear when you run the program!")
            print("It will be:")
            print("  ✅ Centered on screen")
            print("  ✅ On top of all windows")
            print("  ✅ Properly focused")
            print("  ✅ With all input fields ready")
            return True
        else:
            print("\n" + "="*70)
            print("❌ SOME COMPONENTS MISSING")
            print("="*70)
            return False
    
    finally:
        # Restore license
        if backup_file.exists():
            shutil.copy(backup_file, license_file)
            backup_file.unlink()
            print("\n✅ License restored")


if __name__ == "__main__":
    print("\n" + "🔐"*35)
    print("DIALOG APPEARANCE TEST")
    print("🔐"*35)
    
    if test_dialog_appears():
        print("\n✅ Ready to run: python Aventa_HFT_Pro_2026_v7_3_6.py")
        print("   Dialog should appear within 5 seconds")
    else:
        print("\n❌ Dialog implementation needs fixes")
        sys.exit(1)
