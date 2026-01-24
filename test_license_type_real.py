#!/usr/bin/env python3
"""
Test License Type Decoding - Corrected
"""

from license_manager import LicenseManager
import hashlib

def test_metadata_decode():
    print("\n" + "="*70)
    print("🔧 TEST: License Type Decoding - CORRECTED")
    print("="*70)
    
    lm = LicenseManager()
    
    # Test the actual encoding/decoding
    print("\n1️⃣ Test basic metadata decoding:")
    
    test_cases = [
        ("UUUU", -1, "UNLIMITED"),
        ("T7XX", 7, "TRIAL"),
    ]
    
    for metadata, expected_days, description in test_cases:
        result = lm.serial_generator._decode_metadata(metadata)
        status = "✅" if result == expected_days else "❌"
        print(f"{status} {metadata} -> {result} days - {description}")
    
    # Test with real serial from screenshot
    print("\n2️⃣ Test with REAL serial from screenshot:")
    real_serial = "AV-SLA7-ABC1-T7XX-57DC"
    parts = real_serial.split('-')
    metadata = parts[3]
    
    print(f"Serial: {real_serial}")
    print(f"Metadata segment: {metadata}")
    
    days = lm.serial_generator._decode_metadata(metadata)
    print(f"Decoded days: {days}")
    
    if days == 7:
        license_type = "✅ TRIAL (7 Days)"
    elif days == -1:
        license_type = "❌ UNLIMITED (ERROR - should be TRIAL!)"
    else:
        license_type = f"CUSTOM ({days} days)"
    
    print(f"License type: {license_type}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_metadata_decode()
