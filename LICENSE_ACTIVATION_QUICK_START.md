# LICENSE ACTIVATION - QUICK START GUIDE ✅

**Status:** All fixes applied and verified. The system now works correctly!

---

## Step-by-Step: Generate License & Activate

### Step 1: Start License Generator

Run the serial generator standalone tool:

```bash
python serial_generator.py
```

A GUI window will appear showing:
- **Hardware ID:** Unique identifier for your computer
- Generate button
- License type selector
- Output fields

### Step 2: Generate Serial Number

1. Click **"Auto-Generate"** or **"Generate Serial"** button
2. The system will generate a serial key like: `AV-XXXX-XXXX-XXXX-HHHH`
   - Example: `AV-CQYR-DPQZ-PD77-ECCD` ✅
3. Click **"Copy Serial"** to copy to clipboard

### Step 3: Activate in License Dialog

When you run the main program:

```bash
python Aventa_HFT_Pro_2026_v7_3_6.py
```

The **License Activation Dialog** will appear (if not activated yet):

1. **Hardware ID** displays automatically:
   - Should match the Hardware ID in serial_generator.py ✅
   - Example: `AB4$FBA8$459C2E4`

2. **Paste Serial Number** into the input field:
   - Right-click and Paste (Ctrl+V)
   - Should start with `AV-` ✅
   - Should have 5 parts separated by dashes ✅

3. Click **"Activate"** button

### Step 4: Success! ✅

If done correctly:
- ✅ Serial validation succeeds
- ✅ `license.json` file is created
- ✅ Main program starts normally
- ✅ License status shows in program

---

## What Was Fixed

### The Problem ❌
Serial generation used **SHA256** hash but activation validation expected **MD5** hash.

Result: All serials failed validation with error:
```
"Serial number does not match this hardware"
```

### The Solution ✅
Changed serial_generator.py line 33:
```python
# BEFORE (broken)
return hashlib.sha256(hw_id.encode()).hexdigest()[:4].upper()

# AFTER (fixed)
return hashlib.md5(hw_id.encode()).hexdigest()[:4].upper()
```

### Verification ✅
Ran comprehensive tests:
- ✅ Hash function consistency verified
- ✅ Serial format correct (AV-XXXX-XXXX-XXXX-HHHH)
- ✅ Complete validation flow tested
- ✅ All tests PASSED

---

## Troubleshooting

### Error: "Serial number does not match this hardware"

**Cause:** Serial doesn't match the hardware ID it was generated for

**Solution:**
1. Verify Hardware ID matches between:
   - **serial_generator.py** window (top-left) 
   - **License Activation dialog** (top-right)
2. Copy the exact serial from serial_generator.py
3. Paste exactly into dialog (must start with `AV-`)

### Hardware ID doesn't match

**Cause:** serial_generator.py and activation dialog show different IDs

**Solution:**
1. Run serial_generator.py on THE SAME COMPUTER as main program
2. Don't copy serials between different computers
3. Each computer has unique hardware ID

### Dialog doesn't appear

**Cause:** License already activated, or program started with valid license

**Solution:**
1. Delete `license.json` file if you want to re-activate
2. Run program again to show dialog

---

## File Reference

| File | Purpose |
|------|---------|
| `serial_generator.py` | Generate serial numbers for your hardware |
| `license_manager.py` | Validates serials and manages licenses |
| `license_check.py` | Quick license verification on startup |
| `license_validator.py` | Strict license enforcement |
| `license.json` | Your activated license (created after successful activation) |

---

## Success Indicators ✅

Your license system is working correctly if:

1. **serial_generator.py** generates serials starting with `AV-`
2. **License Activation dialog** appears when running main program
3. **Hardware ID** displays in dialog
4. **Serial validation** succeeds without errors
5. **license.json** file appears in program directory
6. **Main program** starts normally

All of the above are now ✅ WORKING!

---

**Questions or Issues?** Check the error message in the dialog and refer to Troubleshooting section above.
