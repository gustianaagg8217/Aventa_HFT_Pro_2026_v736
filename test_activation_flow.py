#!/usr/bin/env python3
"""
Test Complete License Activation Flow with Trial License
"""

from license_manager import LicenseManager
from datetime import datetime, timedelta

def test_activation_flow():
    print("\n" + "="*70)
    print("🧪 TEST: Complete License Activation Flow")
    print("="*70)
    
    lm = LicenseManager()
    
    # Simulate activation with TRIAL serial (from screenshot)
    trial_serial = "AV-SLA7-ABC1-T7XX-57DC"
    
    print(f"\n1️⃣ Create license with serial: {trial_serial}")
    license_data = lm.create_license(trial_serial)
    
    # Check if there was an error
    if license_data.get("status") == "error":
        print(f"❌ Error: {license_data.get('message')}")
        return False
    
    # Display created license data
    print(f"\n✅ License created successfully!")
    print(f"   Serial: {license_data.get('serial')}")
    print(f"   Hardware ID: {license_data.get('hardware_id')[:16]}...")
    print(f"   License Type: {license_data.get('license_type')}")
    print(f"   Expiry Days: {license_data.get('expiry_days')}")
    print(f"   Expiry Date: {license_data.get('expiry_date')}")
    print(f"   Status: {license_data.get('status')}")
    
    # Now generate the success message as it would appear in the GUI
    print(f"\n2️⃣ Generate success message (as shown in GUI):")
    print("-" * 70)
    
    license_type = license_data.get('license_type', 'unknown').upper()
    expiry_date = license_data.get('expiry_date')
    
    if license_type == 'UNLIMITED':
        license_info = "📅 Type: UNLIMITED (No Expiry)"
    elif license_type == 'TRIAL':
        license_info = "📅 Type: TRIAL (7 Days)"
    else:
        # Custom days license
        expiry_days = license_data.get('expiry_days', 0)
        license_info = f"📅 Type: LIMITED ({expiry_days} Days)"
        if expiry_date:
            expiry_dt = datetime.fromisoformat(expiry_date)
            license_info += f"\n📆 Expires: {expiry_dt.strftime('%d %B %Y')}"
    
    message = (
        f"License activated successfully!\n\n"
        f"{license_info}\n\n"
        f"This serial number is now bound to this computer.\n"
        f"The application will now start."
    )
    
    print("SUCCESS MESSAGE:")
    print(message)
    print("-" * 70)
    
    # Verify it's correct
    if "TRIAL (7 Days)" in message:
        print(f"\n✅ CORRECT! Message shows 'TRIAL (7 Days)'")
        return True
    elif "UNLIMITED" in message:
        print(f"\n❌ ERROR! Message incorrectly shows 'UNLIMITED'")
        return False
    else:
        print(f"\n❓ Unexpected message format")
        return False

if __name__ == "__main__":
    success = test_activation_flow()
    print("\n" + "="*70)
    if success:
        print("✅ LICENSE TYPE FIX VERIFIED!")
    else:
        print("❌ LICENSE TYPE FIX FAILED!")
    print("="*70)
