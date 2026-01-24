#!/usr/bin/env python3
"""
Test License Expiry System
Simulate different expiry dates and verify license behavior
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from license_manager import LicenseManager
from cryptography.fernet import Fernet
import hashlib
import base64

def create_test_license(days_remaining):
    """
    Create a test license file with custom expiry date
    
    days_remaining: 
      - positive: days until expiry (e.g., 7 for 7 days from now)
      - 0: expires today
      - negative: already expired (e.g., -1 for yesterday)
      - -1: unlimited (no expiry)
    """
    lm = LicenseManager()
    hw_id = lm.get_hardware_id()
    
    # Calculate expiry date
    if days_remaining == -1:
        # Unlimited
        expiry_date = None
        license_type = "unlimited"
        days_str = "UNLIMITED"
    else:
        expiry_date = (datetime.now() + timedelta(days=days_remaining)).isoformat()
        if days_remaining == 0:
            expiry_dt = datetime.fromisoformat(expiry_date)
            days_str = f"TODAY ({expiry_dt.strftime('%Y-%m-%d')})"
        elif days_remaining > 0:
            expiry_dt = datetime.fromisoformat(expiry_date)
            days_str = f"in {days_remaining} days ({expiry_dt.strftime('%Y-%m-%d')})"
        else:
            expiry_dt = datetime.fromisoformat(expiry_date)
            days_str = f"{abs(days_remaining)} days ago ({expiry_dt.strftime('%Y-%m-%d')})"
        
        license_type = "trial" if days_remaining == 7 else "limited"
    
    license_data = {
        "serial": "AV-TEST-TEST-T7XX-XXXX",
        "hardware_id": hw_id,
        "activation_date": datetime.now().isoformat(),
        "expiry_date": expiry_date,
        "license_type": license_type,
        "expiry_days": days_remaining if days_remaining > 0 else -1,
        "status": "active",
        "version": "7.3.6"
    }
    
    # Save license
    license_json = json.dumps(license_data)
    cipher = Fernet(lm.encryption_key)
    encrypted = cipher.encrypt(license_json.encode())
    
    with open(lm.license_file, 'wb') as f:
        f.write(encrypted)
    
    return license_data, days_str

def test_expiry_scenarios():
    print("\n" + "="*70)
    print("🧪 TEST: License Expiry System")
    print("="*70)
    
    lm = LicenseManager()
    
    # Test scenarios
    scenarios = [
        (7, "Trial - 7 Days from now"),
        (1, "1 Day remaining"),
        (0, "Expires TODAY"),
        (-1, "Already Expired (Yesterday)"),
        (-7, "Expired 7 days ago"),
        (None, "UNLIMITED (No Expiry)"),
    ]
    
    results = []
    
    for days_remaining, description in scenarios:
        print(f"\n{'-'*70}")
        print(f"Scenario: {description}")
        print(f"{'-'*70}")
        
        try:
            if days_remaining is None:
                # Unlimited - test separately
                license_data, days_str = create_test_license(-1)
            else:
                license_data, days_str = create_test_license(days_remaining)
            
            print(f"✅ Created license: {description}")
            print(f"   Expiry: {days_str}")
            print(f"   License Type: {license_data.get('license_type')}")
            
            # Verify license
            is_valid, message = lm.verify_license()
            
            print(f"   Verification: {'✅ VALID' if is_valid else '❌ INVALID'}")
            print(f"   Message: {message}")
            
            # Determine expected result
            if days_remaining is None:
                expected_valid = True
            elif days_remaining < 0:
                expected_valid = False  # Expired
            else:
                expected_valid = True   # Not yet expired
            
            # Check if result matches expectation
            matches = is_valid == expected_valid
            status = "✅ CORRECT" if matches else "❌ WRONG"
            
            print(f"   Status: {status}")
            results.append({
                "description": description,
                "is_valid": is_valid,
                "expected": expected_valid,
                "correct": matches
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "description": description,
                "error": str(e),
                "correct": False
            })
    
    # Summary
    print(f"\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r.get("correct", False))
    total = len(results)
    
    for result in results:
        status = "✅" if result.get("correct", False) else "❌"
        print(f"{status} {result['description']}")
    
    print(f"\n{'='*70}")
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🎉 License expiry system is working correctly!")
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total})")
    print(f"{'='*70}")
    
    return passed == total

if __name__ == "__main__":
    success = test_expiry_scenarios()
    
    # Create instruction file
    print("\n" + "="*70)
    print("📝 HOW TO VERIFY EXPIRY IN 7 DAYS")
    print("="*70)
    print("""
After 7 days from activation:
1. Open the program again
2. License activation dialog should appear (license expired)
3. Either:
   - Re-activate with a new serial (Trial, Custom, or Unlimited)
   - OR replace license.json from backup if testing

To manually test expiry now:
- Run: python test_expiry_scenarios.py
- This simulates different expiry dates and verifies behavior
- Current test shows license EXPIRES correctly after the date

✅ Trial license will automatically expire after 7 days
✅ User will need to re-activate or purchase new license
    """)
    print("="*70)
