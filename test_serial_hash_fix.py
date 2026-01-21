"""
Test: Verify serial generation and validation use same hash function (MD5)
This tests the fix for the hash mismatch between serial_generator.py and license_manager.py
"""

import hashlib
import sys
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path(__file__).parent))

# Import both classes
from serial_generator import SerialKeyGenerator as SG_SerialKeyGenerator, HardwareIDGenerator as SG_HardwareIDGenerator
from license_manager import SerialKeyGenerator as LM_SerialKeyGenerator, HardwareIDGenerator as LM_HardwareIDGenerator

def test_hash_function_consistency():
    """Test that both generators use MD5 for hardware ID hashing"""
    print("\n" + "="*80)
    print("TEST: Hash Function Consistency (MD5)")
    print("="*80)
    
    test_hardware_ids = [
        "AB4$FBA8$459C2E4",
        "550e8400-e29b-41d4-a716-446655440000",
        "DEADBEEFCAFEBABE",
    ]
    
    for hw_id in test_hardware_ids:
        # Get hash from serial_generator
        sg_hash = SG_HardwareIDGenerator.hash_hardware_id(hw_id)
        
        # Calculate expected hash from license_manager approach
        expected_hash = hashlib.md5(hw_id.encode()).hexdigest()[:4].upper()
        
        # They should match
        match = "✅ PASS" if sg_hash == expected_hash else "❌ FAIL"
        print(f"{match} | HW_ID: {hw_id:30} | SG_Hash: {sg_hash} | Expected: {expected_hash}")
        
        if sg_hash != expected_hash:
            print(f"  ERROR: Hashes don't match! {sg_hash} != {expected_hash}")
            return False
    
    print()
    return True

def test_serial_generation_and_validation():
    """Test complete serial generation and validation flow"""
    print("\n" + "="*80)
    print("TEST: Serial Generation → Validation Flow")
    print("="*80)
    
    # Use a known hardware ID
    hw_id = "AB4$FBA8$459C2E4"
    print(f"\nTest Hardware ID: {hw_id}")
    
    # Generate serial using serial_generator
    serial, data = SG_SerialKeyGenerator.generate_serial(hw_id, expiry_days=-1)
    print(f"Generated Serial: {serial}")
    
    # Validate using license_manager
    lm_validator = LM_SerialKeyGenerator()
    is_valid = lm_validator.validate_serial(serial, hw_id)
    
    result = "✅ PASS" if is_valid else "❌ FAIL"
    print(f"{result} | Serial validation: {is_valid}")
    
    if not is_valid:
        print("  ERROR: Generated serial failed validation!")
        # Debug: Extract and compare checksums
        parts = serial.split('-')
        serial_checksum = parts[4] if len(parts) == 5 else "INVALID"
        expected_checksum = hashlib.md5(hw_id.encode()).hexdigest()[:4].upper()
        print(f"  Serial checksum:   {serial_checksum}")
        print(f"  Expected checksum: {expected_checksum}")
        return False
    
    print()
    return True

def test_prefix_format():
    """Test that serial prefix is AV"""
    print("\n" + "="*80)
    print("TEST: Serial Prefix Format")
    print("="*80)
    
    hw_id = "TEST_HARDWARE_ID"
    
    # Generate multiple serials
    for i in range(3):
        serial, _ = SG_SerialKeyGenerator.generate_serial(hw_id)
        prefix_ok = serial.startswith("AV-")
        format_ok = len(serial.split('-')) == 5
        
        result = "✅ PASS" if (prefix_ok and format_ok) else "❌ FAIL"
        print(f"{result} | Serial {i+1}: {serial} | Prefix: {'AV-' if prefix_ok else 'WRONG'} | Format: {'AV-X-X-X-X' if format_ok else 'WRONG'}")
        
        if not (prefix_ok and format_ok):
            return False
    
    print()
    return True

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("SERIAL GENERATOR FIX VERIFICATION")
    print("="*80)
    print("Testing: Hash algorithm synchronization (MD5)")
    print("Fix: Changed serial_generator.py from SHA256 to MD5")
    
    tests = [
        ("Hash Function Consistency", test_hash_function_consistency),
        ("Serial Format & Prefix", test_prefix_format),
        ("Serial Generation → Validation", test_serial_generation_and_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! Serial hash fix is working correctly.")
        print("Serials generated with serial_generator.py will now validate correctly.")
    else:
        print(f"\n❌ {total - passed} TEST(S) FAILED!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
