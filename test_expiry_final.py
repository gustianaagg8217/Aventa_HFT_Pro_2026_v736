#!/usr/bin/env python3
"""
Test License Expiry System - FIXED
Verify that licenses expire correctly after their expiry date
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from license_manager import LicenseManager
from cryptography.fernet import Fernet

def create_test_license_with_expiry(days_remaining):
    """
    Create a valid test license with specific expiry date
    
    days_remaining:
      -1: unlimited (no expiry)
      0-N: expires in N days
      -1-...: already expired
    """
    lm = LicenseManager()
    hw_id = lm.get_hardware_id()
    
    # Generate a valid serial for this hardware
    serial = lm.serial_generator.generate_serial(hw_id)
    
    # Calculate expiry date
    if days_remaining == -1 and days_remaining < 0:
        # Unlimited
        expiry_date = None
        license_type = "unlimited"
        display_str = "UNLIMITED (No Expiry)"
    else:
        # Calculate date
        expiry_date = (datetime.now() + timedelta(days=days_remaining)).isoformat()
        expiry_dt = datetime.fromisoformat(expiry_date)
        
        if days_remaining == 0:
            display_str = f"TODAY ({expiry_dt.strftime('%Y-%m-%d')})"
        elif days_remaining > 0:
            display_str = f"+{days_remaining} days ({expiry_dt.strftime('%Y-%m-%d')})"
        else:
            display_str = f"{days_remaining} days ({expiry_dt.strftime('%Y-%m-%d')})"
        
        license_type = "trial" if days_remaining == 7 else "limited"
    
    # Create license data
    license_data = {
        "serial": serial,
        "hardware_id": hw_id,
        "activation_date": datetime.now().isoformat(),
        "expiry_date": expiry_date,
        "license_type": license_type,
        "expiry_days": days_remaining if days_remaining >= 0 else -1,
        "status": "active",
        "version": "7.3.6"
    }
    
    # Save encrypted license
    license_json = json.dumps(license_data)
    cipher = Fernet(lm.encryption_key)
    encrypted = cipher.encrypt(license_json.encode())
    
    with open(lm.license_file, 'wb') as f:
        f.write(encrypted)
    
    return license_data, display_str

def test_license_expiry():
    print("\n" + "="*70)
    print("✅ TEST: License Expiry System")
    print("="*70)
    
    lm = LicenseManager()
    
    # Test scenarios
    scenarios = [
        (7, True, "Trial License - 7 Days remaining"),
        (1, True, "1 Day remaining - Still VALID"),
        (0, True, "Expires TODAY - Still VALID"),
        (-1, False, "Expired YESTERDAY - INVALID"),
        (-7, False, "Expired 7 days ago - INVALID"),
    ]
    
    results = []
    
    for days_remaining, should_be_valid, description in scenarios:
        print(f"\n{'-'*70}")
        print(f"Test: {description}")
        print(f"{'-'*70}")
        
        try:
            # Create test license
            license_data, expiry_str = create_test_license_with_expiry(days_remaining)
            
            print(f"✅ Created test license")
            print(f"   Serial: {license_data['serial']}")
            print(f"   Type: {license_data['license_type'].upper()}")
            print(f"   Expiry: {expiry_str}")
            
            # Verify license
            is_valid, message = lm.verify_license()
            
            # Check result
            result_str = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"   Verification Result: {result_str}")
            print(f"   Message: {message}")
            
            # Evaluate if correct
            is_correct = (is_valid == should_be_valid)
            expected_str = "VALID" if should_be_valid else "INVALID"
            status = "✅ CORRECT" if is_correct else "❌ WRONG"
            
            print(f"   Expected: {expected_str}")
            print(f"   Status: {status}")
            
            results.append({
                "description": description,
                "is_valid": is_valid,
                "expected": should_be_valid,
                "correct": is_correct
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "description": description,
                "error": str(e),
                "correct": False
            })
    
    # Summary
    print(f"\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r.get("correct", False))
    total = len(results)
    
    for result in results:
        status = "✅" if result.get("correct", False) else "❌"
        print(f"{status} {result['description']}")
    
    print(f"\n{'='*70}")
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🎉 License expiry system working correctly!")
        print("\nAfter 7 days from REAL activation:")
        print("1. License will automatically show as EXPIRED")
        print("2. User must activate new license (Trial/Unlimited/Custom)")
        print("3. Dialog will appear again requiring new serial")
    else:
        print(f"❌ SOME TESTS FAILED ({total-passed}/{total})")
    print(f"{'='*70}\n")
    
    return passed == total

if __name__ == "__main__":
    success = test_license_expiry()
    exit(0 if success else 1)
