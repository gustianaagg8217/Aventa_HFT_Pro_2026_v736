# 🕐 LICENSE EXPIRY SYSTEM - Complete Guide

## Overview

The license system now supports **expiry-based licenses** allowing you to:
- ✅ **Unlimited licenses** (no expiry date)
- ✅ **Trial licenses** (7 days, auto-expires)
- ✅ **Custom licenses** (any number of days you specify)

---

## Features

### 1. Unlimited License
- **No expiry date** - License never expires
- **Perfect for**: Permanent customers, bulk purchases
- **Admin selection**: "🔓 Unlimited (No expiry)"

### 2. Trial License (7 Days)
- **Expires in 7 days** automatically
- **Perfect for**: Free trials, demo access
- **Admin selection**: "⏱️ Trial 7 Days (auto expire)"

### 3. Custom License
- **Expires in N days** (you choose the number)
- **Perfect for**: Monthly subscriptions (30 days), quarterly (90 days), etc.
- **Admin selection**: "📅 Custom Days" + enter number

---

## How It Works

### For Admin / Reseller

#### Step 1: Generate Serial with Expiry Type
```
1. Run: python serial_generator.py
2. Paste customer's Hardware ID
3. Select License Type:
   - Unlimited: No expiry
   - Trial: 7 days
   - Custom: Enter number of days (e.g., 30, 90, 180)
4. Click "Generate Serial"
5. Send serial to customer
```

#### Step 2: Records
- All serials are saved in `serial_records.json`
- Shows license type and expiry date for each serial
- Perfect for tracking subscriptions

### For End User

#### First Time
1. Run: `python Aventa_HFT_Pro_2026_v7_3_6.py`
2. See activation dialog with Hardware ID
3. Send Hardware ID to admin
4. Receive serial (with expiry info)
5. Paste serial → Click "Activate"
6. Program starts!

#### During Trial (Last 3 Days)
- Warning dialog appears: "License expiring in X days"
- Click OK to continue
- Reminder to renew

#### After Expiry
- Program shows: "License has expired X days ago"
- Cannot start program
- Must renew license (get new serial)

---

## License File Structure

### Unlimited License
```json
{
  "serial": "AV-5E9E-D5DB-B9B0-249C",
  "hardware_id": "444F6B290AAE751D",
  "activation_date": "2026-01-21T10:30:45.123456",
  "expiry_date": null,
  "license_type": "unlimited",
  "expiry_days": -1,
  "status": "active",
  "version": "7.3.6"
}
```

### Trial License (7 Days)
```json
{
  "serial": "AV-38C9-6035-D6B3-249C",
  "hardware_id": "444F6B290AAE751D",
  "activation_date": "2026-01-21T10:30:45.123456",
  "expiry_date": "2026-01-28T10:30:45.123456",
  "license_type": "trial",
  "expiry_days": 7,
  "status": "active",
  "version": "7.3.6"
}
```

### Limited License (Custom Days)
```json
{
  "serial": "AV-F737-17AC-67E7-249C",
  "hardware_id": "444F6B290AAE751D",
  "activation_date": "2026-01-21T10:30:45.123456",
  "expiry_date": "2026-02-20T10:30:45.123456",
  "license_type": "limited",
  "expiry_days": 30,
  "status": "active",
  "version": "7.3.6"
}
```

---

## Serial Records (Admin Tracking)

File: `serial_records.json`

```json
[
  {
    "serial": "AV-5E9E-D5DB-B9B0-249C",
    "hardware_id": "444F6B290AAE751D",
    "generated": "2026-01-21T10:30:45.123456",
    "license_type": "Unlimited",
    "expiry_days": -1,
    "expiry_date": null,
    "activated": false
  },
  {
    "serial": "AV-38C9-6035-D6B3-249C",
    "hardware_id": "ABC123DEF456GHI",
    "generated": "2026-01-21T11:00:00.123456",
    "license_type": "Trial (7 days)",
    "expiry_days": 7,
    "expiry_date": "2026-01-28T11:00:00.123456",
    "activated": true
  }
]
```

---

## Usage Examples

### Example 1: Generate Unlimited Serial
```
Admin Console → Serial Generator tab
→ Enter Hardware ID: ABC123XYZ789
→ Select: "🔓 Unlimited (No expiry)"
→ Click "Generate Serial"
→ Result: AV-XXXX-XXXX-XXXX-HHHH (no expiry)
```

