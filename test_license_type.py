#!/usr/bin/env python3
"""
Test License Type Decoding from Serial Number
"""

from license_manager import LicenseManager

def test_metadata_decode():
    print("\n" + "="*70)
    print("🔧 TEST: License Type Decoding from Serial")
    print("="*70)
    
    lm = LicenseManager()
    
    # Test cases
    test_cases = [
        ("UUUU", -1, "UNLIMITED"),
        ("T7XX", 7, "TRIAL"),
        ("D01XX", 1, "CUSTOM (1 day)"),
        ("D30XX", 30, "CUSTOM (30 days)"),
    ]
    
    for metadata, expected_days, description in test_cases:
        result = lm.serial_generator._decode_metadata(metadata)
        status = "✅" if result == expected_days else "❌"
        print(f"{status} {metadata} -> {result} days (expected {expected_days}) - {description}")
    
    # Now test with actual serial numbers
    print("\n" + "="*70)
    print("Testing with actual serial numbers:")
    print("="*70)
    
    # Extract metadata from a serial
    test_serials = [
        "AV-H0TL-RZK1-UUUU-94BF",  # Unlimited
        "AV-SLA7-ABC1-T7XX-57DC",   # Trial
        "AV-1234-5678-D30XX-ABCD",  # 30 days
    ]
    
    for serial in test_serials:
        parts = serial.split('-')
        metadata = parts[3]
        days = lm.serial_generator._decode_metadata(metadata)
        
        # Determine license type
        if days == -1:
            license_type = "UNLIMITED"
        elif days == 7:
            license_type = "TRIAL"
        else:
            license_type = f"CUSTOM ({days} days)"
        
        print(f"✅ Serial: {serial}")
        print(f"   Metadata: {metadata} -> {license_type}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_metadata_decode()
