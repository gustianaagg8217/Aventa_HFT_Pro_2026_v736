"""
Test suite for license expiry functionality
Tests unlimited, trial (7 days), and custom expiry licenses
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from license_manager import LicenseManager, HardwareIDGenerator, SerialKeyGenerator


def test_expiry_system():
    """Test license expiry system"""
    print("\n" + "=" * 70)
    print("AVENTA HFT PRO 2026 - LICENSE EXPIRY SYSTEM TEST")
    print("=" * 70)
    
    # Setup
    hw_gen = HardwareIDGenerator()
    hw_id = hw_gen.get_hardware_id()
    serial_gen = SerialKeyGenerator()
    
    print(f"\nHardware ID: {hw_id}")
    
    tests_passed = 0
    tests_failed = 0
    
    # TEST 1: UNLIMITED LICENSE
    print("\n" + "-" * 70)
    print("TEST 1: UNLIMITED LICENSE")
    print("-" * 70)
    try:
        lm1 = LicenseManager("test_license_unlimited.json")
        
        # Generate serial
        serial1 = serial_gen.generate_serial(hw_id, -1)
        print(f"Generated Serial: {serial1}")
        
        # Create license with unlimited expiry
        license1 = lm1.create_license(serial1, expiry_days=-1)
        print(f"License Type: {license1.get('license_type')}")
        print(f"Expiry Date: {license1.get('expiry_date')}")
        
        # Verify
        if license1.get('license_type') == 'unlimited' and license1.get('expiry_date') is None:
            print("✅ PASS: Unlimited license created correctly")
            tests_passed += 1
        else:
            print("❌ FAIL: Unlimited license not created correctly")
            tests_failed += 1
            
        # Save and verify
        lm1.save_license(license1)
        is_valid, msg = lm1.verify_license()
        print(f"Verification: {msg}")
        if is_valid:
            print("✅ PASS: Unlimited license verified")
            tests_passed += 1
        else:
            print("❌ FAIL: Unlimited license verification failed")
            tests_failed += 1
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 2
    
    # TEST 2: TRIAL LICENSE (7 DAYS)
    print("\n" + "-" * 70)
    print("TEST 2: TRIAL LICENSE (7 DAYS)")
    print("-" * 70)
    try:
        lm2 = LicenseManager("test_license_trial.json")
        
        # Generate serial
        serial2 = serial_gen.generate_serial(hw_id, 7)
        print(f"Generated Serial: {serial2}")
        
        # Create trial license
        license2 = lm2.create_license(serial2, expiry_days=7)
        print(f"License Type: {license2.get('license_type')}")
        print(f"Expiry Date: {license2.get('expiry_date')[:10]}")
        
        # Verify
        if license2.get('license_type') == 'trial' and license2.get('expiry_date'):
            print("✅ PASS: Trial license created correctly")
            tests_passed += 1
        else:
            print("❌ FAIL: Trial license not created correctly")
            tests_failed += 1
        
        # Save and verify
        lm2.save_license(license2)
        is_valid, msg = lm2.verify_license()
        print(f"Verification: {msg}")
        if is_valid:
            print("✅ PASS: Trial license verified")
            tests_passed += 1
        else:
            print("❌ FAIL: Trial license verification failed")
            tests_failed += 1
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 2
    
    # TEST 3: CUSTOM LICENSE (30 DAYS)
    print("\n" + "-" * 70)
    print("TEST 3: CUSTOM LICENSE (30 DAYS)")
    print("-" * 70)
    try:
        lm3 = LicenseManager("test_license_custom.json")
        
        # Generate serial
        serial3 = serial_gen.generate_serial(hw_id, 30)
        print(f"Generated Serial: {serial3}")
        
        # Create custom license (30 days)
        license3 = lm3.create_license(serial3, expiry_days=30)
        print(f"License Type: {license3.get('license_type')}")
        print(f"Expiry Date: {license3.get('expiry_date')[:10]}")
        
        # Verify
        if license3.get('license_type') == 'limited' and license3.get('expiry_date'):
            print("✅ PASS: Custom license created correctly")
            tests_passed += 1
        else:
            print("❌ FAIL: Custom license not created correctly")
            tests_failed += 1
        
        # Save and verify
        lm3.save_license(license3)
        is_valid, msg = lm3.verify_license()
        print(f"Verification: {msg}")
        if is_valid:
            print("✅ PASS: Custom license verified")
            tests_passed += 1
        else:
            print("❌ FAIL: Custom license verification failed")
            tests_failed += 1
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 2
    
    # TEST 4: EXPIRED LICENSE
    print("\n" + "-" * 70)
    print("TEST 4: EXPIRED LICENSE DETECTION")
    print("-" * 70)
    try:
        lm4 = LicenseManager("test_license_expired.json")
        
        # Generate serial
        serial4 = serial_gen.generate_serial(hw_id, 1)
        print(f"Generated Serial: {serial4}")
        
        # Create license that expires tomorrow
        license4 = lm4.create_license(serial4, expiry_days=1)
        
        # Manually modify to make it expired (yesterday)
        license4['expiry_date'] = (datetime.now() - timedelta(days=1)).isoformat()
        print(f"License Type: {license4.get('license_type')}")
        print(f"Expiry Date: {license4.get('expiry_date')[:10]} (expired)")
        
        # Save
        lm4.save_license(license4)
        
        # Verify - should fail
        is_valid, msg = lm4.verify_license()
        print(f"Verification: {msg}")
        if not is_valid and "expired" in msg.lower():
            print("✅ PASS: Expired license correctly detected")
            tests_passed += 1
        else:
            print("❌ FAIL: Expired license not detected")
            tests_failed += 1
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 1
    
    # TEST 5: LICENSE TYPE DETERMINATION
    print("\n" + "-" * 70)
    print("TEST 5: LICENSE TYPE DETERMINATION")
    print("-" * 70)
    try:
        test_cases = [
            (-1, "unlimited", None),
            (7, "trial", "trial"),
            (30, "limited", "limited"),
            (90, "limited", "limited"),
        ]
        
        for expiry_days, expected_type, expected_label in test_cases:
            lm_test = LicenseManager(f"test_license_type_{expiry_days}.json")
            serial = serial_gen.generate_serial(hw_id, expiry_days)
            license_data = lm_test.create_license(serial, expiry_days=expiry_days)
            
            actual_type = license_data.get('license_type')
            if actual_type == expected_type:
                print(f"✅ {expiry_days} days -> {actual_type}")
                tests_passed += 1
            else:
                print(f"❌ {expiry_days} days -> {actual_type} (expected {expected_type})")
                tests_failed += 1
                
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 4
    
    # TEST 6: LICENSE DATA PERSISTENCE
    print("\n" + "-" * 70)
    print("TEST 6: LICENSE DATA PERSISTENCE")
    print("-" * 70)
    try:
        lm_persist = LicenseManager("test_license_persist.json")
        
        # Create and save
        serial_persist = serial_gen.generate_serial(hw_id, 60)
        license_persist = lm_persist.create_license(serial_persist, expiry_days=60)
        original_expiry = license_persist.get('expiry_date')
        
        lm_persist.save_license(license_persist)
        
        # Load and verify data persists
        loaded_license = lm_persist.load_license()
        loaded_expiry = loaded_license.get('expiry_date')
        
        if loaded_expiry == original_expiry:
            print(f"✅ PASS: License data persisted correctly")
            print(f"   Original: {original_expiry[:10]}")
            print(f"   Loaded:   {loaded_expiry[:10]}")
            tests_passed += 1
        else:
            print(f"❌ FAIL: License data not persisted")
            tests_failed += 1
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        tests_failed += 1
    
    # Cleanup
    test_files = [
        "test_license_unlimited.json",
        "test_license_trial.json",
        "test_license_custom.json",
        "test_license_expired.json",
        "test_license_persist.json"
    ]
    for f in test_files:
        try:
            Path(f).unlink()
        except:
            pass
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    total = tests_passed + tests_failed
    success_rate = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {tests_passed} ✅")
    print(f"Failed: {tests_failed} ❌")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed")
    
    print("=" * 70)
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_expiry_system()
    exit(0 if success else 1)
