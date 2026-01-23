#!/usr/bin/env python3
"""
Test the license activation dialog fix
"""

import os
import sys
import time
from pathlib import Path

def test_license_system():
    print("\n" + "="*70)
    print("🔧 TEST: LICENSE ACTIVATION DIALOG FIX")
    print("="*70)
    
    # Test 1: Check that license file can be loaded and verified
    print("\n1️⃣ Test: License validation...")
    from license_manager import LicenseManager
    
    lm = LicenseManager()
    is_valid, msg = lm.verify_license()
    
    print(f"   License valid: {is_valid}")
    print(f"   Message: {msg}")
    
    if not is_valid:
        print("   ❌ FAIL: License should be valid!")
        return False
    else:
        print("   ✅ PASS: License is valid")
    
    # Test 2: Backup and remove license.json to test dialog
    print("\n2️⃣ Test: Backup license for next test...")
    license_file = Path("license.json")
    backup_file = Path("license.json.backup_test")
    
    if license_file.exists():
        license_file.rename(backup_file)
        print(f"   ✅ License backed up to {backup_file}")
    
    # Test 3: Verify that without license, verification fails
    print("\n3️⃣ Test: License verification should fail without file...")
    is_valid, msg = lm.verify_license()
    
    print(f"   License valid: {is_valid}")
    print(f"   Message: {msg}")
    
    if is_valid:
        print("   ❌ FAIL: License should NOT be valid without file!")
        # Restore license
        backup_file.rename(license_file)
        return False
    else:
        print("   ✅ PASS: License correctly fails without file")
    
    # Test 4: Restore license
    print("\n4️⃣ Test: Restore license...")
    if backup_file.exists():
        backup_file.rename(license_file)
        print(f"   ✅ License restored from backup")
    
    # Test 5: Final verification
    print("\n5️⃣ Test: Final license validation...")
    is_valid, msg = lm.verify_license()
    
    print(f"   License valid: {is_valid}")
    print(f"   Message: {msg}")
    
    if is_valid:
        print("   ✅ PASS: License valid again after restore")
    else:
        print("   ❌ FAIL: License should be valid after restore!")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    return True

if __name__ == "__main__":
    success = test_license_system()
    sys.exit(0 if success else 1)
