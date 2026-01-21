# 🔐 LICENSE SYSTEM QUICK START

## What This Does

✅ **Requires license activation to run program**
✅ **Serial number tied to specific computer (hardware binding)**
✅ **Cannot use same serial on different computers**
✅ **License file encrypted and secured**

---

## Installation

### 1. Install cryptography package
```bash
pip install cryptography
```

### 2. Files included
- `license_manager.py` - Core license system
- `license_check.py` - Startup license check
- `serial_generator.py` - Admin tool to generate serials

---

## For Customers (End Users)

### First time running:

1. Run: `python Aventa_HFT_Pro_2026_v7_3_6.py`

2. See license activation dialog with your **Hardware ID**

3. Send Hardware ID to admin/reseller

4. Receive Serial Number from admin

5. Paste Serial Number in dialog → Click "Activate"

6. ✅ Program is now ready to use!

### After first activation:

- Just run the program normally
- License is remembered
- Program starts immediately

---

## For Admin/Reseller

### Generate serial for customer:

1. Run: `python serial_generator.py`

2. Paste customer's **Hardware ID**

3. Click "Generate Serial"

4. Get the **Serial Number**

5. Send to customer

---

## Integration with Main Program

### Add 2 lines to main file:

```python
# At TOP after imports:
from license_check import enforce_license_on_startup

# In main block BEFORE creating GUI:
if __name__ == "__main__":
    if not enforce_license_on_startup():
        sys.exit(1)
    
    # ... rest of your code ...
```

---

## How It Works

### Hardware ID
- Unique identifier for each computer
- Based on: MAC address, Processor ID, Disk serial, Hostname, etc.
- Cannot be spoofed

### Serial Number Format
- Pattern: `AV-XXXX-XXXX-XXXX-HHHH`
- Last 4 characters derived from customer's Hardware ID
- Only works on that specific hardware

### License File
- Encrypted with customer's hardware ID
- Cannot be opened/moved to different computer
- Stored as `license.json`

---

## Security

🔒 **Hardware Binding** - Serial locked to specific computer
🔒 **Encryption** - License file encrypted, unreadable without correct hardware
🔒 **Validation** - License verified every program start
🔒 **No Transfer** - Cannot copy license to different computer

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "License file not found" | Run program first time to activate |
| "Serial does not match hardware" | Serial is for different computer, get new one |
| "License bound to different hardware" | Cannot transfer license, need new serial |
| Error decrypting license | Delete license.json, re-activate |

---

## File Locations

```
Aventa_HFT_Pro_2026_v736/
├── Aventa_HFT_Pro_2026_v7_3_6.py (modified)
├── license_manager.py
├── license_check.py
├── serial_generator.py
├── license.json (auto-created at activation)
└── serial_records.json (admin records)
```

---

## Key Features

| Feature | Details |
|---------|---------|
| **Activation Required** | Must activate before first use |
| **Hardware Locked** | Each serial for one computer only |
| **Encrypted Storage** | License file cannot be copied or hacked |
| **Easy Activation** | Just paste serial and click "Activate" |
| **No Expiry** | Once activated, no time limit (can be extended later) |
| **Admin Control** | Admin generates and tracks all serials |

---

## Next Steps

1. ✅ Copy `license_manager.py` to project folder
2. ✅ Copy `license_check.py` to project folder
3. ✅ Copy `serial_generator.py` to project folder
4. ✅ Edit main program file (add 2 lines of import + 2 lines check)
5. ✅ Test activation process
6. ✅ Done!

---

See **LICENSE_SYSTEM_GUIDE.md** for detailed documentation.
See **IMPLEMENTATION_EXAMPLE.py** for code examples.

