#!/usr/bin/env python3
"""
Debug License Activation Dialog Issue
"""

import json
from pathlib import Path
from license_manager import LicenseManager

def main():
    print("\n" + "="*70)
    print("🔧 DEBUG: LICENSE ACTIVATION DIALOG ISSUE")
    print("="*70)
    
    license_file = Path("license.json")
    lm = LicenseManager()
    
    # 1. Check if license.json exists
    print(f"\n1️⃣ License file exists: {license_file.exists()}")
    
    if license_file.exists():
        print(f"   File size: {license_file.stat().st_size} bytes")
    
    # 2. Try to load license
    print("\n2️⃣ Loading license...")
    license_data = lm.load_license()
    print(f"   Status: {license_data.get('status')}")
    
    if license_data.get('status') != 'error':
        print(f"   Serial: {license_data.get('serial')}")
        print(f"   Hardware ID (stored): {license_data.get('hardware_id')[:20]}...")
        print(f"   License Type: {license_data.get('license_type')}")
        print(f"   Expiry Date: {license_data.get('expiry_date')}")
        print(f"   Status: {license_data.get('status')}")
    else:
        print(f"   Error: {license_data.get('message')}")
    
    # 3. Check hardware ID
    print("\n3️⃣ Current hardware ID...")
    hw_id = lm.get_hardware_id()
    print(f"   Current: {hw_id}")
    
    # 4. Verify license
    print("\n4️⃣ Verifying license...")
    is_valid, message = lm.verify_license()
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")
    
    # 5. Check if serial validates against hardware
    if license_data.get('status') != 'error':
        print("\n5️⃣ Validating serial against hardware...")
        serial = license_data.get('serial')
        hw_id = license_data.get('hardware_id')
        
        validates = lm.serial_generator.validate_serial(serial, hw_id)
        print(f"   Serial '{serial}' validates for hardware ID: {validates}")
        
        # Also check against CURRENT hardware
        current_hw_id = lm.get_hardware_id()
        current_validates = lm.serial_generator.validate_serial(serial, current_hw_id)
        print(f"   Serial '{serial}' validates for CURRENT hardware: {current_validates}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