### Example 2: Generate 7-Day Trial
```
Admin Console → Serial Generator tab
→ Enter Hardware ID: ABC123XYZ789
→ Select: "⏱️ Trial 7 Days (auto expire)"
→ Click "Generate Serial"
→ Result: AV-XXXX-XXXX-XXXX-HHHH (expires in 7 days)
```

### Example 3: Generate 30-Day License
```
Admin Console → Serial Generator tab
→ Enter Hardware ID: ABC123XYZ789
→ Select: "📅 Custom Days"
→ Enter Days: 30
→ Click "Generate Serial"
→ Result: AV-XXXX-XXXX-XXXX-HHHH (expires in 30 days)
```

---

## Verification Process

### On Every Program Start

```python
if __name__ == "__main__":
    if LICENSE_SYSTEM_AVAILABLE:
        if not enforce_license_on_startup():
            print("❌ License verification failed. Exiting application.")
            sys.exit(1)
    
    # Program continues...
```

### License Check Steps

1. **Load license file** (`license.json`)
2. **Decrypt** with hardware key
3. **Verify serial matches hardware**
4. **Check expiry date**:
   - If `expiry_date` is NULL → Unlimited, always valid
   - If `expiry_date` > NOW → Valid
   - If `expiry_date` ≤ NOW → Expired, invalid
5. **If valid**: Load program
6. **If invalid**: Show activation dialog

---

## Expiry Behavior

### 3 Days Before Expiry
- ⚠️ Warning dialog shows: "License expires in X days"
- User can click OK to continue
- Warning appears every time program starts

### On Expiry Day
- ❌ Program cannot start
- Error message: "License has expired"
- Must renew with new serial

### License Duration Examples

| License Type | Duration | Use Case |
|---|---|---|
| Unlimited | ∞ (never) | Permanent customers |
| Trial | 7 days | Free trial |
| Monthly | 30 days | Subscription |
| Quarterly | 90 days | Quarterly plan |
| 6 Months | 180 days | Long-term |
| Annual | 365 days | Yearly plan |

---

## Technical Details

### License Type Determination
```python
if expiry_days == -1:
    license_type = "unlimited"  # No expiry
elif expiry_days == 7:
    license_type = "trial"      # 7-day trial
else:
    license_type = "limited"    # Custom days
```

### Expiry Date Calculation
```python
expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
```

### Expiry Verification
```python
expiry_date_str = license_data.get('expiry_date')
if expiry_date_str is not None:  # Not unlimited
    expiry_date = datetime.fromisoformat(expiry_date_str)
    if datetime.now() > expiry_date:
        return False, "License has expired..."
```

---

## Admin Console Features

### Serial Generator Tab
- Input Hardware ID
- Select License Type (Unlimited / Trial / Custom)
- Generate Serial
- Copy Serial to clipboard
- View generation log

### Records Tab
- View all generated serials
- See license types and expiry dates
- Track which serials are activated
- Historical record of all generations

---

## Troubleshooting

| Issue | Solution |
|---|---|
| "License has expired" | Admin generates new serial, customer re-activates |
| "License expires in X days" warning | Normal warning, customer can renew when ready |
| License type shows "unknown" | Delete `license.json` and re-activate |
| Expiry date not showing | Check that `expiry_date` field exists in license file |
| Custom days not working | Verify number is positive (>0) |

---

## Testing

Run the test suite to verify expiry system:

```bash
python test_expiry_system.py
```

Tests include:
- ✅ Unlimited license creation
- ✅ Trial license (7 days)
- ✅ Custom license (30, 90 days)
- ✅ Expired license detection
- ✅ License type determination
- ✅ Data persistence

---

## Related Files

| File | Purpose |
|---|---|
| `license_manager.py` | Core expiry logic, encryption |
| `serial_generator.py` | Admin tool, license type selection |
| `license_check.py` | Startup verification, warnings |
| `test_expiry_system.py` | Test suite for expiry features |
| `license.json` | Encrypted license file (created automatically) |
| `serial_records.json` | Admin records of all generated serials |

---

## Security

🔒 **Expiry dates are encrypted** in license file
- Cannot be modified without valid hardware key
- Decryption fails on different hardware
- Date validation happens at runtime

🔒 **Serial number format includes hardware checksum**
- Serial only works on specific hardware
- Expiry tied to hardware binding

---

## Future Enhancements (Optional)

- [ ] Automatic serial renewal via online service
- [ ] License extension for existing customers
- [ ] Multi-device subscription (2-3 computers)
- [ ] Email reminders before expiry
- [ ] License history/audit log
- [ ] Bulk license generation

---

**Last Updated**: January 21, 2026  
**Version**: 7.3.6

