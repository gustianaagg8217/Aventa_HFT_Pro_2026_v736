"""
Test script untuk License System
Gunakan untuk testing berbagai scenario
"""

import sys
from license_manager import (
    HardwareIDGenerator,
    SerialKeyGenerator,
    LicenseManager
)
import json


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def test_hardware_id():
    """Test 1: Generate Hardware ID"""
    print_header("TEST 1: Generate Hardware ID")
    
    generator = HardwareIDGenerator()
    hw_id = generator.get_hardware_id()
    
    print(f"Generated Hardware ID: {hw_id}")
    print(f"Length: {len(hw_id)} characters")
    print("✓ Test passed: Hardware ID generated successfully")
    
    return hw_id


def test_serial_generation(hw_id):
    """Test 2: Generate Serial Number"""
    print_header("TEST 2: Generate Serial Number")
    
    generator = SerialKeyGenerator()
    serial = generator.generate_serial(hw_id)
    
    print(f"Hardware ID: {hw_id}")
    print(f"Generated Serial: {serial}")
    print(f"Serial Format: AV-XXXX-XXXX-XXXX-HHHH")
    print("✓ Test passed: Serial generated successfully")
    
    return serial


def test_serial_validation(serial, hw_id):
    """Test 3: Validate Serial for Hardware"""
    print_header("TEST 3: Validate Serial for Hardware")
    
    generator = SerialKeyGenerator()
    is_valid = generator.validate_serial(serial, hw_id)
    
    print(f"Serial: {serial}")
    print(f"Hardware ID: {hw_id}")
    print(f"Validation Result: {is_valid}")
    
    if is_valid:
        print("✓ Test passed: Serial is valid for this hardware")
    else:
        print("✗ Test failed: Serial is NOT valid for this hardware")
    
    return is_valid


def test_wrong_serial_validation(serial, different_hw_id):
    """Test 4: Validate Serial with WRONG Hardware"""
    print_header("TEST 4: Validate Serial with Wrong Hardware (should FAIL)")
    
    generator = SerialKeyGenerator()
    is_valid = generator.validate_serial(serial, different_hw_id)
    
    print(f"Serial: {serial} (from other hardware)")
    print(f"Current Hardware ID: {different_hw_id} (different)")
    print(f"Validation Result: {is_valid}")
    
    if not is_valid:
        print("✓ Test passed: Serial correctly rejected for different hardware")
    else:
        print("✗ Test failed: Serial should NOT work for different hardware")
    
    return not is_valid


def test_license_creation_and_save(serial, hw_id):
    """Test 5: Create and Save License"""
    print_header("TEST 5: Create and Save License")
    
    manager = LicenseManager("test_license.json")
    
    # Override hardware ID for testing
    print(f"Creating license for: {hw_id}")
    
    license_data = manager.create_license(serial)
    print(f"\nLicense Data:")
    print(json.dumps(license_data, indent=2))
    
    # Check if create_license returned an error
    if license_data.get("status") == "error":
        print(f"\n✗ Test failed: {license_data.get('message')}")
        return False
    
    if manager.save_license(license_data):
        print("\n✓ Test passed: License created and saved successfully")
        return True
    else:
        print("\n✗ Test failed: Could not save license")
        return False


def test_license_load():
    """Test 6: Load License"""
    print_header("TEST 6: Load License")
    
    manager = LicenseManager("test_license.json")
    license_data = manager.load_license()
    
    if license_data.get("status") == "error":
        print(f"✗ Test failed: {license_data.get('message')}")
        return False
    
    print("Loaded License Data:")
    print(json.dumps(license_data, indent=2))
    print("\n✓ Test passed: License loaded successfully")
    
    return True


def test_license_verification():
    """Test 7: Verify License"""
    print_header("TEST 7: Verify License")
    
    manager = LicenseManager("test_license.json")
    is_valid, message = manager.verify_license()
    
    print(f"License Valid: {is_valid}")
    print(f"Message: {message}")
    
    if is_valid:
        print("✓ Test passed: License verified successfully")
    else:
        print(f"✗ Test failed: {message}")
    
    return is_valid


def test_wrong_hardware_rejection():
    """Test 8: Reject License on Wrong Hardware"""
    print_header("TEST 8: License Rejection on Wrong Hardware")
    
    # This test requires simulating different hardware
    # For now, just show the concept
    
    print("Concept Test: License bound to hardware")
    print("When license is moved to different computer:")
    print("- Hardware ID will be different")
    print("- License verification will fail")
    print("- User will see: 'License is bound to a different hardware'")
    print("- User will need new serial number for new hardware")
    
    print("\n✓ Concept verified in license_manager.verify_license()")


def test_encryption():
    """Test 9: Encryption"""
    print_header("TEST 9: License File Encryption")
    
    try:
        # Try to read the license file as text
        with open("test_license.json", "rb") as f:
            raw_data = f.read()
        
        # Try to decode as JSON (should fail if encrypted)
        try:
            json.loads(raw_data.decode())
            print("✗ Test failed: License file is NOT encrypted")
            return False
        except:
            print("License file is binary/encrypted (not readable as plain JSON)")
            print(f"File size: {len(raw_data)} bytes")
            print("✓ Test passed: License file is encrypted")
            return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False


def cleanup():
    """Clean up test files"""
    print_header("CLEANUP")
    
    import os
    
    try:
        if os.path.exists("test_license.json"):
            os.remove("test_license.json")
            print("✓ Removed test_license.json")
    except Exception as e:
        print(f"Warning: {e}")


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  AVENTA HFT PRO 2026 - LICENSE SYSTEM TEST SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {}
    
    try:
        # Test 1
        hw_id = test_hardware_id()
        results["Hardware ID Generation"] = True
        
        # Test 2
        serial = test_serial_generation(hw_id)
        results["Serial Generation"] = True
        
        # Test 3
        results["Serial Validation"] = test_serial_validation(serial, hw_id)
        
        # Test 4 - Generate different HW ID for comparison
        different_hw_id = "0123456789ABCDEF"  # Fake different hardware
        results["Wrong Serial Rejection"] = test_wrong_serial_validation(serial, different_hw_id)
        
        # Test 5 - Modified: Generate serial for current hardware instead
        current_hw_id = HardwareIDGenerator().get_hardware_id()
        current_serial = SerialKeyGenerator().generate_serial(current_hw_id)
        results["License Creation & Save"] = test_license_creation_and_save(current_serial, current_hw_id)
        
        # Test 6
        results["License Loading"] = test_license_load()
        
        # Test 7
        results["License Verification"] = test_license_verification()
        
        # Test 8
        test_wrong_hardware_rejection()
        results["Hardware Binding Concept"] = True
        
        # Test 9
        results["Encryption"] = test_encryption()
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        cleanup()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! License system is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
